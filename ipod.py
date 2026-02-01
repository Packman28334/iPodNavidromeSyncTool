import os
from dotenv import load_dotenv
load_dotenv()

import gpod # type: ignore

db = gpod.Database(os.environ["IPOD_PATH"])
