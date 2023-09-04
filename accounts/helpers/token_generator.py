from django.contrib.auth.tokens import PasswordResetTokenGenerator

class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + user.email + str(timestamp) +
            str(user.is_active)
        )

confirmation_token_generator = CustomTokenGenerator()