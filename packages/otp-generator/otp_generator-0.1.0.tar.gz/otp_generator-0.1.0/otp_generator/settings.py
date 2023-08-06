# Define a list of configuration or settings for the OTP service

MAX_COUNT = 2
MAX_WAIT_DURATION = 3600000  # 1hr in milliseconds
COUNT_FACTOR = 1
AUTH_KEY_HASH = None  # Set to the hashed key of the user. Possibly from config
KEY_SIZE = 40
TIME_STEP = 30
DEFAULT_CODE_LENGTH = 6
ISSUER = '#Your business or brand name here. Leave empty if you want the OTP to be anonymous'
CODE_EXPIRATION = 86400  # Validity period for the generated Code in microseconds
