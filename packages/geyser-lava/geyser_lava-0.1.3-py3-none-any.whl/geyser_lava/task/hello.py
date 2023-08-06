from geyser import Geyser
from taskflow.task import Task


@Geyser.task()
class Hello(Task):
    def execute(self, *args, logger, **kwargs):
        logger.debug('Hello, level debug.')
        logger.info('Hello, level info.')
        logger.warning('Hello, level warning')
        logger.error('Hello, level error.')
        logger.critical('Hello, level critical.')
