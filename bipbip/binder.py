import json
import os
from typing import List, Optional, Tuple
import random
import string
import encryption
import base64

class Binder(object):
    """
    binder is an object to save, read and interact with the users informations.

    The decrypting data of the user can be load with json and we optain the following structure :

    userdict = json.load(data)

    userdict = { website_code [str] : website_info [dict] }

    website_info = { '__name__' : website_name [str] , '__data__' : website_data [list], '__encrypted__' : bool}

    website_data = [ website_datum [tuple] ]

    website_datum = ( type [str] , datum = [str] )

    """
    code_lenght = 10
    private_website_code = []
    encryption_iterations = 100_000

    def __init__(self) -> None:
        super().__init__()
        self.userdict = {}

    def load(self, data: bytearray) -> None:
        """
        loads the data from the decrypted data bytearray using json.loads to generate the userdict.

        .. note::
            The data will be deleted from `data` in the method.

        Parameters
        ----------
            data : bytearray
                The decrypted data containing user informations.
        
        Raises
        ------
            TypeError 
                If the data is not bytearray.
            JSONDecodeError
                If the data bytearray can't be read.
        """
        if not isinstance(data, bytearray):
            raise TypeError("Parameter data is not bytearray.")
        if len(data) == 0:
            self.userdict = {}
        else :
            self.userdict = json.loads(data.decode('utf-8'))
    
    def dump(self) -> bytearray:
        """
        dumps the userdict into the decrypted data bytearray using json.dumps.

        Returns
        -------
            data : bytearray
                The decrypted data containing user informations.
        """
        if len(self.userdict.keys()) == 0:
            data = bytearray("".encode('utf-8'))
        else :
            data = bytearray(json.dumps(self.userdict).encode('utf-8'))
        return data
    
    def listing_website_codes(self) -> List[str]:
        """
        returns the list containing the website codes.

        Returns
        -------
            website_codes : List[str]
                 The list containing the website codes.
        """
        website_codes = list(self.userdict.keys())
        # Removing private code keys.
        website_codes = [website_code for website_code in website_codes if website_code not in self.private_website_code]
        return website_codes

    def is_website_code(self, website_code: str) -> bool:
        """
        returns True if the website code exists in the userdict keys.

        Parameters
        ----------
            website_code : str
                 The code of a website.
        
        Returns
        -------
            bool
                If the website code is associated with a website.
        
        Raises
        ------
            TypeError
                If the website code is not a string.
        """
        if not isinstance(website_code, str):
            raise TypeError("Parameter website_code must be a string")
        return website_code in self.listing_website_codes()

    def generate_website_code(self) -> str:
        """
        generates a new website code.
        
        Returns
        -------
            website_code : str
                A new website code used instead.
        """
        chars = string.ascii_letters + string.digits
        website_code = ''.join(random.choice(chars) for _ in range(self.code_lenght))
        website_codes = self.listing_website_codes()
        while website_code in website_codes or website_code in self.private_website_code: 
            website_code = ''.join(random.choice(chars) for _ in range(self.code_lenght))
        return website_code

    def get_website_name(self, website_code: str) -> str:
        """
        returns the name of the given website.
        
        Parameters
        ----------
            website_code : str
                 The code of a website.

        Returns
        -------
            website_name : str
                The name of the website.

        Raises
        ------
            TypeError
                If the website code is not a string.
            ValueError
                If the website code is not associated with an existing website.
        """
        if not self.is_website_code(website_code):
            raise ValueError("Parameter website_code is not associated with an existing website.")
        return self.userdict[website_code]['__name__']
    
    def set_website_name(self, website_code: str, website_name: str) -> None:
        """
        Sets the name of the given website.
        
        Parameters
        ----------
            website_code : str
                 The code of a website.
            website_name : str
                The name of the website.

        Raises
        ------
            TypeError
                If the website code or name is not a string.
            ValueError
                If the website code is not associated with an existing website.
        """
        if not self.is_website_code(website_code):
            raise ValueError("Parameter website_code is not associated with an existing website.")
        if not isinstance(website_name, str):
            raise TypeError("Parameter website_name is not a string.")
        self.userdict[website_code]['__name__'] = website_name

    def get_website_data_number(self, website_code: str) -> int:
        """
        returns the number of data stored for the given website.
        
        Parameters
        ----------
            website_code : str
                 The code of a website.

        Returns
        -------
            website_data_number : int
                The number of data stored for the website.

        Raises
        ------
            TypeError
                If the website code is not a string.
            ValueError
                If the website code is not associated with an existing website.
        """
        if not self.is_website_code(website_code):
            raise ValueError("Parameter website_code is not associated with an existing website.")
        return len(self.userdict[website_code]['__data__'])

    def is_encrypted_website_data(self, website_code: str) -> bool:
        """
        returns true if the data of the website are encrypted.
        
        Parameters
        ----------
            website_code : str
                 The code of a website.

        Returns
        -------
            is_encrypted : bool
               If the data are encrypted for the website.

        Raises
        ------
            TypeError
                If the website code is not a string.
            ValueError
                If the website code is not associated with an existing website.
        """
        if not self.is_website_code(website_code):
            raise ValueError("Parameter website_code is not associated with an existing website.")
        return self.userdict[website_code]['__encrypted__']
    
    def set_website_data_encryption(website_code, set_encrypted: bool) -> None:
        """
        Activates or deactivates encryption of a website.

        .. warning::
            The data must be reset in the website to apply changes ! 
        
        Parameters
        ----------
            website_code : str
                 The code of a website.
            set_encrypted : bool 
                 The status of __encrypted__ key.

        Raises
        ------
            TypeError
                If the website code is not a string.
                If the set_encrypted is not a booleen.
            ValueError
                If the website code is not associated with an existing website.
        """
        if not self.is_website_code(website_code):
            raise ValueError("Parameter website_code is not associated with an existing website.")
        if not isinstance(set_encrypted, bool):
            raise TypeError("Parameter set_encrypted is not a boolen.")
        self.userdict[website_code]['__encrypted__'] = set_encrypted

    def get_website_data(self, website_code: str, *, user_key: Optional[bytearray] = None) -> List[Tuple[str, str]]:
        """
        returns the decrypted data of the website.
        
        Parameters
        ----------
            website_code : str
                 The code of a website.
            user_key : Optional[bytearray]
                 Requiered only if the data are encrypted. The default is None.

        Returns
        -------
            website_data : List[List[str, str]]
                The list containing the decrypted website data.

        Raises
        ------
            TypeError
                If the website code is not a string.
                If the user_key is not un bytearray when the data are encrypted.
            ValueError
                If the website code is not associated with an existing website.
            encryption.WrongKeyError
                If the user_key is incorrect.
                If the encryptedtext has been modified.
        """
        if not self.is_encrypted_website_data(website_code):
            return self.userdict[website_code]['__data__']
        # if encryption
        if user_key is None:
            raise TypeError("Parameter user_key is required for encrypted website data.")
        if not isinstance(user_key, bytearray): 
            raise TypeError("Parameter user_key is not bytearray.")
        website_data = self.userdict[website_code]['__data__']
        for index, datum in enumerate(website_data):
            try:
                encrypted_datum = bytearray(base64.b64decode(datum[1]))
                decrypted_datum = encryption.encryptedtext_to_data(encrypted_datum, user_key.copy(), iterations = self.encryption_iterations)
                website_data[index] = (datum[0], decrypted_datum.decode('utf-8'))
            except encryption.WrongKeyError:
                encryption.delete_bytearray(user_key) # Securely delete user_key from memory if decryption fails
                raise
        encryption.delete_bytearray(user_key)
        return website_data

    def set_website_data(self, website_code: str, website_data: List[Tuple[str, str]], *, user_key: Optional[bytearray] = None) -> None:
        """
        sets the data of the website.
        
        Parameters
        ----------
            website_code : str
                 The code of a website.
            website_data : List[List[str, str]]
                The list containing the decrypted website data.
            user_key : Optional[bytearray]
                 Requiered only if the data are encrypted. The default is None.

        Raises
        ------
            TypeError
                If the website code is not a string.
                If the user_key is not un bytearray when the data are encrypted.
                If the website data is not list.
            ValueError
                If the website code is not associated with an existing website.
                If the website data is not is not well structured.
        """
        if not isinstance(website_data, list):
            raise TypeError("Parameter website_data is not list.")
        if not all(isinstance(website_datum, tuple) and len(website_datum) == 2 and all(isinstance(datum,str) for datum in website_datum) for website_datum in website_data):
            raise ValueError("Parameter website_data is not well structured.")
        if not self.is_encrypted_website_data(website_code):
            self.userdict[website_code]['__data__'] = website_data
            return 
        # if encryption
        if user_key is None:
            raise TypeError("Parameter user_key is required for encrypted website data.")
        if not isinstance(user_key, bytearray): 
            raise TypeError("Parameter user_key is not bytearray.")
        for index, datum in enumerate(website_data):
            decrypted_datum = bytearray(datum[1].encode('utf-8'))
            encrypted_datum = encryption.data_to_encryptedtext(decrypted_datum, user_key.copy(), iterations = self.encryption_iterations)
            website_data[index] = (datum[0], base64.b64encode(encrypted_datum).decode('utf-8'))
        self.userdict[website_code]['__data__'] = website_data
        encryption.delete_bytearray(user_key)
        return website_data

    def remove_website(self, website_code: str) -> None:
        """
        Removes the website from the userdict.
        
        Parameters
        ----------
            website_code : str
                 The code of a website.

        Raises
        ------
            TypeError
                If the website code is not a string.
            ValueError
                If the website code is not associated with an existing website.
        """
        if not self.is_website_code(website_code):
            raise ValueError("Parameter website_code is not associated with an existing website.")
        del self.userdict[website_code]

    def add_website(self, website_code: str, website_name: str = "") -> None:
        """
        Adds a new website on the userdict.
        
        Parameters
        ----------
            website_code : str
                 The code of a website.
            website_name : str
                The name of the website. The default is "".

        Raises
        ------
            TypeError
                If the website code or name is not a string.
            ValueError
                If the website code is associated with an existing website.
        """
        if self.is_website_code(website_code):
            raise ValueError("Parameter website_code is associated with an existing website.")
        self.userdict[website_code] = {"__name__" : "",
                                       "__encrypted__" : False,
                                       "__data__" : []}
        self.set_website_name(website_code, website_name)
        
