import os
import time

from deep_learning.fundamental_training_nn import FaultTrainingNn
# from data_splitter import path_data
# from data_splitter import DataSplitter
from utilities import log
from utilities.common_methods import getDebugInfo


class FundamentalPredictor:
    def __init__(self):

        try:
            # load the already optimized neural network.
            self.model = FaultTrainingNn.load_model_from_json()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_data_to_evaluate(self, path_files=None):

        try:
            # I will get the data to evaluate from a file stored in a folder.
            if path_files is None:
                path_files_to_evaluate = os.path.join(path_data, 'test')
            else:
                path_files_to_evaluate = path_files

            list_files = [f for f in os.listdir(path_files_to_evaluate) if os.path.isfile(os.path.join(path_files_to_evaluate, f))]
            list_files.sort()

            data, ground_truth = FaultTrainingNn.initialise_tensor(list_files, path_files_to_evaluate)

            FaultTrainingNn.fill_data_vectors(list_files, path_files_to_evaluate, data, ground_truth)
            FaultTrainingNn.normalize_data(data)

            counter_faults = 0
            truth = 'N/A'
            for index, sample in enumerate(data):
                sample = sample.reshape((1, 1000, 6))
                result = FaultTrainingNn.predict_sample(sample, self.model)

                if result.item(0) > 0.5:
                    counter_faults += 1
                else:
                    continue

                truth = ground_truth[index].item(0)
                if truth == 1:
                    truth = 'fault'
                elif truth == 0:
                    truth = 'no fault'
                else:
                    truth = 'N/A'

            if counter_faults == 0:
                result = 'no fault'
            elif counter_faults == 1:
                result = 'possible fault in 1 day'
            elif counter_faults == 2:
                result = 'possible fault in 1 hour'
            elif counter_faults > 2:
                result = 'possible fault very soon'
            else:
                result = 'case not understood'

            log.info(f"the sample you just input was classified as {result}.\nThe truth is {truth}")

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def delete_evaluation_files(path_files):
        """
        The method deletes the files used for the evaluation
        @return Nothing
        """
        try:
            list_files = [os.path.join(path_files, f) for f in os.listdir(path_files) if os.path.isfile(os.path.join(path_files, f))]
            for file in list_files:
                os.remove(file)
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")


def predict_fault(path_data_to_predict):
    try:
        # The original list of files which have been stored in the folder when extracting synchronous data
        path_originals = os.path.join(path_data_to_predict, 'original')
        original_files = [os.path.join(path_originals, f) for f in os.listdir(path_originals) if os.path.isfile(os.path.join(path_originals, f))]
        original_files.sort()

        # send a single original file each time to be predicted.
        for file in original_files:
            DataSplitter.read_data_and_split(file, max_num_sample_per_file=1000, key='prediction', counter_files=0, paths_data_files=path_data_to_predict)

            fault_predictor = FaultPredictor()
            fault_predictor.get_data_to_evaluate(path_files=path_data_to_predict)

            time.sleep(1)
            fault_predictor.delete_evaluation_files(path_files=path_data_to_predict)

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")


if __name__ == "__main__":

    # The following is the path where data used for the prediction is stored.
    # The data extracted from the Wristbot app needs to be stored in a folder called 'original'
    # In this case the structure will be in the following way.
    # path_data_to_predict = "./data/prediction"
    #   ./failure_prediction/data/prediction/original   <- where to find data extracte from the wristbot
    #   ./failure_prediction/data/prediction/           <- where the data used for prediction will be split and stored.

    path_data_to_predict = "./data/prediction"

    predict_fault(path_data_to_predict)