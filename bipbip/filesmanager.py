import os
import shutil
from typing import List
import encryption
import re


def dirname(path: str, deep: int = 1) -> str:
    """
    dirname apply os.path.dirname deep times on the given path.

    Parameters
    ----------
        path : str
            The path of a file or directory.
        deep : int
            The number of call to os.path.dirname, default is 1.
    
    Returns
    -------
        str
            The dirname path.
    
    Raises
    ------
        TypeError
            If the path is not string or deep is not integer.
        ValueError
            If deep is not positive integer.
    """
    if not isinstance(path, str):
        raise TypeError("The path must be a string.")
    if not isinstance(deep, int):
        raise TypeError("The deep must be an integer.")
    if deep <= 0:
        raise ValueError("The deep must be a positive integer")
    for iteration in range(deep):
        path = os.path.dirname(path)
    return path

def is_valid_account_name(account: str) -> bool:
    """
    Validates whether the account name is valid. A valid name contains alphanumeric characters,
    hyphens (`-`), and underscores (`_`).
    
    Parameters
    ----------
        account : str
            The account name.
    
    Returns
    -------
        bool
            True if the account name is valid, False otherwise.
    
    Raises
    ------
        TypeError
            If the account parameter is not a string.
        ValueError
            If the account name is an empty string.
    """
    if not isinstance(account, str):
        raise TypeError("The account name must be a string.")
    if len(account) == 0:
        raise ValueError("The account name cannot be empty.")
    
    pattern = r'^[A-Za-z0-9_-]+$'
    return bool(re.match(pattern, account))

def exist_account(account: str) -> bool:
    """
    Checks if an account with the given name exists.
    
    Parameters
    ----------
        account : str
            The account name.
    
    Returns
    -------
        bool
            True if the account exists, False otherwise.
    
    Raises
    ------
        TypeError
            If the account parameter is not a string.
        ValueError
            If the account name is invalid or non-existent.
    """
    if not is_valid_account_name(account):
        raise ValueError("The account name is invalid.")
    
    accountpath = os.path.join(dirname(__file__,2), 'files', 'accounts', account)
    return os.path.isdir(accountpath)

def get_account_path(account: str) -> str:
    """
    Returns the full path of the account's folder.
    
    Parameters
    ------------------
        account : str
            The account name.
    
    Returns
    -------
        str
            The full path of the account's folder.
    
    Raises
    ------
        TypeError
            If the account parameter is not a string.
        ValueError
            If the account does not exist.
    """
    if not exist_account(account):
        raise ValueError(f"The account '{account}' does not exist.")
    
    return os.path.join(dirname(__file__,2), 'files', 'accounts', account)

def get_existing_accounts() -> List[str]:
    """
    Returns a list of all existing accounts.
    
    Returns
    -------
        List[str]
            A list of account names.
    
    Raises
    ------
        FileNotFoundError
            If the 'accounts' directory is not found.
    """
    accounts_dir = os.path.join(dirname(__file__,2), 'files', 'accounts')
    if not os.path.isdir(accounts_dir):
        raise FileNotFoundError("The 'accounts' directory is not found.")
    
    return [d for d in os.listdir(accounts_dir) if os.path.isdir(os.path.join(accounts_dir, d))]

def get_UI_icon(icon_name: str) -> str:
    """
    Returns the ui icon associated with the given icon name. 
    
    Parameters
    ----------
        icon_name : str
            The icon name.
    
    Returns
    -------
        str
            The path to the ui icon.
    
    Raises
    ------
        TypeError
            If the icon_name parameter is not a string.
        ValueError
            If the account is invalid or does not exist.
        FileNotFoundError
            If the ui icon is not found.
    """
    if not isinstance(icon_name, str):
        raise TypeError("The 'icon_name' parameter must be a string.")

    icon_path = os.path.join(dirname(__file__,2), "files", "iconbank", "iconui", icon_name + ".png")
    
    if not os.path.isfile(icon_path):
        raise FileNotFoundError(f"UI icon {icon_path} not found.")
    
    return icon_path

