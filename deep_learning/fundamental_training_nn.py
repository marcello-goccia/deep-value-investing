import os
import sys

import csv
import numpy as np
import matplotlib.pyplot as plt

from keras import models
from keras import layers
from keras.models import model_from_json
from keras.utils.np_utils import to_categorical

from utilities.log import root_folder_all_code

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_root = dir_path.split(root_folder_all_code, 1)[0]
code_path = os.path.join(dir_root, root_folder_all_code)
sys.path.insert(0, code_path)

from data_storing.assets.database_manager import DatabaseManager as db_mngr
from utilities import log
from utilities.common_methods import getDebugInfo


class FundamentalTrainingNn:
    """
    Class used to find the parameters for the neural network needed to identify the equities among the ones with
    good fundamentals which have higher chance to succeed in the stock market.
    """
    def __init__(self, num_epochs=None, batch_size=None):
        """
        Constructor of the Fundamental Training class.
        """
        try:
            self.equities = db_mngr.query_all_equities_by()

            self.path_data = dict()

            self.data = dict()
            self.ground_truth = dict()
            self.sizes = dict()

            self.model = None

            self.history = None
            self.history_dict = None

            if num_epochs is None:
                self.num_epochs = 50
            else:
                self.num_epochs = num_epochs

            if batch_size is None:
                self.batch_size = 12
            else:
                self.batch_size = batch_size
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def initialise_tensor(files, path_data):
        """
        Given the data in input, it returns a tensor of all the data initialised with default values.
        @return the initialised tensor of data.
        """
        try:
            num_samples = len(files)

            file = os.path.join(path_data, files[0])
            with open(file, "r") as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                header = next(reader, None)
                num_timestamps = sum(1 for row in reader)
                num_features = 6  # len(header) - 1  # TODO FIX THIS AND EXTRACT THE CORRECT NUMBERS OF FEATURES!!!
                float_data = np.zeros((num_samples, num_timestamps, num_features))
                ground_truth = np.zeros(num_samples)
            return float_data, ground_truth

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            return None

    def load_data(self, path_data):
        """
        It takes in input the path of the training data, and parses the data to produce tensors usable by the Network.
        @return Nothing
        """
        try:
            for label in data_labels:
                self.path_data[label] = os.path.join(path_data, label)

            # if path_data is not available run al least once the splitter to produce the data.
            for path in self.path_data.values():
                if not os.path.isdir(path):
                    log.info("Generating the data to train the network because missing.")
                    split_data()

            available_files = dict()

            from os import listdir
            from os.path import isfile, join

            # loop through folders train, validation and test.
            for label, path_data in self.path_data.items():  # labels -> train, validation, test.
                available_files[label] = [f for f in listdir(path_data) if isfile(join(path_data, f))]
                self.data[label], self.ground_truth[label] = FaultTrainingNn.initialise_tensor(available_files[label], path_data)

            self.sizes = self.get_data_size(self.data)

            for label, list_files in available_files.items():
                FundamentalTrainingNn.fill_data_vectors(list_files, self.path_data[label], self.data[label], self.ground_truth[label])

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def fill_data_vectors(list_files, path, data, ground_truth=None):
        """
        The method fills up the vectors with the data and the ground_truth (if available)
        taking the data from the list of files passed as input
        @param list_files list of files in input
        @param path the path where to find the files in the list_files
        @param data the data to fill up
        @param ground_truth the ground truth of the data to fill up, it cannot be passed, if not needed.
        @return Nothing
        """
        try:
            for current_file, file in enumerate(list_files):
                path_file = os.path.join(path, file)
                with open(path_file, "r") as csv_file:
                    reader = csv.reader(csv_file, delimiter=',')
                    header = next(reader, None)
                    for current_row, row in enumerate(reader):
                        if len(row) == 8:
                            row = row[:-1]  # this will be done in case the by mistake I selected more columns.
                        data[current_file, current_row, :] = row[1:]

                    if ground_truth is not None:
                        ground_truth[current_file] = FundamentalTrainingNn.get_the_id_class_of_the_file(file)

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def get_data_size(data):
        """
        The methods gets a dictionary of data to be used for the learning process and returns a dictoinary
        with all the sizes of the features.
        @param data the dictionary with the data to input into the neaural network.
        @return a dictionary with all the sizes.
        """
        try:
            data_size = dict()
            for key, value in data.items():
                data_size[key] = dict()

                shape = value.shape
                for index, label in enumerate(feats_labels):
                    data_size[key][label] = shape[index]
            return data_size

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def get_the_id_class_of_the_file(file):
        """
        The method returns the clas of the file in input.
        The class of the file is embedded in the file itself.
        @param the file to retrieve the class
        @return the class of the file
        """
        try:
            for id, label in enumerate(keyword_classes):
                if label in file:
                    return id
            return -1
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def normalize_data(data, ground_truth=None):
        """
        Method to normalise the data and prepare them to be fed into the neural network
        @param data the data to normalize.
        @return Nothing
        """
        try:
            # self.train_data = self.train_data.reshape((self.sizes['train']['samples'], self.sizes['train']['timestamps'] * self.sizes['train']['features'] ))
            # self.validation_data = self.validation_data.reshape((self.sizes['validation']['samples'], self.sizes['validation']['timestamps'] * self.sizes['validation']['features'] ))
            # self.test_data = self.test_data.reshape((self.sizes['test']['samples'], self.sizes['test']['timestamps'] * self.sizes['test']['features'] ))

            # data['train'] -= data['train'].mean()
            # data['validation'] -= data['validation'].mean()
            # data['test'] -= data['test'].mean()
            #
            # np.seterr(divide='ignore', invalid='ignore')
            # data['train'] /= data['train'].std()
            # data['validation'] /= data['validation'].std()
            # data['test'] /= data['test'].std()

            if ground_truth is not None:

                # we vectorize the labels
                ground_truth['train'] = np.asarray(ground_truth['train']).astype('float32')
                ground_truth['validation'] = np.asarray(ground_truth['validation']).astype('float32')
                ground_truth['test'] = np.asarray(ground_truth['test']).astype('float32')

                ground_truth['train'] = to_categorical(ground_truth['train'])
                ground_truth['validation'] = to_categorical(ground_truth['validation'])
                ground_truth['test'] = to_categorical(ground_truth['test'])
            pass

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def define_neural_network(self):
        """
        The method defines the structor of the neural network.
        :return:
        """
        try:
            num_timestamps = self.sizes['train']['timestamps']
            num_features = self.sizes['train']['features']

            self.model = models.Sequential()
            self.model.add(layers.Dense(16, activation='relu', input_shape=(num_timestamps, num_features)))
            self.model.add(layers.Dense(32, activation='relu'))
            self.model.add(layers.Flatten())
            self.model.add(layers.Dense(1, activation='sigmoid'))

            self.model.compile(optimizer='rmsprop',
                          loss='binary_crossentropy',
                          metrics=['accuracy'])

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def train(self):
        """
        The method starts training the neural network.
        :return:
        """
        try:
            self.history = self.model.fit(self.data['train'],
                                self.ground_truth['train'],
                                epochs=self.num_epochs,
                                batch_size=self.batch_size,
                                validation_data=(self.data['validation'], self.ground_truth['validation']))

            self.history_dict = self.history.history

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def store_model(self):
        """
        It stores to file the model after having been trained, so to skip the training in the future
        @return Nothing
        """
        try:
            import pickle
            with open('./trained_model/model.pickle', 'wb') as file:
                pickle.dump(self, file)

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def load_model(self):
        """
        It loads from file the model which has been trained, so to skip the training in the future
        @return The object class
        """
        try:
            import pickle
            with open('./trained_model/model.pickle', mode='rb') as file:
                return pickle.load(file)

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def store_model_to_json(self):
        """
        It stores to a json file the model after having been trained, so to skip the training in the future
        @return Nothing
        """
        try:
            # serialize model to JSON
            model_json = self.model.to_json()
            with open("./trained_model/model.json", "w") as json_file:
                json_file.write(model_json)
            # serialize weights to HDF5
            self.model.save_weights("./trained_model/model.h5")
            log.info("Saved model to disk")
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def load_model_from_json(path_file=None):
        """
        It loads from json file the model which has been trained, so to skip the training in the future
        @return The object class
        """
        try:
            if path_file is None:
                path_file = './trained_model'

            model_file = 'model.json'
            weights_file = 'model.h5'

            model_path = os.path.join(path_file, model_file)
            weights_path = os.path.join(path_file, weights_file)

            # load json and create model
            json_file = open(model_path, 'r')
            loaded_model_json = json_file.read()
            json_file.close()

            model = model_from_json(loaded_model_json)
            # load weights into new model
            model.load_weights(weights_path)
            log.info("Loaded model from disk")

            return model
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def evaluate(self):
        """
        The method evaluates the results of the training network measuring the accuracy.
        @return
        """
        try:
            results = self.model.evaluate(self.data['test'], self.ground_truth['test'])
            log.info(f"The output of the neural network evaluation for the test data is - loss: {results[0]} accuracy {results[1]}")
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def plot_training_validation_loss(self):
        """
        The method plots the a grapth to let us understand the goodness of the training and validation output.
        @return Nothing
        """
        try:
            loss_values = self.history_dict['loss']
            val_loss_values = self.history_dict['val_loss']

            accuracy = self.history_dict['accuracy']
            epochs = range(1, len(accuracy) + 1)

            plt.plot(epochs, loss_values, 'bo', label='Training loss')
            plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
            plt.title('Training and validation loss')
            plt.xlabel('Epochs')
            plt.ylabel('Loss')
            plt.legend()
            plt.show()

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def plot_training_validation_accuracy(self):
        """
        The method plots the a grapth to let us understand the goodness of the training and validation output.
        @return Nothing
        """
        try:
            plt.clf()

            accuracy_values = self.history_dict['accuracy']
            epochs = range(1, len(accuracy_values) + 1)

            accuracy_values = self.history_dict['accuracy']
            val_accuracy_values = self.history_dict['val_accuracy']

            plt.plot(epochs, accuracy_values, 'bo', label='Training accuracy')
            plt.plot(epochs, val_accuracy_values, 'b', label='Validation accuracy')
            plt.title('Training and validation accuracy')
            plt.xlabel('Epochs')
            plt.ylabel('Loss')
            plt.legend()
            plt.show()

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def predict_sample(input_sample, model):
        """
        The metohd takes an input sample as input and tries to predict it by using the optimized parameters of the NN
        @param input_sample the input sample to predict
        @param model the model of the neural network used to predict the sample
        @return Nothing
        """
        try:
            output = model.predict(input_sample)
            return output

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")


def train_nn():

    try:
        fault_trainer = FundamentalTrainingNn(num_epochs=3, batch_size=5)
        fault_trainer.load_data(path_data)
        FundamentalTrainingNn.normalize_data(fault_trainer.data)

        fault_trainer.define_neural_network()
        fault_trainer.train()

        # # If needed to store the entire class object and reload for evaluation in the future.
        fault_trainer.store_model_to_json()
        # fault_trainer = fault_predictor.load_model()

        fault_trainer.evaluate()

        fault_trainer.plot_training_validation_loss()
        fault_trainer.plot_training_validation_accuracy()

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")


if __name__ == "__main__":
    train_nn()