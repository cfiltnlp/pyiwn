import os
from pathlib import Path


IWN_DATA_URL = 'https://www.dropbox.com/s/t29eqq19nt5eygs/iwn_data.tar.gz?dl=1'
USER_HOME = str(Path.home())
IWN_DATA_TEMP_PATH = os.path.join(USER_HOME, 'iwn_data.tar.gz')
IWN_DATA_PATH = os.path.join(*[USER_HOME, 'iwn_data'])
