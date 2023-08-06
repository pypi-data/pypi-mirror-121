import json


class ParserClass:
    """
        A parser class to interchange between json objects and python dicts.
        ...
        Methods
        -------
        json_encode(dict)

        json_decode(string)
    """

    @staticmethod
    def json_encode(element):
        """
        Returns the json representation of given element.
            Parameters:
                element (dict): A python dict
        Returns:
                value (str): A string representation of the json object
        """
        return json.dumps(element)

    @staticmethod
    def json_decode(element):
        """
        Returns the dict representation of given json object.
            Parameters:
                element (string): A json object
        Returns:
                value (str): A dict representation of the json object
        """
        return json.loads(element)
