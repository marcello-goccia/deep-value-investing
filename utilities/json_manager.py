import os
import json
import collections

extension = 'json'


class JsonManager:

    def __init__(self):
        pass

    @staticmethod
    def save(data, path_filename):
        """
        Save the dictionary passed as input, which is data, into a json file.

        The path_filename must already contains the correct path.
        @param data the dictionary to store
        @param path_filename the path and filename of the file where the json string will be stored.
        @return The path and filename of the stored json file
        """

        path_filename = f'{os.path.splitext(path_filename)[0]}.{extension}'
        json_file = json.dumps(data, indent=2)
        f = open(path_filename, "w")
        f.write(json_file)
        f.close()
        return path_filename


    @staticmethod
    def load(path_filename):
        """
        Load the dictionary from the json file passed as input
        @param path_filename the path and the name of the file where the json string was stored
        @return The dictionary loaded
        """
        json_data = open(path_filename).read()
        data = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(json_data)
        return data
