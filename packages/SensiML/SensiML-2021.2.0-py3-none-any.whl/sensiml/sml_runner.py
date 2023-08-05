import os
import json
import ctypes
from ctypes import CDLL
from pandas import DataFrame, Series
from numpy import ndarray
from wurlitzer import pipes


class ImportPathException(Exception):
    pass


def dummy_function(*args, **kwrags):
    print("Not Supported by this version of the Knowledge Pack.")
    return None


class struct_pme_pattern(ctypes.Structure):
    __slots__ = ["influence", "category", "vector"]

    _fields_ = [
        ("influence", ctypes.c_uint16),
        ("category", ctypes.c_uint16),
        ("vector", ctypes.POINTER(ctypes.c_uint8)),
    ]


class struct_pme_model_header(ctypes.Structure):
    __slots__ = ["number_patterns", "pattern_length"]

    _fields_ = [
        ("number_patterns", ctypes.c_uint16),
        ("pattern_length", ctypes.c_uint16),
    ]


class struct_tf_micro_model_result(ctypes.Structure):
    __slots__ = ["num_outputs", "output_tensor"]

    _fields_ = [
        ("num_outputs", ctypes.c_ubyte),
        ("output_tensor", ctypes.POINTER(ctypes.c_float)),
    ]


def empty_function(*args, **kwargs):
    print("Not Supported by this Knowledge Pack.")
    return


class Model(object):
    def __init__(self, neuron_array, class_map, configuration, feature_summary=None):
        self._class_map = None
        self._feature_summary = None
        self._neuron_array = None
        self._configuration = None

        self.class_map = class_map
        self.neuron_array = neuron_array
        self.configuration = configuration

        if feature_summary:
            self.feature_summary = feature_summary
        else:
            self.feature_summary_from_neurons()

    @property
    def class_map(self):
        return self._class_map

    @class_map.setter
    def class_map(self, value):
        self._class_map = value

    @property
    def neuron_array(self):
        return self._neuron_array

    @neuron_array.setter
    def neuron_array(self, value):
        self._neuron_array = value

    @property
    def configuration(self):
        return self._configuration

    @configuration.setter
    def configuration(self, value):
        self._configuration = value

    @property
    def feature_summary(self):
        return self._feature_summary

    @feature_summary.setter
    def feature_summary(self, value):
        self._feature_summary = [{"Feature": str(x)} for x in value]

    def feature_summary_from_neurons(self):
        feature_vector = self.neuron_array[0]["Vector"]
        self.feature_summary = [{"Feature": str(x)} for x in range(len(feature_vector))]


