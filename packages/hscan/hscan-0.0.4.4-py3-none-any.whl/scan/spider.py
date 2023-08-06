import asyncio
import random
from abc import ABCMeta, abstractmethod
from scan import logger
from scan.config import Config
from scan.util import get_local_ip, get_local_name


class Spider(object):
    __metaclass__ = ABCMeta

    def __init__(self, spider_name, cfg_path):
        self.spider_name = spider_name
        self.spider_id = self.spider_id()
        self.config = Config(cfg_path)
        self.status = 1
        self.rabbitmq = None
        self.mongo_db = None
        self.redis_conn = None
        self.oss_conn = None
        self.task_num = None

    def spider_id(self):
        local_ip = get_local_ip()
        container_id = get_local_name()[:12]
        spider_id = local_ip + '_' + container_id + '_' + self.spider_name
        with open('spider_id', 'w') as f:
            f.write(spider_id)
            f.close()
        return spider_id

    @abstractmethod
    async def process(self, task_info):
        pass

    async def site(self):
        """
        1. 可以对配置文件进行修改
        eg：
            self.config.config.set('client', 'task_num', 1)
        :return:
        2. 可以设置新的成员变量
        eg:
            self.mq2 = ''
        """

    @abstractmethod
    async def init(self):
        """
        初始化数据处理连接
        eg:
            mq_config = self.config.rabbitmq()
            self.rabbitmq = RabbitMQ(host=mq_config.get('host'), port=mq_config.get('port'), user=mq_config.get('user'),
                           password=mq_config.get('password'))
            await self.rabbitmq.init()
        :return:
        """

    async def queue_task(self):
        task_queue = self.config.rabbitmq().get('task_queue')
        if not self.rabbitmq:
            await logger.error('The task queue connection is not initialized')
            return
        while self.status:
            try:
                res = await self.rabbitmq.consume(task_queue)
                if res:
                    task_info, message = res
                else:
                    await asyncio.sleep(10)
                    continue
                pres = await self.process(task_info)
                if pres:
                    await message.ack()
            except Exception as e:
                await logger.error(e)

    async def simple_task(self):
        while self.status:
            try:
                pres = await self.process(None)
                if pres:
                    pass
            except Exception as e:
                await logger.error(e)

    async def run(self, task_num=None):
        await self.site()
        if task_num and isinstance(task_num, int):
            self.task_num = task_num
        else:
            self.task_num = int(self.config.client().get('task_num'))
        await self.init()
        task_type = self.config.client().get('task_type')
        task_list = []
        if task_type == 'simple':
            for _ in range(self.task_num):
                t = asyncio.create_task(self.simple_task())
                task_list.append(t)
        else:
            for _ in range(self.task_num):
                t = asyncio.create_task(self.queue_task())
                task_list.append(t)
        await asyncio.gather(*task_list)

