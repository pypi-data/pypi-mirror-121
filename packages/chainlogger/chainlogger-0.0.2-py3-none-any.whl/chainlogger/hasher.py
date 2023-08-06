from chainlogger.parser_class import ParserClass
import hashlib


class Hasher:
    """
        A class to hash the values, add salt and verify with given values.

        ...

        Attributes
        ----------
        salt : str
            a salt value to randomize the hash

        Methods
        -------
        create(string)

        add0x(string)

        hash_with_salt(string)

        verify_input(string, string)
    """

    def __init__(self, salt):
        """
        Initialize the given class.
            Parameters:
                salt (string): a salt value to randomize the hash
        """
        self.salt = salt

    @staticmethod
    def create(salt):
        """
        Returns the initialized class.
            Parameters:
                salt (string): a salt value to randomize the hash
        Returns:
                Hasher (class): A hasher class
        """
        return Hasher(salt)

    @staticmethod
    def add0x(input_x):
        """
        Returns the "0x" added version of the input.
            Parameters:
                input_x (string): a data
            Returns:
                value (string): "0x" merged with a data
        """
        return "0x" + input_x

    def hash_with_salt(self, input_x):
        """
        Returns the hashed with sha256 version of the data.
            Parameters:
                input_x (string): a data
            Returns:
                value (string): hashed and salted version of the data
        """
        hashed_data = hashlib.sha256((input_x + self.salt).encode()).hexdigest()
        return hashed_data

    def verify_input(self, hashed_input, raw_data):
        """
        Takes the raw input and hashed_input, and makes a comparison.
            Parameters:
                hashed_input (string): a hashed data
                raw_data (string): a raw data
            Returns:
                value (boolean): are they the same or not
        """
        to_check = Hasher.add0x(self.hash_with_salt(ParserClass.json_encode(element=raw_data)))

        if hashed_input == to_check:
            return True
        else:
            return False
