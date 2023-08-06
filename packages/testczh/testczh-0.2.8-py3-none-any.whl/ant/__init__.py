# pyant
import os
import sys

ant_root_path = os.path.dirname(os.path.abspath(__file__))
if ant_root_path not in sys.path:
    sys.path.append(ant_root_path)

__version__ = '0.3.0'

from pyant import *
from rpc_call_helper import call, async_call
from logger import log_dbg, log_inf, log_wrn, log_err, log_fat
