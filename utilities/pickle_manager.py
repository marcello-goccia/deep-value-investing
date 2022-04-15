import pickle
import os
from utilities.json_manager import JsonManager as jSon

extension = 'pkl'

# To read a pickle file from the command line try the following:
# python -mpickle pickle_file.pkl


class PickleManager:

    def __init__(self):
        pass

    @staticmethod
    def save(data, name_file='', path=''):
        """
        Save the dictionary passed as input, data, into a pickle file.

        After saving the data into a pickle file, it stores it into a json file for offline easy reading.
        @param data the dictionary to store
        @param name_file the name of the file where the pickle data will be stored.
        @param path the path where to store the pickle file
        @return The path and filename of the stored pickle file
        """
        if not name_file:
            name_file = f"data.{extension}"
        if extension not in name_file:
            name_file = f'{name_file}.{extension}'

        path_filename = os.path.abspath(os.path.join(path, name_file))

        with open(path_filename, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

        jSon.save(data, path_filename)

        return path_filename

    @staticmethod
    def load(path_filename):
        """
        Load the dictionary from the json file passed as input
        @param path_filename the path and the name of the file where the pickle file was stored
        @return The dictionary loaded
        """
        with open(path_filename, 'rb') as f:
            return pickle.load(f)
