import base64
import hashlib
import os
import random
import re
import time
import uuid
from collections import namedtuple
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.twofactor import InvalidToken
from cryptography.hazmat.primitives.twofactor.hotp import HOTP
from cryptography.hazmat.primitives.twofactor.totp import TOTP

from otp_generator import settings


def is_blocked_user(user: str) -> bool:
    # Validate from data source if the given user/email is not blacklisted or blocked by service
    return NotImplemented


def otp_generated_signal(cmd: Callable, data: Any = None) -> None:
    """
    Fire event or signal of OTP created. Alternative call operation (cmd) to be performed when an OTP is created
    :param cmd: Callable to be executed
    :param data: data to pass to the function. Multiple data can be passed as dictionary
    :return: None
    """
    if callable(cmd):
        return cmd(**data)


def otp_auth_failed_signal(cmd: Callable, data: Any = None) -> None:
    """
    Fire event or signal of OTP failed authentication.
    Alternative call operation (cmd) to be performed when an OTP authentication fails
    :param cmd: Callable to be executed
    :param data: data to pass to the function. Multiple data can be passed as dictionary
    :return:
    """
    if callable(cmd):
        return cmd(**data)


def user_black_listed_signal(cmd: Callable, data: Any = None) -> None:
    """
    # Fire event or signal of blacklisting user due to many failed attempts
    # Alternative call operation (cmd) to be performed when a user is block-listed
    :param cmd: Callable to be executed
    :param data: data to pass to the function. Multiple data can be passed as dictionary
    :return:
    """
    if callable(cmd):
        return cmd(**data)


def save_otp_signal(cmd: Callable, data: Any = None) -> None:
    """
    # Fire event or signal to save newly generated OTP.
    # Alternative call operation (cmd) to be performed when OTP is to be saved to a database
    :param cmd: Callable to be executed
    :param data: data to pass to the function. Multiple data can be passed as dictionary
    :return:
    """
    if callable(cmd):
        return cmd(**data)


otp_entry = namedtuple('OtpRecord', ('key', 'reference', 'code_hash'))


def generate_token() -> str:
    user_code = base64.urlsafe_b64encode(str(uuid.uuid4()).encode())
    return user_code.decode()


def _generate_totp(length: int = 6, times_step: int = 30):
    if length < 6 or length > 8:
        length = settings.DEFAULT_CODE_LENGTH
    if times_step < settings.TIME_STEP:
        times_step = settings.TIME_STEP
    try:
        key = os.urandom(settings.KEY_SIZE)
        totp = TOTP(key=key, length=length, algorithm=SHA256(), time_step=times_step,
                    backend=default_backend())
        time_value = time.time()
        totp_value = totp.generate(time_value)
        return totp_value, key, time_value
    except ValueError:
        raise ValueError('Invalid OTP parameter(s) provided')
    except TypeError:
        raise TypeError('Unsupported operation used for generating OTP')
    except Exception:
        raise Exception('Invalid operation')


def _generate_hotp(counter: int = 0):
    try:
        if isinstance(counter, int) and counter < 0:
            counter = 0
        key = os.urandom(settings.KEY_SIZE)
        hotp = HOTP(key=key, length=6, algorithm=SHA256(), backend=default_backend())
        hotp_value = hotp.generate(counter)
        return hotp_value, key
    except ValueError:
        raise ValueError('Invalid user key provided for OTP')
    except TypeError:
        raise TypeError('Unsupported operation used for generating OTP')
    except Exception:
        raise Exception('Invalid operation')


def _verify_totp(code: bytes, key: str, timer: Any = None):
    try:
        timer = settings.TIME_STEP if timer is None else timer
        totp = TOTP(key=key.encode(), length=len(code), algorithm=SHA256(), backend=default_backend(), time_step=timer)
        return True if totp.verify(code, timer) is None else False
    except InvalidToken:
        raise


def _verify_hotp(code: bytes, key: str, counter: int = 0):
    try:
        hotp = HOTP(key=key.encode(), length=len(code), algorithm=SHA256(), backend=default_backend())
        return True if hotp.verify(code, counter) is None else False
    except InvalidToken:
        raise


def otp_unblock(auth, username):
    # Attempt using perm as auth or AUTH_KEY_HASH
    return NotImplemented


class OTP(Enum):
    HOTP = 139
    TOTP = 177


