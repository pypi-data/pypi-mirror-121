import json

from hashlib import sha1
from functools import reduce
from base64 import b85decode, b64decode


def generate_device_info():
    return {
        "device_id": "22CCEA23A7F868405192250D13EDA48245F4442E89293554E7A7320BA4E3F7C6E79985F239D012C1B2",
        "device_id_sig": "Aa0ZDPOEgjt1EhyVYyZ5FgSZSqJt",
        "user_agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.4.33562)"
    }

# okok says: please use return annotations :(( https://www.python.org/dev/peps/pep-3107/#return-values


def decode_sid(sid: str) -> dict:
    return json.loads(b64decode(reduce(lambda a, e: a.replace(*e), ("-+", "_/"), sid + "=" * (-len(sid) % 4)).encode())[1:-20].decode())


def sid_to_uid(SID: str) -> str: return decode_sid(SID)["2"]


def sid_to_ip_address(SID: str) -> str: return decode_sid(SID)["4"]
