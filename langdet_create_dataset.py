"""
This program detects the language of documents,
here the dataset is created as a comparison for detecting languages
"""

from my_lib.configuration_handler import ConfigurationHandler
from my_lib.conditional_print import ConditionalPrint
from my_lib.text_file_loader import TextFileLoader
from my_lib.langdet.SpatialLanguageIdentificator import SpatialLanguageIdentificator
import os
import re

CODED_CONFIGURATION_PATH = './configurations/language_detector.conf'
config_handler = ConfigurationHandler(first_init=True, fill_unkown_args=True,\
                                      coded_configuration_paths=[CODED_CONFIGURATION_PATH])
config = config_handler.get_config()
cpr = ConditionalPrint(config.PRINT_MAIN, config.PRINT_EXCEPTION_LEVEL, config.PRINT_WARNING_LEVEL,
                       leading_tag="langdet_create_dataset")


# make sure the tags in this list correspond to the folder names for languages in your io_data
selected_datasets = ["de", "en", "fr", "th", "sp"]

# initialize classes and variables for later usage
text_file_loader = TextFileLoader()


def preprocess_bible_text_file(text, language_code):
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


# go through all selected datasets
for folder_addition in selected_datasets:

    language_set_path = os.path.join(config.DATASETS_BASE_PATH, folder_addition)
    # initialize spatial language identificator for this set
    current_sli = SpatialLanguageIdentificator(language_set_path, folder_addition)
    # iterate set and fill the identificator
    cpr.print("processing folder:", language_set_path)
    all_files_in_path = os.listdir(language_set_path)
    for file_index, file in enumerate(all_files_in_path):
        # if file_index >= 10: break      # debugging condition
        if file.endswith(".txt"):
            if "000_000_000" in file:
                # skip the start file with only comments
                continue
            else:
                cpr.print("processing file:", file)
                # obtain complete file path
                file_path = os.path.join(language_set_path, file)
                # get text from the file
                text = text_file_loader.load_txt_text(file_path, "utf-8")
                # pre-process text  (change pre-processing function if other content)
                preprocessed_text = preprocess_bible_text_file(text, folder_addition)
                # tokenize the text
                tokenized_text = tokenize_text(preprocessed_text)
                # update the current spatial language identificator
                current_sli.update_spatial_language_identificator(tokenized_text)
                cpr.print("done processing file")

    # sort keys alphabetically
    current_sli.sort_spatial_language_identificator()
    print(current_sli)
    # plot_spatial_language_identificator()
    # save the filled spatial language identificator
    current_sli.save_spatial_language_identificator(config.IO_BASE_PATH)
