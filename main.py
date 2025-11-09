import json
import time
import uuid
import datetime
from admin import ADMINID, ADMINTOKEN, TOKFILE, TOKDUR
autho_users = {}
def authusers():
    tokens = loadtok()
    for _, data in tokens["used"].items():
        user_id = data.get("user_id")
        expiry_str = data.get("expiry")
        expiry_ts = get_expiry_ts(expiry_str)
        if user_id and (not expiry_ts or time.time() < expiry_ts):
            autho_users[user_id] = True

def loadtok():
    try:
        with open(TOKFILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        default_tokens = {"active": {}, "used": {}}
        savetok(default_tokens)
        return default_tokens

def savetok(tokens):
    with open(TOKFILE, "w") as f:
        json.dump(tokens, f, indent=4)

def get_expiry_ts(expiry_str):
    if expiry_str == "never":
        return None
    else:
        return datetime.datetime.strptime(expiry_str, '%Y-%m-%d %H:%M:%S').timestamp()

def gentok(duration_type):
    if duration_type not in TOKDUR:
        raise ValueError("Invalid duration type. Choose: 7days, 30days, lifetime")
    token = str(uuid.uuid4())
    expiry = None if TOKDUR[duration_type] is None else time.time() + TOKDUR[duration_type]
    tokens = loadtok()
    def convert_ts(ts):
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    expiry_str = "never" if expiry is None else convert_ts(expiry)
    tokens["active"][token] = {"expiry": expiry_str, "user_id": None, "type": duration_type}
    savetok(tokens)
    return token

def validtok(token, user_id):
    tokens = loadtok()
    for used_token, data in tokens["used"].items():
        if data["user_id"] == user_id:
            expiry_ts = get_expiry_ts(data["expiry"])
            if not expiry_ts or time.time() < expiry_ts:
                expiry_time = "never" if not expiry_ts else datetime.datetime.fromtimestamp(expiry_ts).strftime('%Y-%m-%d %H:%M:%S')
                return False, f"You already have an active token that expires at: {expiry_time}. Wait before activating a new one."
    if token in tokens["used"]:
        return False, "Token already used."
    if token not in tokens["active"]:
        return False, "Invalid token."
    data = tokens["active"][token]
    expiry_ts = get_expiry_ts(data["expiry"])
    if expiry_ts and time.time() > expiry_ts:
        return False, "Token expired."
    data["user_id"] = user_id
    tokens["used"][token] = data
    del tokens["active"][token]
    savetok(tokens)
    autho_users[user_id] = True
    expiry= "never expires" if not expiry_ts else f"expires at {datetime.datetime.fromtimestamp(expiry_ts).strftime('%Y-%m-%d %H:%M:%S')}"
    return True, f"Token activated successfully! Your access {expiry}"

def accesschck(user_id):
    if user_id in autho_users:
        return True
    tokens = loadtok()
    for t, data in tokens["used"].items():
        if data["user_id"] == user_id:
            expiry_ts = get_expiry_ts(data["expiry"])
            if not expiry_ts or time.time() < expiry_ts:
                autho_users[user_id] = True
                return True
    return False