class OtpServer:
    __slots__ = '_counter', '_throttle', '_codes', '_service', '_account', '_session', \
                '_cache', '_wait', '_timer', '_user_hash', 'USER_IDENTIFIER', 'user'

    def __init__(self, user: str):
        self._counter = 0
        self._cache = dict()
        # validate email
        self._session = None
        self._throttle = 0
        self._codes = []
        self._wait = 0
        self._timer = None
        self.USER_IDENTIFIER = 'email'
        abbreviation = generate_token()[:4]
        self._user_hash = abbreviation.upper()

        if isinstance(user, str) and re.match(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', user):
            self.user = user
        else:
            raise RuntimeError('Invalid user object provided')
        self._account = user

    @property
    def counter(self):
        return self._counter

    @property
    def throttle(self):
        return self._throttle

    @property
    def codes(self):
        return self._codes

    @property
    def service(self):
        return self._service

    @property
    def account(self):
        return self._account

    @property
    def session(self):
        return self._session

    @session.setter
    def session(self, value):
        self._session = value if isinstance(value, str) else None

    @property
    def wait(self):
        return self._wait

    def _make_code_hash(self, reference: Any) -> str:
        return hashlib.md5(str(reference).encode()).hexdigest()

    def _check_code_hash(self, reference: Any):
        return hashlib.md5(reference).hexdigest()

    def generate_otp(self, otp_type: Any = 'HOTP', cmd: Callable = None):
        created = datetime.now()
        expiration = created + timedelta(hours=24)
        if otp_type == 'HOTP' or otp_type == OTP.HOTP:
            reference = random.randint(1000, 9999)
            hotp, key = _generate_hotp(counter=reference)
            if key and len(hotp) >= 6:
                # send otp_signal
                reference = str(reference).encode()
                otp_generated_signal(cmd, data={
                    'sender': self.__class__,
                    'user': self.user,
                    'otp': hotp,
                    'key': key,
                    'reference': reference,
                    'code_hash': self._make_code_hash(reference),
                    'created_at': created,
                    'expire_at': expiration})
                return otp_entry(key, reference, hotp)
        elif otp_type == 'TOTP' or otp_type == OTP.TOTP:
            totp, key, timer = _generate_totp(times_step=settings.TIME_STEP)
            if key and len(totp) >= 6:
                reference = str(timer).encode()
                otp_generated_signal(cmd, data={
                    'sender': self.__class__,
                    'user': self.user,
                    'otp': totp,
                    'key': key,
                    'reference': reference,
                    'code_hash': self._make_code_hash(reference),
                    'created_at': created,
                    'expire_at': expiration})
                return otp_entry(key, reference, totp)

    def verify_otp(self, code: int, key: Any, reference: Any, otp_type: Any = 'HOTP', throttle: int = 1, wait: int = 0,
                   failed_cmd: Callable = None,
                   blacklist_cmd: Callable = None):

        def _pre_check_lockout(throttle, wait, entity: str, service: str = None, save_cmd: Callable = None):
            if throttle and wait:
                if (throttle > settings.MAX_COUNT) or (wait > settings.MAX_WAIT_DURATION):
                    # send the fail otp authentication signal
                    otp_auth_failed_signal(failed_cmd, data={
                        'sender': self.__class__,
                        'user': entity,
                        'code': code,
                        'created_at': datetime.now(),
                        'service': service})
                    user_black_listed_signal(blacklist_cmd, data={
                        'sender': self.__class__,
                        'user': entity,
                        'code': code,
                        'created_at': datetime.now(),
                        'service': service
                    })

                throttle += settings.COUNT_FACTOR
                wait = throttle * 60000
                save_otp_signal(save_cmd, data={'throttle': throttle, 'wait': wait})
                return throttle, wait

        if not self.user:
            raise RuntimeError("Selected user does not exist. Ensure user is registered or "
                               "valid user email is provided")
        # validate if the user has been blacklisted
        # is_blocked_user(user)
        if is_blocked_user(self.user):
            raise RuntimeError('Unable to process request for blocked account')

        try:
            if otp_type == 'HOTP' or otp_type == OTP.HOTP:
                if not (reference and key):
                    return False
                if _verify_hotp(str(code).encode(), key, int(reference)):
                    return self._make_code_hash(reference)
                else:
                    return False

            elif otp_type == 'TOTP' or otp_type == OTP.TOTP:
                if _verify_totp(str(code).encode(), key, float(reference)):
                    return self._make_code_hash(reference)
                else:
                    return False

        except InvalidToken:
            raise
        finally:
            return _pre_check_lockout(throttle, wait, entity=self.user, service='OTP validation')

    def otp_provisioning_url(self, user: str, otp_type: Any, key: Any, reference: Any, issuer: str = None) -> Any:
        if not user:
            raise RuntimeError('Invalid user account provided. Ensure user is registered or '
                               'has valid email')
        if not issuer and settings.ISSUER:
            issuer = settings.ISSUER
        if otp_type == 'HOTP' or otp_type == OTP.HOTP:
            hotp = HOTP(key=key, length=settings.DEFAULT_CODE_LENGTH, algorithm=SHA256(),
                        backend=default_backend())
            return hotp.get_provisioning_uri(account_name=self._user_hash, counter=reference, issuer=issuer)
        else:
            totp = TOTP(key=key, length=settings.DEFAULT_CODE_LENGTH, algorithm=SHA256(),
                        backend=default_backend(), time_step=settings.TIME_STEP)
            return totp.get_provisioning_uri(account_name=self._user_hash, issuer=issuer)
