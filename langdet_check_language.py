"""
This program detects the language of documents
"""

from my_lib.configuration_handler import ConfigurationHandler
from my_lib.conditional_print import ConditionalPrint
from my_lib.text_file_loader import TextFileLoader
from my_lib.langdet.SpatialLanguageIdentificator import SpatialLanguageIdentificator, ComparatorSLI
import re
import os

CODED_CONFIGURATION_PATH = './configurations/language_detector.conf'
config_handler = ConfigurationHandler(first_init=True, fill_unkown_args=True,\
                                      coded_configuration_paths=[CODED_CONFIGURATION_PATH])
config = config_handler.get_config()
cpr = ConditionalPrint(config.PRINT_MAIN, config.PRINT_EXCEPTION_LEVEL, config.PRINT_WARNING_LEVEL,
                       leading_tag="main")


# Take bibles as learn in test data ( here's a good source for other languages)
# en http://www.bibleprotector.com/TEXT-PCE-127.txt  king james version
# en https://ebible.org/find/details.php?id=eng-kjv2006 king james version used (cause format similar)
# de https://info2.sermon-online.com/german/MartinLuther-1912/Martin_Luther_Uebersetzung_1912.txt  luther version
# de https://ebible.org/find/details.php?id=deu1912 luther version used
# fr https://ebible.org/find/details.php?id=fraLSG loius segond bible equivalent to king james
# th https://ebible.org/find/details.php?id=thaKJV  thai king james version

# load dataset spatial language identificators saved through 'langdet_create_dataset'
# make sure the tags in this list correspond to the folder names for languages in your io_data
selected_datasets = ["de", "en", "fr", "sp", "th"]

identifiers_loaded = []
for lang_code in selected_datasets:
    current_sli = SpatialLanguageIdentificator.load_spatial_language_identificator(config.IO_BASE_PATH, lang_code)
    current_sli.normalize_spatial_language_identificator()  # create normalized sli
    identifiers_loaded.append(current_sli)

# create SLI comparator for later distance calculations
sli_comparator = ComparatorSLI()

# text_file_loader
text_file_loader = TextFileLoader()

# get list of input files
all_input_files_in_path = os.listdir(config.INPUT_FILE_FOLDER_PATH)
all_input_complete_paths = []
for file in all_input_files_in_path:
    path_complete = os.path.join(config.INPUT_FILE_FOLDER_PATH, file)
    all_input_complete_paths.append(path_complete)

specific_input_file_path = config.INPUT_FILE_PATH
combined_files_list = [specific_input_file_path]
combined_files_list.extend(all_input_complete_paths)


def preprocess_input_text(text): # very similar to the method in create_dataset
    text_list = text.split('\n')

    if len(text_list) >= 2:
        text_list_new = text_list[2:]  # remove first two lines, cause they contain chapter header
    else:
        text_list_new = text_list

    # join list again to string
    text_joined = "".join(text_list_new)

    # text_joined = text_joined.lower() # capitalization should be a good for identification, commented out
    return text_joined


def tokenize_text(preprocessed_text):
    # tokenized_text = preprocessed_text.split(" ")
    tokenized_text = re.split('\s|-', preprocessed_text)  # split at spaces and dashes
    return tokenized_text

def process_a_file(file_path):

    # determine input file format
    format = text_file_loader.check_file_format(file_path)

    input_text = ""
    # get text from file
    if format.is_pdf:
        input_text, pdf_metadata = text_file_loader.load_pdf_text(file_path)
    elif format.is_txt:
        input_text = text_file_loader.load_txt_text(file_path)



    # preprocessing steps for the given input
    p_input_text = preprocess_input_text(input_text)
    tokenized_text = tokenize_text(p_input_text)

    # create an sli for the input
    input_sli = SpatialLanguageIdentificator(file_path, "input")
    input_sli.update_spatial_language_identificator(tokenized_text)
    input_sli.sort_spatial_language_identificator()
    input_sli.normalize_spatial_language_identificator()

    results = dict()
    for identifier in identifiers_loaded:
        distance_matrix, distance = sli_comparator.compare_slis(input_sli, identifier, print_output=False)
        results[identifier.language_code] = distance

    # normalize results
    maximum_distance = max(results.values())
    results_normalized = dict()
    for key in results:
        result = results[key]
        result_normalized = result / maximum_distance
        result_normalized = 100 - (result_normalized * 100)
        results_normalized[key] = result_normalized
        # cpr.print(key, "\t", result, result_normalized)


    # sort after normalized results and print the result
    sorted_results_normalized = sorted(results_normalized.items(), key=lambda kv: kv[1])
    sorted_results_normalized.reverse()

    # print results
    print("Results______________________________________________________")

    print("{0:<10} {1:<25}".format("Input:", input_sli.base_path))
    print("{0:<10} {1:<25}".format("Det. lang:", sorted_results_normalized[0][0]))

    print("_____________________________________________________________")
    # print headline
    print("{0:<10} {1:<25} {2:<25}".format("language", "distance", "likeliness"))

    # print results comparison table
    for key, holder in sorted_results_normalized:
        result = results[key]
        result_normalized = results_normalized[key]
        # cpr.print(key, "\t", result, result_normalized)
        print("{0:<10} {1:<25} {2:<25}".format(key, result, result_normalized))

    print("")
    print("")
# iterate through the files list and calculate results for each file
for file_path in combined_files_list:
    process_a_file(file_path)
cpr.print("done")
