from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH", "")
TOKRN = getenv("TOKEN", "")
LOG_BOT = getenv("LOG_BOT", "")
MONGO = getenv("MONGO", "")
REDIS = getenv("REDIS", "")
REDIS_PW = getenv("REDIS_PW", "")
OWNER_ID = int(getenv("OWNER_ID", ""))