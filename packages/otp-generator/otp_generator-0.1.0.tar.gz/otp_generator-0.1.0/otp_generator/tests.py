from unittest import TestCase
from faker import Faker


# Create your tests here.
from otp_generator.otp import OtpServer


class TestAuthentication(TestCase):
    def setUp(self) -> None:
        fake = Faker()
        self.user = fake.ascii_safe_email()

    def tearDown(self) -> None:
        self.user = None

    def test_access_token(self) -> None:
        otp = OtpServer(self.user)
        otp_entry = otp.generate_otp()
        assert otp_entry[0]
        assert otp_entry[1]
        assert otp_entry[2]
        assert 8 > len(otp_entry[2]) >= 6
