import os
import sys
import requests
import logging
import tarfile

import pyiwn.constants as constants


logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def download():
    if os.path.exists(constants.IWN_DATA_PATH):
        return True

    logger.info('Downloading IndoWordNet data of size ~31 MB...')
    with open(constants.IWN_DATA_TEMP_PATH, 'wb') as f:
        try:
            response = requests.get(constants.IWN_DATA_URL, stream=True)
        except Exception as e:
            logger.error(e)
            return False

        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total / 1000), 1024 * 1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50 * downloaded / total)
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                sys.stdout.flush()
    sys.stdout.write('\n')

    logger.info(f'Extracting {constants.IWN_DATA_TEMP_PATH} into {constants.USER_HOME}...')
    tar = tarfile.open(constants.IWN_DATA_TEMP_PATH, "r:gz")
    tar.extractall(constants.USER_HOME)
    tar.close()

    logger.info(f'Removing temporary zip file from {constants.IWN_DATA_TEMP_PATH}')
    os.remove(constants.IWN_DATA_TEMP_PATH)

    logger.info(f'IndoWordNet data successfully downloaded at {constants.IWN_DATA_PATH}')

    return True
