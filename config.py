import os

API_ID = int(os.environ.get("API_ID", "25531611"))
API_HASH = os.environ.get("API_HASH", "2f63a48be678dfea4ad03e495377403f")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8659589420:AAG5yM6ZQKxZzVLvGe1NQSF0_EogMtZpjQw")
PASS_DB = int(os.environ.get("PASS_DB", "721"))
OWNER = int(os.environ.get("OWNER", "8553304761"))
LOG = []

try:
    ADMINS = []
    for x in (os.environ.get("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")
if OWNER:
    ADMINS.append(OWNER)
