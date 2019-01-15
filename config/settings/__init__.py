import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base import *
from .local import *

# prepend the LOG_DIR to the filenames in LOGGING
for handler in LOGGING['handlers'].values():
    if 'filename' in handler:
        handler['filename'] = os.path.join(LOG_DIR, handler['filename'])

# set the LOG_LEVEL to the loggers in LOGGING
for logger in LOGGING['loggers'].values():
    if logger.get('level') == 'LOG_LEVEL':
        logger['level'] = LOG_LEVEL
