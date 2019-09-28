import sys
import logging

from .helpers import download


logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO)
logger = logging.getLogger(__name__)


if not download():
    logger.error('Could not download IndoWordNet data.')
    sys.exit(1)


from .iwn import Language
from .iwn import PosTag
from .iwn import SynsetRelations
from .iwn import IndoWordNet
