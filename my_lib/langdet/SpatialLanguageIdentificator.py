"""
This class holds data for the spatial language identificator
and provides methods for usage
"""

import pickle
import os


class ComparatorSLI(object):
    """
    Mostly creates distances in between SLI's
    """

    def __init__(self):
        print("SLI Comparator initialized")
    @staticmethod
    def distance_comparison(row_a, row_b):
        distances_in_row = []
        accumulated_distance = 0
        for row_index, value_a in enumerate(row_a):
            value_b = row_b[row_index]
            dist = abs(value_a - value_b)
            distances_in_row.append(dist)
            accumulated_distance += dist
        return distances_in_row, accumulated_distance

    @staticmethod
    def distance_comparison_zerovec(row_a):
        distances_in_row = []
        accumulated_distance = 0
        for row_index, value_a in enumerate(row_a):
            dist = abs(value_a)
            distances_in_row.append(dist)
            accumulated_distance += dist
        return distances_in_row, accumulated_distance

    def compare_slis(self, sli_a, sli_b,print_output=False):
        if print_output:
            print("comparing slis:", sli_a.language_code, "to", sli_b.language_code)
        distances_matrix = dict()
        accumulated_distance = 0
        # check dimensions
        if sli_a.x_dimension != sli_b.x_dimension:
            print("Warning dimensions not compatible")

        # cast to lists cause processing later
        keys_a_holder = list(sli_a.sli_normalized.keys())
        keys_b_holder = list(sli_b.sli_normalized.keys())

        # go through all keys in keys_a
        for key in sli_a.sli_normalized.keys():
            if key in sli_b.sli_normalized.keys():
                # keys are both found in a and b
                keys_a_holder.remove(key)     # remove the key from check amount for second run
                keys_b_holder.remove(key)     # remove the key from check amount for second run
                # make distance comparison
                distance_row, distance_number = self.distance_comparison(sli_a.sli_normalized[key],
                                                                         sli_b.sli_normalized[key])
                distances_matrix[key] = distance_row
                accumulated_distance += distance_number
            else:
                # key only in a, make zero distance comparison
                distance_row, distance_number = self.distance_comparison_zerovec(sli_a.sli_normalized[key])
                distances_matrix[key] = distance_row
                accumulated_distance += distance_number

        # go through all rest keys in keys b
        for key in keys_b_holder:
            # just add distances from zero for this rest keys, key only in b
            distance_row, distance_number = self.distance_comparison_zerovec(sli_b.sli_normalized[key])
            distances_matrix[key] = distance_row
            accumulated_distance += distance_number
        if print_output:
            print("accumulated_distance is", accumulated_distance)
        return distances_matrix, accumulated_distance

class SpatialLanguageIdentificator(object):
    def __init__(self, base_path, language_code):
        self.base_path = base_path
        self.language_code = language_code
        self.sli = dict()
        self.x_dimension = 100  # maximum estimated length of a word
        self.number_of_chars_added = 0  # accumulated number of chars added to this sli
        self.sli_normalized = dict()    # normalized sli counters, only filled if normalization function triggered
        self.normalization_upward_factor = 10000  # a multiplicator for normalization


    def update_spatial_language_identificator(self, tokenized_text):
        for word in tokenized_text:
            characters_in_word = list(word)
            for char_index, char in enumerate(characters_in_word):
                # unicode_ordinal = ord(char) # atm unused

                if char_index >= self.x_dimension:
                    break  # escape inner loop ( a word is longer than x_dimension,-> prevent program crash)

                previous_val = 0
                if char not in self.sli:
                    # initialize zeros list at key -> character
                    start_list = [0] * self.x_dimension  # fast initialization of list with zeros
                    self.sli[char] = start_list
                else:
                    # get the previous value in dictionary at list index
                    previous_val = self.sli[char][char_index]

                # update the value at the correct index -> one more occurence
                incremented_val = previous_val + 1
                self.sli[char][char_index] = incremented_val
                # update the overall element counter
                self.number_of_chars_added += 1

    def sort_spatial_language_identificator(self):
        keys_sorted = sorted(self.sli) # sorts the keys alphabetically
        new_sli = {}
        # update also the values corresponding to keys
        for key in keys_sorted:
            new_sli[key] = self.sli[key]
        # update sli finally
        self.sli = new_sli

    def normalize_spatial_language_identificator(self):
        """
        Normalizes sli, creates a new normalized array, which causes more memory needed
        :return:
        """
        my_sli = self.sli
        normalized_sli = dict()

        for key in my_sli:
            spatial_occurences = my_sli[key]
            new_spatial_occurences = []
            for occurrence in spatial_occurences:
                new_occurence = occurrence / self.number_of_chars_added * self.normalization_upward_factor
                new_spatial_occurences.append(new_occurence)
            normalized_sli[key] = new_spatial_occurences

        self.sli_normalized = normalized_sli



    def get_number_of_used_characters(self):
        return len(self.sli)

    def plot_spatial_language_identificator(self):
        print("tbd plotting")

    def save_spatial_language_identificator(self, io_root):
        """
        serialize the current object to path in io_root with pickle, with langauge_code as identifier
        :param io_root: base path to save sli
        :return:
        """
        # import json
        # print(json.dumps(self))
        save_file_path = os.path.join(io_root, "saved_identifiers", self.language_code+".pickle")
        with open(save_file_path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_spatial_language_identificator(io_root, language_code):
        """
        deserialize the current object to path in io_root with pickle, with langauge_code as identifier,
        works like a factory method
        :param io_root: base path to load sli
        :return: the object
        """
        # import json
        # print(json.dumps(self))
        load_file_path = os.path.join(io_root, "saved_identifiers", language_code+".pickle")
        with open(load_file_path, 'rb') as f:
            loaded_object = pickle.load(f)

        return loaded_object