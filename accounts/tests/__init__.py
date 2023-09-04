from .user_register_tests import RegisterTestCase
from .user_login_tests import LoginTestCase
from .forgot_password_tests import PasswordResetTestCase
from .users_tests import GetUsersTestCase, GetUserTestCase, GetUserCoursesTestCase
from .contact_support_tests import ContactSupportTestCase

_ = [
    RegisterTestCase,
    LoginTestCase,
    PasswordResetTestCase,
    ContactSupportTestCase,
    GetUsersTestCase,
    GetUserTestCase,
    GetUserCoursesTestCase,
]
