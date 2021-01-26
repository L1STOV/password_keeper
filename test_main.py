import unittest
from main import set_up_root_password, passwords_requirements_checker


class TestMain(unittest.TestCase):
    def setUp(self):
        self.root_password = 'Temp123456789#'

    def tearDown(self):
        self.root_password = ''

    def test_set_up_root_password(self):
        self.assertEqual(set_up_root_password(self.root_password), '*** root password was created ***')

    def test_password_requirements_checker(self):
        self.assertEqual(passwords_requirements_checker(self.root_password), '*** password requirements are met *** ')


if __name__ == '__main__':
    unittest.main()