def get_website_icon(account: str, website_code: str) -> str:
    """
    Returns the icon for a website associated with a given account. If the icon does not exist, 
    returns the default website icon.
    
    Parameters
    ----------
        account : str
            The account name.
        website_code : str
            The website code (site identifier).
    
    Returns
    -------
        str
            The path to the website icon.
    
    Raises
    ------
        TypeError
            If the website_code parameter is not a string.
        ValueError
            If the account is invalid or does not exist.
        FileNotFoundError
            If the default icon is not found.
    """
    if not isinstance(website_code, str):
        raise TypeError("The 'website_code' parameter must be a string.")

    accountpath = get_account_path(account)
    icon_path = os.path.join(accountpath, "icons", website_code + ".png")
    
    if not os.path.isfile(icon_path):
        return get_UI_icon("default_website")
    
    return icon_path

def remove_website_icon(account: str, website_code: str) -> None:
    """
    Removes the icon for a website associated with a given account.
    
    Parameters
    ----------
        account : str
            The account name.
        website_code : str
            The website code (site identifier).
    
    Raises
    ------
        TypeError
            If the website_code parameter is not a string.
        ValueError
            If the account is invalid or does not exist.
        FileNotFoundError
            If the icon file for the website is not found.
    """
    if not isinstance(website_code, str):
        raise TypeError("The 'website_code' parameter must be a string.")

    accountpath = get_account_path(account)
    icon_path = os.path.join(accountpath, "icons", website_code + ".png")
    
    if os.path.isfile(icon_path):
        os.remove(icon_path)

def set_website_icon(account: str, website_code: str, iconpath: str) -> None:
    """
    Sets a new icon for a specific website associated with a given account.
    
    Parameters
    ----------
        account : str
            The account name.
        website_code : str
            The website code (site identifier).
        iconpath : str
            The path to the new icon file.
    
    Raises
    ------
        TypeError
            If the website_code or iconpath parameters are not strings.
        ValueError
            If the account is invalid or does not exist.
        FileNotFoundError
            If the provided icon file is not found.
    """
    if not isinstance(website_code, str):
        raise TypeError("The 'website_code' parameter must be a string.")
    if not isinstance(iconpath, str):
        raise TypeError("The 'iconpath' parameter must be a string.")
    if not os.path.isfile(iconpath):
        raise FileNotFoundError(f"The icon file '{iconpath}' is not found.")

    accountpath = get_account_path(account)
    icon_path = os.path.join(accountpath, "icons", website_code + ".png")
    
    remove_website_icon(account, website_code)
    shutil.copyfile(iconpath, icon_path)

def get_profile_icon(account: str) -> str:
    """
    Returns the profile icon associated with a given account. If it does not exist, 
    returns the default profile icon.
    
    Parameters
    ----------
        account : str
            The account name.
    
    Returns
    -------
        str
            The path to the profile icon.
    
    Raises
    ------
        TypeError
            If the account parameter is not a string.
        ValueError
            If the account is invalid or does not exist.
        FileNotFoundError
            If the default icon is not found.
    """
    accountpath = get_account_path(account)
    profile_icon_path = os.path.join(accountpath, "profile.png")
    
    if not os.path.isfile(profile_icon_path):
        return get_UI_icon("default_profile")
    
    return profile_icon_path

def set_profile_icon(account: str, iconpath: str) -> None:
    """
    Sets a new profile icon for a given account.
    
    Parameters
    ----------
        account : str
            The account name.
        iconpath : str
            The path to the new profile icon.
    
    Raises
    ------
        TypeError
            If the iconpath parameter is not a string.
        ValueError
            If the account is invalid or does not exist.
        FileNotFoundError
            If the provided icon file is not found.
    """
    if not isinstance(iconpath, str):
        raise TypeError("The 'iconpath' parameter must be a string.")
    if not os.path.isfile(iconpath):
        raise FileNotFoundError(f"The icon file '{iconpath}' is not found.")
    
    accountpath = get_account_path(account)
    profile_icon_path = os.path.join(accountpath, "profile.png")
    
    shutil.copyfile(iconpath, profile_icon_path)

