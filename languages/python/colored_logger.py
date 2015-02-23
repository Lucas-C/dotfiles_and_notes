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
        'warning': Fore.YELLOW,
        'error': Fore.RED,
        'critical': Back.RED,
    }

    def __init__(self, logger):
        self.logger = logger

    def __getattr__(self, attr_name):
        if attr_name == 'warn':
            attr_name = 'warning'
        if attr_name not in 'debug info warning error critical':
            return getattr(self.logger, attr_name)
        log_level = getattr(logging, attr_name.upper())
        # mimicking logging/__init__.py behaviour :
        if not self.logger.isEnabledFor(log_level):
            return

        def log_method(msg, *args, **kwargs):
            style_prefix = self.COLOR_MAP[attr_name]
            msg = style_prefix + msg + Style.RESET_ALL
            # We call _.log directly to not increase the callstack
            # so that Logger.findCaller extract the corrects filename/lineno
            return self.logger._log(log_level, msg, args, **kwargs)
        return log_method

logging.basicConfig(stream=sys.stderr, format=LOG_FORMAT, level=logging.DEBUG)
LOGGER = ColorLogsWrapper(logging.getLogger(__name__))
LOGGER.debug('Debug')
LOGGER.info('Info')
LOGGER.warn('Warning')
LOGGER.error('Error')
LOGGER.critical('Critical')
