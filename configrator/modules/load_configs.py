import configparser
import os 

### local imports ####################################

from .error import error
from ...paths import config_path
from .ui import initizer_ui

######################################################

def configurator():

    if not os.path.isdir(os.path.dirname(config_path)):
        os.mkdir(os.path.dirname(config_path))
    
        