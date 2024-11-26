from pyutils import Dir_util
import os

PROJ_DIR = Dir_util.get_cur_dir(__file__)

OUTPUT_DIR = os.path.join(PROJ_DIR, "output")
if os.path.exists(OUTPUT_DIR) == False:
    os.mkdir(OUTPUT_DIR)