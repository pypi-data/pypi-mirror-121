# -*- coding: utf-8 -*-
import os
import sys

protocol_root_path = os.path.dirname(os.path.abspath(__file__))
if protocol_root_path not in sys.path:
    sys.path.append(protocol_root_path)
