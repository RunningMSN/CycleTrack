import os
import shutil
import datetime
from ..site_settings import DB_LOC, DB_NAME
def backup_db():
    if os.path.exists(f"{DB_LOC}/{DB_NAME}"):
        shutil.copy(f"{DB_LOC}/{DB_NAME}", f"{DB_LOC}/{DB_NAME}_{datetime.datetime.now().timestamp()}")
