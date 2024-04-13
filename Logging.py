"""
Logger Module
"""
__author__ = 'H115-125'
__version__ = 'V 6.0.0'

# -----------------Start of Import statements------------------------ #
import logging.handlers
import os.path
import time
from configparser import ConfigParser
# -----------------end of Import statements------------------------ #
CONFIGURATION_FILE = "app.conf"
parser = ConfigParser()
parser.read(CONFIGURATION_FILE)
base_path = parser.get('LogDetails', 'basepath')
image_path = parser.get("ImageDetails", "basepath")
if not os.path.exists(image_path):
    os.makedirs(image_path)
try:
    log_level = parser.get('LogDetails', 'log_level')
except Exception as e:
    log_level = "INFO"
try:
    serviceName = parser.get('LogDetails', 'serviceName')
except Exception as e:
    serviceName = "CricFace"
# --------------------- Purpose : To create logger ------------------ #
LOG_FILE_UPLOADER = base_path +"/"+ serviceName
if not os.path.exists(LOG_FILE_UPLOADER):
    os.makedirs(LOG_FILE_UPLOADER)
    with open(f"{LOG_FILE_UPLOADER}.log", "x"):
        pass
logger = logging.getLogger(serviceName)
hdlr_uploader = logging.FileHandler(LOG_FILE_UPLOADER +'.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', "%Y-%m-%d %H:%M:%S")
hdlr_uploader.setFormatter(formatter)
logger.addHandler(hdlr_uploader)
logger.setLevel(log_level)
logger.debug('Logger Initialized \n')
