import os
import sys

current_path = os.path.abspath(os.path.dirname(__file__))
# src_path = os.path.join(current_path, "src")
# if os.path.isdir(src_path):
#     sys.path.insert(0, src_path)

WEB_DIRECTORY = "./js"

from . import (
    showcase,
)
