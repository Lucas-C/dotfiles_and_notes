"""
ColoredLogger inspired by https://gist.github.com/1238935 and https://gist.github.com/813057
"""
import logging, sys
from colorama import Back, Fore, Style

LOG_FORMAT = "%(asctime)s - pid:%(process)s %(filename)s:%(lineno)d %(levelname)8s| %(message)s"

class ColorLogsWrapper(object):
    COLOR_MAP = {
        'debug': Fore.CYAN,
        'info': Fore.GREEN,
        'warn': Fore.YELLOW,
        'warning': Fore.YELLOW,
        'error': Fore.RED,
        'critical': Back.RED,
    }

    def __init__(self, logger):
        self.logger = logger

    def __getattr__(self, attr_name):
        attr = getattr(self.logger, attr_name)
        if attr_name not in ('debug', 'info', 'warn', 'warning', 'error', 'critical'):
            return attr
        style_prefix = self.COLOR_MAP[attr_name]

        def wrapped_attr(msg, *args, **kwargs):
            return attr(style_prefix + msg + Style.RESET_ALL, *args, **kwargs)
        return wrapped_attr

logging.basicConfig(stream=sys.stderr, format=LOG_FORMAT, level=logging.DEBUG)
logger = ColorLogsWrapper(logging.getLogger(__name__))
logger.debug('Debug')
logger.info('Info')
logger.warn('Warning')
logger.error('Error')
logger.critical('Critical')
