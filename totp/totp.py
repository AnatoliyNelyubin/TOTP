import time
from typing import Optional
from base58 import b58encode
from secrets import token_bytes
from hashlib import sha256

# totp time window in seconds
# would go to a config in a real microservice

time_window = 15


def generate_secret() -> str:
    """Returns a random 20-symbol base58 string"""
    # return "abcdeabcdeabcdeabcd" + str(int(time.time_ns()) % 9)
    return b58encode(token_bytes(20))[:20].decode()


def generate_code(secret: str,
                  seconds_since_the_epoch: Optional[int] = None) -> str:
    """Generates a TOTP code.
    Arguments:
    secret -- 20-symbol base58 string to act as a secret key to make TOTP code
    seconds_since_the_epoch -- second for which to generate. Current moment if None

    Returns 4-digit string that changes every window"""

    if len(secret) > 20:
        raise ValueError("Secret must be 20-symbol base58 string, is '{}' instead".format(secret))

    if seconds_since_the_epoch is None:
        seconds_since_the_epoch = int(time.time())
    seconds_since_the_epoch = int(seconds_since_the_epoch // time_window)

    # code = str(seconds_since_the_epoch)[-4:]
    hash_object = sha256((str(seconds_since_the_epoch) + secret).encode())
    code = str(abs(int(hash_object.hexdigest(), 16)))[:4]
    return code


def check_code(secret: str, code: str,
               seconds_since_the_epoch: Optional[int] = None) -> bool:
    """Checks if the code is correct for the current moment.
    Arguments:
    secret -- 20-symbol base58 string to act as a secret key to generate TOTP code
    code -- 4-digit string TOTP code.
    seconds_since_the_epoch -- moment at which code should be correct

    Returns True if the code is valid for the provided moment
    """
    if len(code) != 4:
        raise ValueError("TOTP code must be 4 digits string, is '{}' instead".format(code))
    if len(secret) != 20:
        raise ValueError("secret must be 20 symbols long, but it, is '{}' instead".format(len(secret)))
    # return generate_code(secret, seconds_since_the_epoch) == code
    if seconds_since_the_epoch is None:
        seconds_since_the_epoch = int(time.time())
    seconds_since_the_epoch = int(seconds_since_the_epoch // time_window)
    hash_object = sha256((str(seconds_since_the_epoch) + secret).encode())
    check_code = str(abs(int(hash_object.hexdigest(), 16)))[:4]
    return check_code == code