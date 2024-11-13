import unittest
import os
import shutil

# Import the functions from the filesmanager.py module
import bipbip.filesmanager as fm

class TestAccountManagement(unittest.TestCase):
    
    def setUp(self):
        """ Prepare the test directory. """
        self.account_name = '----testuser----'
        self.password = bytearray("password123".encode('utf-8'))
        self.pin = bytearray("1234".encode('utf-8'))
        self.accounts_dir = os.path.join(fm.dirname(__file__,2), 'files', 'accounts')

        if fm.exist_account(self.account_name): 
            fm.delete_account(self.account_name)

    def test_01_is_valid_account_name_valid(self):
        """ Test a valid account name. """
        self.assertTrue(fm.is_valid_account_name("valid_account-123"))
        
    def test_02_is_valid_account_name_invalid(self):
        """ Test an invalid account name. """
        self.assertFalse(fm.is_valid_account_name("invalid account!"))
    
    def test_03_create_account(self):
        """ Test account creation. """
        if not fm.exist_account(self.account_name):  # Ensure the account doesn't already exist
            fm.create_account(self.account_name, self.password, self.pin)
        
        account_path = fm.get_account_path(self.account_name)
        self.assertTrue(os.path.isdir(account_path))  # Check if the folder was created.
    
    def test_04_get_account_path(self):
        """ Test the account path. """
        if not fm.exist_account(self.account_name):  # Ensure the account doesn't already exist
            fm.create_account(self.account_name, self.password, self.pin)
        
        account_path = fm.get_account_path(self.account_name)
        expected_path = os.path.join(self.accounts_dir, self.account_name)
        self.assertEqual(account_path, expected_path)
    
    def test_05_get_UI_icon(self):
        """ Test the default UI icon. """
        icon_name = "default_profile"
        icon_path = fm.get_UI_icon(icon_name)
        self.assertTrue(os.path.isfile(icon_path))  # Check if the icon file exists

    def test_06_get_existing_accounts(self):
        """ Test fetching existing accounts. """
        # Create an account to ensure the function returns a list of existing accounts
        if not fm.exist_account(self.account_name):
            fm.create_account(self.account_name, self.password, self.pin)
        
        existing_accounts = fm.get_existing_accounts()
        self.assertIn(self.account_name, existing_accounts)

    def test_07_delete_account(self):
        """ Test account deletion. """
        # Create an account to test it
        if not fm.exist_account(self.account_name):
            fm.create_account(self.account_name, self.password, self.pin)
        
        account_path = fm.get_account_path(self.account_name)
        self.assertTrue(os.path.isdir(account_path))  # Ensure the account exists

        fm.delete_account(self.account_name)
        self.assertFalse(os.path.isdir(account_path))  # Ensure the account was deleted


if __name__ == "__main__":
    unittest.main()