def get_encryptedtext_filepath(account: str) -> str:
    """
    Returns the path to the encrypted text file for the given account.
    
    Parameters
    ----------
        account : str
            The account name.
    
    Returns
    -------
        str
            The path to the 'encryptedtext.bin' file.
    
    Raises
    ------
        TypeError
            If the account parameter is not a string.
        ValueError
            If the account is invalid or does not exist.
    """
    if not isinstance(account, str):
        raise TypeError("The 'account' parameter must be a string.")
    
    accountpath = get_account_path(account)
    return os.path.join(accountpath, "encryptedtext.bin")

def get_account_language(account: str) -> str:
    """
    Returns the language of the account from the 'language.txt' file.
    
    Parameters
    ----------
        account : str
            The account name.
    
    Returns
    -------
        str
            The account language (ISO 639-1 code).
    
    Raises
    ------
        TypeError
            If the account parameter is not a string.
        ValueError
            If the 'language.txt' file is not found.
    """
    accountpath = get_account_path(account)
    language_file = os.path.join(accountpath, "language.txt")
    
    if not os.path.isfile(language_file):
        raise ValueError(f"The language file for account '{account}' was not found.")
    
    with open(language_file, 'r') as f:
        return f.read().strip()

def set_account_language(account: str, language: str) -> None:
    """
    Sets the language for the account by writing to the 'language.txt' file.
    
    Parameters
    ----------
        account : str
            The account name.
        language : str
            The language code (ISO 639-1).
    
    Raises
    ------
        TypeError
            If the language parameter is not a string.
        ValueError
            If the account is invalid or does not exist.
    """
    if not isinstance(language, str):
        raise TypeError("The 'language' parameter must be a string.")
    
    accountpath = get_account_path(account)
    language_file = os.path.join(accountpath, "language.txt")
    
    with open(language_file, 'w') as f:
        f.write(language)

def create_account(account: str, password: bytearray, pin: bytearray, language: str = "en") -> None:
    """
    create_account creates a new empty account.
    The password and the pin are used to log-in the account. 

    .. note::
        The language is defined with ISO 639-1 Code.

    Parameters
    ----------
        account : str
            The name of the new account.
        password : bytearray
            The user password.
        pin : bytearray
            The user pin.
        language : str
            The language of the user (default is "en").
    
    Raises
    ------
        TypeError
            If the given argument is of the wrong type.
        ValueError
            If the account already exists, if the account name is invalid, or if password and pin are empty.
    """
    if not isinstance(account,str):
        raise TypeError("Parameter account is not string.")
    if not isinstance(password,bytearray):
        raise TypeError("Parameter password is not bytearray.")
    if not isinstance(pin,bytearray):
        raise TypeError("Parameter pin is not bytearray.")
    if not isinstance(language,str):
        raise TypeError("Parameter language is not string.")
    if len(password) == 0:
        raise ValueError("Parameter password is empty")
    if len(pin) == 0:
        raise ValueError("Parameter pin is empty")
    if len(account) == 0 or not is_valid_account_name(account):
        raise ValueError(f"{account=} is not a valid account name.")
    if exist_account(account):
        raise ValueError(f"{account=} already created.")

    # Creating directory tree for the account
    accountpath = os.path.join(dirname(__file__,2), "files", "accounts", account)
    os.mkdir(accountpath)
    os.mkdir(os.path.join(accountpath, "icons"))
    
    # Creating empty encryptedtext
    data = bytearray("".encode('utf-8'))
    _, _, encryptedtext = encryption.data_to_encryptedtext(data, password, pin=pin)
    
    with open(os.path.join(accountpath, "encryptedtext.bin"), "wb") as file:
        file.write(encryptedtext)
    
    with open(os.path.join(accountpath, "language.txt"), "w") as file:
        file.write(language)
    
    shutil.copyfile(get_UI_icon("default_profile"), os.path.join(accountpath, "profile.png"))

