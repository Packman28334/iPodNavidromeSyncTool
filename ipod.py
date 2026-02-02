import os
from dotenv import load_dotenv
load_dotenv()

import gpod # type: ignore

db = gpod.Database(os.environ["IPOD_PATH"])

def get_total_space_on_ipod() -> int: # https://stackoverflow.com/a/12327880
    statvfs = os.statvfs(os.environ["IPOD_PATH"])
    return statvfs.f_frsize * statvfs.f_blocks