import os
from pathlib import Path


IWN_DATA_URL = 'https://www.dropbox.com/s/866wgo0j9l3l386/pyiwn_data.tar.gz?dl=1'
USER_HOME = str(Path.home())
IWN_DATA_TEMP_PATH = os.path.join(USER_HOME, 'pyiwn_data.tar.gz')
IWN_DATA_PATH = os.path.join(*[USER_HOME, 'pyiwn_data'])