def delete_account(account: str) -> None:
    """
    delete_account removes the account sub-directory from the 'files' directory.
    It also deletes all associated data for the account. 

    Parameters
    ----------
        account : str
            The name of the account to delete.

    Raises
    ------
        TypeError
            If any given argument is of the wrong type.
        ValueError
            If the account does not exist or is invalid.
        FileNotFoundError
            If the account's directory is not found.
    """
    accountpath = get_account_path(account)
    encryptedtextfilepath = get_encryptedtext_filepath(account)
    
    # Erasing all information
    with open(encryptedtextfilepath, "rb") as file:
        encryptedtext = bytearray(file.read())
    
    with open(encryptedtextfilepath, "wb") as file:
        file.write(encryption.random_bytearray(len(encryptedtext)))
    
    encryption.delete_bytearray(encryptedtext)
    
    # Deleting the account subdirectory
    shutil.rmtree(accountpath)

def load_encryptedtext(account: str, password: bytearray, pin: bytearray) -> bytearray:
    """
    load_encryptedtext loads the encrypted text for a given account.

    Parameters
    ----------
        account : str
            The name of the account.
        password : bytearray
            The user password.
        pin : bytearray
            The user pin.

    Returns
    -------
        data : bytearray
            The decrypted data. 

    Raises
    ------
        TypeError
            If any given argument is of the wrong type.
        ValueError
            If the account does not exist or is invalid, or if password and pin are empty.
        ComputationError
            If the decryption process fails.
    """
    class ComputationError(Exception):
        pass

    encryptedtextfilepath = get_encryptedtext_filepath(account)
    
    if not isinstance(password, bytearray):
        raise TypeError("Parameter password is not bytearray")
    if not isinstance(pin, bytearray):
        raise TypeError("Parameter pin is not bytearray")
    if len(password) == 0:
        raise ValueError("Parameter password is empty")
    if len(pin) == 0:
        raise ValueError("Parameter pin is empty")
    
    with open(encryptedtextfilepath, "rb") as file:
        encryptedtext = file.read()

    is_error, error, data = encryption.encryptedtext_to_data(encryptedtext, password, pin=pin)
    
    if is_error:
        # Ensure deleting critical data
        encryption.delete_bytearray(password)
        encryption.delete_bytearray(pin)
        raise ComputationError(f"Error number {error} during decryption. See documentation.")
    
    return data

def dumps_encryptedtext(account: str, password: bytearray, pin: bytearray, data: bytearray) -> None:
    """
    dumps_encryptedtext saves the given data into the encryptedtext.bin file for a given account.

    Parameters
    ----------
        account : str
            The name of the account.
        password : bytearray
            The user password.
        pin : bytearray
            The user pin.
        data : bytearray
            The data to encrypt using AES-CBC.

    Raises
    ------
        TypeError
            If any given argument is of the wrong type.
        ValueError
            If the account does not exist or is invalid, or if password and pin are empty.
        ComputationError
            If the encryption process fails.
    """
    class ComputationError(Exception):
        pass

    encryptedtextfilepath = get_encryptedtext_filepath(account)
    
    if not isinstance(password, bytearray):
        raise TypeError("Parameter password is not bytearray")
    if not isinstance(pin, bytearray):
        raise TypeError("Parameter pin is not bytearray")
    if len(password) == 0:
        raise ValueError("Parameter password is empty")
    if len(pin) == 0:
        raise ValueError("Parameter pin is empty")
    
    is_error, error, encryptedtext = encryption.data_to_encryptedtext(data, password, pin=pin)
    
    if is_error:
        # Ensure deleting critical data
        encryption.delete_bytearray(password)
        encryption.delete_bytearray(pin)
        encryption.delete_bytearray(data)
        raise ComputationError(f"Error number {error} during encryption. See documentation.")
    
    with open(encryptedtextfilepath, "wb") as file:
        file.write(encryptedtext)
