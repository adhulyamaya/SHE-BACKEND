from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import salted_hmac
from django.utils.http import int_to_base36, base36_to_int
from django.conf import settings
from django.utils.timezone import datetime, now
from django.utils.crypto import constant_time_compare

class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Customize how the hash value is generated
        return (
            str(user.pk) + user.email + str(timestamp) +
            str(user.last_login)
        )

custom_token_generator = CustomTokenGenerator()