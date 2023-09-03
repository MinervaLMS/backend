from .user_register_tests import RegisterTestCase
from .user_login_tests import LoginTestCase
from .forgot_password_tests import PasswordResetTestCase
from .users_list_tests import GetUsersTestCase
from .contact_support_tests import ContactSupportTestCase

_ = [
    RegisterTestCase,
    LoginTestCase,
    PasswordResetTestCase,
    GetUsersTestCase,
    ContactSupportTestCase,
]
