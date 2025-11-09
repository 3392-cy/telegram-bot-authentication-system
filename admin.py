import os
from pathlib import Path

ADMINTOKEN = os.environ.get('BOT_TOKEN', "ADMMIN BOT TOKEN HERE")
ADMINID = ADMIN ID HERE
base = Path(__file__).parent
TOKFILE = base / "tokens.json"
TOKDUR = {
    "7days": 7 * 86400,
    "30days": 30 * 86400,
    #you can add more
    "lifetime": None
}