class SMLRunner(object):
    """
    This class provides a python interface to the knowledgpack libary generated by SensiML.
    After downloading the knowledgpack for your platform, you can instantiate this function
    by passing the path to libsensiml.so

        sml = SMLRunner(<path_to_libsensiml.so>)
        sml.init_model()

    Then, you can pythonically call all of the c functions in kb.h passing data like you
    normally would.  For example, if you have a dataframe df which has your sensor data
    stored in it,

        print(df.head(2))
        > AccX, AccY, AccZ
            9    10     11
            12   8      23

    you can call run_model and pass a single sample at a time to run the model as you would
    on the device.

        for index in range(len(df)):
            category = sml.run_model(df.iloc[index].values, 0, model_index)
            if category >= 0:
                print(category)
                sml.reset_model(0)

    """

    def __init__(self, path):
        self._run_type = None
        self._model_initialized = False
        if os.name == "nt":
            print("SML Runner is not supported on Windows OS.")

        if not os.path.exists(os.path.join(path, "libsensiml.so")):
            print("ERROR: libsensiml.so as not found in {}.".format(path))
            raise ImportPathException(
                "ERROR: libsensiml.so as not found in {}".format(path)
            )

        clf_lib = CDLL(os.path.join(path, "libsensiml.so"))
        self._model_init = clf_lib.kb_model_init
        self._model_init.argtypes = []

        self._run_model = clf_lib.kb_run_model
        self._run_model.argtypes = [
            ctypes.POINTER(ctypes.c_int16),
            ctypes.c_int,
            ctypes.c_int,
        ]
        self._run_model.restype = ctypes.c_int

        self._run_segment = clf_lib.kb_run_segment
        self._run_segment.argtypes = [ctypes.c_int]
        self._run_segment.restype = ctypes.c_int

        self._add_segment = clf_lib.kb_add_segment
        self._add_segment.argtypes = [
            ctypes.POINTER(ctypes.c_int16),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
        ]

        self._reset_model = clf_lib.kb_reset_model
        self._reset_model.argtypes = [ctypes.c_int]
        self._reset_model.restype = ctypes.c_int

        # self._print_model_map = clf_lib.kb_print_model_map

        # self._print_model_result = clf_lib.kb_print_model_result
        # self._print_model_result.argtypes = [ctypes.c_int, ctypes.c_int]

        # self._print_model_score = clf_lib.kb_print_model_score
        # self._print_model_score.argtypes = [ctypes.c_int]
        # self._print_model_score.restype = ctypes.c_int

        # self._score_model = clf_lib.kb_score_model
        # self._score_model.argtypes = [ctypes.c_int, ctypes.c_uint16]
        # self._score_model.restype = ctypes.c_int

        # self._retrain_model = clf_lib.kb_retrain_model
        # self._retrain_model.argtypes = [ctypes.c_int]
        # self._retrain_model.restype = ctypes.c_int

        if hasattr(clf_lib, "kb_flush_model_buffer"):
            self._flush_model_buffer = clf_lib.kb_flush_model_buffer
            self._flush_model_buffer.argtypes = [ctypes.c_int]
            self._flush_model_buffer.restype = ctypes.c_int
        else:
            self._flush_model_buffer = dummy_function

        self._add_last_pattern_to_model = clf_lib.kb_add_last_pattern_to_model
        self._add_last_pattern_to_model.argtypes = [
            ctypes.c_int,
            ctypes.c_uint16,
            ctypes.c_uint16,
        ]
        self._add_last_pattern_to_model.restype = ctypes.c_int

        self._add_custom_pattern_to_model = clf_lib.kb_add_custom_pattern_to_model
        self._add_custom_pattern_to_model.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_uint8),
            ctypes.c_uint16,
            ctypes.c_uint16,
        ]
        self._add_custom_pattern_to_model.restype = ctypes.c_int

        # self._print_model_class_map = clf_lib.kb_print_model_class_map
        # self._print_model_class_map.argtypes = [ctypes.c_int, ctypes.c_char_p]

        self._get_model_header = clf_lib.kb_get_model_header
        self._get_model_header.argtypes = [
            ctypes.c_int,
            ctypes.POINTER(struct_pme_model_header),
        ]
        self._get_model_header.restype = ctypes.c_int

        self._get_model_pattern = clf_lib.kb_get_model_pattern
        self._get_model_pattern.argtypes = [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(struct_pme_pattern),
        ]
        self._get_model_pattern.restype = ctypes.c_int

        self._flush_model = clf_lib.kb_flush_model_buffer
        self._flush_model.argtypes = [ctypes.c_int]
        self._flush_model.restype = ctypes.c_int

        try:
            self._get_feature_vector = clf_lib.kb_get_feature_vector
            self._get_feature_vector.argtypes = [
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_uint8),
                ctypes.POINTER(ctypes.c_uint8),
            ]
        except:
            self._get_feature_vector = empty_function

        try:
            self._get_feature_vector = clf_lib.kb_get_feature_vector
            self._get_feature_vector.argtypes = [
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_uint8),
                ctypes.POINTER(ctypes.c_uint8),
            ]
        except:
            self._get_feature_vector = empty_function

        try:
            self._set_feature_vector = clf_lib.kb_set_feature_vector
            self._set_feature_vector.argtypes = [
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_uint8),
            ]
        except:
            self._set_feature_vector = empty_function

        try:
            self._set_feature_vector = clf_lib.kb_set_feature_vector
            self._set_feature_vector.argtypes = [
                ctypes.c_int,
                ctypes.POINTER(ctypes.c_uint8),
            ]
            self._set_feature_vector.restype = ctypes.c_int
        except:
            self._set_feature_vector = empty_function

        try:
            self._recognize_feature_vector = clf_lib.kb_recognize_feature_vector
            self._recognize_feature_vector.argtypes = [ctypes.c_int]
            self._recognize_feature_vector.restype = ctypes.c_uint16
        except:
            self._recognize_feature_vector = empty_function

        try:
            self._classification_result_info = clf_lib.kb_classification_result_info
            self._classification_result_info.argtypes = [
                ctypes.c_int,
                ctypes.POINTER(struct_tf_micro_model_result),
            ]
            self._classification_result_info.restype = ctypes.c_int
        except:
            self._classification_result_info = empty_function

    def _initialized(self):
        if os.name == "nt":
            print("SML Runner is not supported on Windows OS.")
            return None

        if not self._model_initialized:
            print("Initialize the model before running this function")
            return None

        return True

    def _run_with(self, run_type):
        if self._run_type is None:
            self._run_type = run_type

        if self._run_type != run_type:
            print(
                "This model has already been run with {}. You will need to restart your kernal to run in this mode.".format(
                    self._run_type
                )
            )
            return False

        return True

    def init_model(self):
        """
        This will initialize the parameters of all the models, it should be run once before
        running anything elese.
        """
        if not self._model_initialized:
            self._model_initialized = True
            self._model_init()

    def flush_model_buffer(self, model_index):
        """
        This will flush the data buffer of a knowledge pack.
        """
        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)

        self._flush_model_buffer(model_index_ctype)

    def add_custom_pattern_to_model(self, model_index, feature_vector, category, aif):
        """
        updates the model by adding the a new pattern to the database
        with a new category and influence field

        Args:
           model_index(int): Index of the model to update
           feature_vector(list): List of uint8 values that will be added to the database
           category(uint16): category of the vector to add
           aif(uint16): weight function for the new pattern

         Returns:
             int: 0 if model does not support dynamic updates
                  -1 if model can not be updated anymore
                  1 if model was succesfully updated
        """

        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)
        category_ctype = ctypes.c_uint16(category)
        aif_ctype = ctypes.c_uint16(aif)

        feature_vector_array = (ctypes.c_uint8 * len(feature_vector))()

        for index, value in enumerate(feature_vector):
            feature_vector_array[index] = ctypes.c_uint8(value)

        return self._add_custom_pattern_to_model(
            model_index_ctype, feature_vector_array, category_ctype, aif_ctype
        )

    def add_last_pattern_to_model(self, model_index, category, aif):
        """
        Updates the model by adding the a the last feature vector created to the database
        with a new category and influence field

        Args:
           model_index(int): Index of the model to update
           category(uint16): category of the vector to add
           aif(uint16): weight function for the new pattern

         Returns:
             int: 0 if model does not support dynamic updates
                  -1 if model can not be updated anymore
                  1 if model was succesfully updated
        """

        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)
        category_ctype = ctypes.c_uint16(category)
        aif_ctype = ctypes.c_uint16(aif)

        return self._add_last_pattern_to_model(
            model_index_ctype, category_ctype, aif_ctype
        )

    def score_model(self, model_index, category, silent=False):
        """
        Given the ground truth of the current feature vector, this will score the model
        internally

        Args:
           model_index(int): Index of the model to update
           category(uint16): category of the vector to add

        Returns:
           int: 0 if model does not support dynamic scoring
                -1 if model can not be scored
                1 if model was succesfully scored
        """
        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)
        category_ctype = ctypes.c_uint16(category)

        res = None
        with pipes() as (out, _):
            res = self._score_model(model_index_ctype, category_ctype)

        if silent:
            print(out.read())

        return res

    def retrain_model(self, model_index):
        """
        After a model has been scored, this will retraing the model according
        to the models supported reinforcment learning approach

        Args:
           model_index(int): Index of the model to update

        Returns:
           int: 0 if model does not support dynamic scoring
                1 if model was succesfully scored
        """
        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)

        ret = self._retrain_model(model_index_ctype)

        if ret == 0:
            print("Retraining is not supported/enabled for this model.")

        return ret

    def run_model(self, data_sample, model_index, debug_log=False):
        """
        This is the main entry point into the pipeline. It takes a single timepoint of data as an array. Adds that sample to the internal ring buffer
        checks for a segment, generates features if there is a segment,
        produces a classification and returns the result.

        Args:
            data_sample(array):  single timepoint of data as an array from all sensors
            nsensors(int): unused
            model_index(int): Index of the model to run
            debug_log(bool): Prints the debug output from the knowledge pack

         Returns:
             Classification results will be 0 if unkown through the classification numbers
                 you have. This function returns -1 when a segment hasn't yet been identified.

        """
        if not self._initialized():
            return

        if self._run_with("run_model") is False:
            return

        if isinstance(data_sample, DataFrame) or isinstance(data_sample, Series):
            data = data_sample.values
        elif isinstance(data_sample, ndarray):
            data = data_sample
        else:
            print("Input data Must be either dataframe or array.")
            return

        data_array = (ctypes.c_int16 * data.shape[0])()
        nsensors_ctype = ctypes.c_int(0)
        model_index_ctype = ctypes.c_int(model_index)

        for index, value in enumerate(data):
            data_array[index] = ctypes.c_int16(value)

        with pipes() as (out, _):
            ret = self._run_model(data_array, nsensors_ctype, model_index_ctype)

        if debug_log:
            print(out.read())

        return ret

    def run_segment(self, data_segment, model_index, debug_log=False):
        """
        Add a segment of data to the model as input. Then runs the model on the current segment, skipping the data streaming steps.

        (Warning: using this call will flush the models internal ring buffer. Alternating between this and run_and_score model may produce incorrect results or crashes)

        Args:
            data(array):  Array of timseries data
            model_index(int): Index of the model to run
            debug_log(bool): Prints the debug output from the knowledge pack

         Returns:
             Classification results will be 0 if unkown through the classification numbers
                 you have. This function returns -1 when a segment hasn't yet been identified.

        """
        if not self._initialized():
            return

        if self._run_with("run_segment") is False:
            return

        if isinstance(data_segment, (DataFrame, Series)):
            data = data_segment.values
        elif isinstance(data_segment, ndarray):
            data = data_segment
        else:
            print("Input data Must be either dataframe or array.")
            return

        data_array = (ctypes.c_int16 * (data.shape[0] * data.shape[1]))()
        length_ctype = ctypes.c_int(data.shape[0])
        nbuffs = ctypes.c_int(data.shape[1])
        model_index_ctype = ctypes.c_int(model_index)

        for col in range(data.shape[1]):
            for index, value in enumerate(data[:, col]):
                data_array[col * data.shape[0] + index] = ctypes.c_int16(value)

        self._add_segment(data_array, length_ctype, nbuffs, model_index_ctype)

        model_index_ctype = ctypes.c_int(model_index)

        with pipes() as (out, _):

            ret = self._run_segment(model_index_ctype)

        if debug_log:
            print(out.read())

        return ret

    def reset_model(self, model_index):
        """
        Advances the model state to so that it is ready for a more input data. Use
        only after classification steps.

        (Note: this does not reset the model to a clean state, only init_model does this)


        Args:
           model_index(int): Index of the model to update
        """

        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)

        self._reset_model(model_index_ctype)

    def flush_model(self, model_index):
        """
        Deletes all of the patterns in the database.

        Args:
           model_index(int): Index of the model to update
        """

        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)

        self._flush_model(model_index_ctype)

    def get_model_map(self):
        """
        Print the model name to map relationship
        """
        print("not currently supported.")

        return

        with pipes() as (out, _):
            self._print_model_map()

        return json.loads(out.read())

    def get_model_result(self, model_index, result):
        """ """

        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)
        result_ctype = ctypes.c_int(result)

        with pipes() as (out, _):
            self._print_model_result(model_index_ctype, result_ctype)

        return json.loads(out.read())

    def get_model(self, model_index):
        """
        Prints the model weights and info for current model if supported

        Args:
            model index - number of axes in the data stream

        """

        if not self._initialized():
            return

        model_header = self.get_model_header(model_index)
        model = []

        for index in range(model_header.number_patterns):
            tmp_dict = {}
            pattern = self.get_model_pattern(model_index, index)
            tmp_dict["Category"] = pattern.category
            tmp_dict["Vector"] = [
                pattern.vector[i] for i in range(model_header.pattern_length)
            ]
            tmp_dict["AIF"] = pattern.influence
            tmp_dict["Identifier"] = index
            model.append(tmp_dict)

        return DataFrame(model)

    def get_model_score(self, model_index):

        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)

        with pipes() as (out, _):
            self._print_model_score(model_index_ctype)

        model_scores = []
        for line in out.read().split("\n")[:-1]:
            model_scores.append(json.loads(line))

        cats = [str(x) for x in range(1, len(DataFrame(model_scores).columns) - 1)]

        return DataFrame(model_scores)[["ID", "ERR"] + cats].style.apply(_color, axis=1)

    def get_class_map(self, model_index):

        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)

        with pipes() as (out, _):
            self._print_model_class_map(model_index_ctype, None)

        return json.loads(out.read())

    def get_model_header(self, model_index):

        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)
        pme_model_header = struct_pme_model_header()

        with pipes() as (out, _):
            self._get_model_header(model_index_ctype, pme_model_header)

        return pme_model_header

    def get_model_pattern(self, model_index, pattern_index):

        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)
        pattern_index_ctype = ctypes.c_int(pattern_index)
        pme_pattern = struct_pme_pattern()

        with pipes() as (out, _):
            self._get_model_pattern(model_index_ctype, pattern_index_ctype, pme_pattern)

        return pme_pattern

    def get_feature_vector(self, model_index, feature_vector_buffer_size=256):

        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)
        feature_vector_ctype = (ctypes.c_ubyte * feature_vector_buffer_size)()
        feature_length_ctype = ctypes.c_ubyte(0)

        self._get_feature_vector(
            model_index_ctype, feature_vector_ctype, ctypes.byref(feature_length_ctype)
        )

        return list(feature_vector_ctype[: feature_length_ctype.value])

    def set_feature_vector(self, model_index, feature_vector):
        """
        set a model buffers feature vector
        """

        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)
        feature_vector_array = (ctypes.c_ubyte * len(feature_vector))()

        for index, value in enumerate(feature_vector):
            feature_vector_array[index] = ctypes.c_ubyte(value)

        return self._set_feature_vector(model_index_ctype, feature_vector_array)

    def recognize_feature_vector(self, model_index):
        """
        classify the feature vector that is currently in the model buffer
        """

        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)

        return self._recognize_feature_vector(model_index_ctype)

    def get_model_result_detail_view(self, model_index):
        """
        classify the feature vector that is currently in the model buffer
        """

        if not self._initialized():
            return

        model_index_ctype = ctypes.c_int(model_index)
        model_result = struct_tf_micro_model_result()
        output_tensor = (ctypes.c_float * 128)()
        model_result.output_tensor = ctypes.POINTER(output_tensor)

        self._classification_result_info(model_index_ctype, model_result)

        return model_result

    def knowledgepack(self, model_index, distance_mode=0, feature_list=None):
        """
        Turn into a knowledgepack Model Object (Only works for PME)
        """
        self.init_model()
        neuron_array = self.get_model(model_index).to_dict("records")
        class_map = self.get_class_map(model_index)

        return Model(
            neuron_array,
            class_map,
            {"distance_mode": distance_mode},
            feature_summary=feature_list,
        )

    def run_and_score_model(self, data_sample, category, model_index=0):
        """
        Will Run ans core a model based on passing a single sample at a time.

        """

        ret = self.run_model(data_sample, model_index)

        if ret is None:
            return

        if ret >= 0:
            print("Class: {}".format(ret))
            if ret > 0:  # only retrain if greater than 0
                score_ret = self.score_model(model_index, category)
                if score_ret == 0:
                    print("Retraining is not supported for this model.")
            self.reset_model(model_index)

            return self.get_model_score(model_index)

        return -1

    def run_and_score_model_on_segment(self, segment, category, model_index=0):
        """
        will run and score a model based on a segment of data.

        (Warning: using this call will flush the models internal ring buffer. Alternating between this and run_and_score model may produce incorrect results or crashes)

        """

        ret = self.run_segment(segment, model_index)

        if ret is None:
            return

        if ret >= 0:
            print("Class: {}".format(ret))
            if ret > 0:  # only retrain if greater than 0
                self.score_model(model_index, category)
            self.reset_model(model_index)

        return self.get_model_score(model_index)


def _color(val):
    color = "white"
    if val.ERR > 0:
        color = "#90ee90"
    elif val.ERR < 0:
        color = "red"
    return ["background-color: %s" % color] * len(val)
