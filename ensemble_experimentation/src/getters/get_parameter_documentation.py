""" This module defines functions to easily access values stored in the file `parameters_documentation.json`, located
in the `res` folder at the root of the program's package.
This file contains the name of the command-line documentation, which will be parsed by the `docopt` program.

It follows the following strict guidelines:
- All values stored in the files must have its own access function.
- All access functions must have the same name as its respective key in the file. The only exception is a key is named
after a built-in function or variable. In this case, the programmer is free to prepend a word to its access function
name.
- Except for the access functions, this module mustn't have any side effect to the program's namespace nor the files it
tries to access.
"""
import json
import os


_PATH_PARAMS_DOC = "../../res/parameters_documentation.json"


def _get_doc_from_file(value):
    path = os.path.join(os.path.dirname(__file__),
                        _PATH_PARAMS_DOC)
    with open(path) as file:
        return json.load(file)[value]


def usage() -> str:
    return _get_doc_from_file("usage")


def help_doc() -> str:
    return _get_doc_from_file("help")


def training_value() -> str:
    return _get_doc_from_file("training_value")


def reference_value() -> str:
    return _get_doc_from_file("reference_value")


def trees_in_forest() -> str:
    return _get_doc_from_file("trees_in_forest")


def initial_split_method() -> str:
    return _get_doc_from_file("initial_split_method")


def reference_split_method() -> str:
    return _get_doc_from_file("reference_split_method")


def subsubtrain_split_method() -> str:
    return _get_doc_from_file("subsubtrain_split_method")


def train_name() -> str:
    return _get_doc_from_file("train_name")


def test_name() -> str:
    return _get_doc_from_file("test_name")


def preprocessed_database_name() -> str:
    return _get_doc_from_file("preprocessed_database_name")


def subtrain_name() -> str:
    return _get_doc_from_file("subtrain_name")


def reference_name() -> str:
    return _get_doc_from_file("reference_name")


def subsubtrain_name_pattern() -> str:
    return _get_doc_from_file("subsubtrain_name_pattern")


def statistics_file_name() -> str:
    return _get_doc_from_file("statistics_file_name")


def header_name() -> str:
    return _get_doc_from_file("header_name")


def tree_file_extension() -> str:
    return _get_doc_from_file("tree_file_extension")


def vector_file_extension() -> str:
    return _get_doc_from_file("vector_file_extension")


def header_extension() -> str:
    return _get_doc_from_file("header_extension")


def difficulty_vector_prefix() -> str:
    return _get_doc_from_file("difficulty_vector_prefix")


def quality_vector_prefix() -> str:
    return _get_doc_from_file("quality_vector_prefix")


def class_found_vector_prefix() -> str:
    return _get_doc_from_file("class_found_vector_prefix")


def main_directory() -> str:
    return _get_doc_from_file("main_directory")


def subtrain_directory() -> str:
    return _get_doc_from_file("subtrain_directory")


def subsubtrain_directory_pattern() -> str:
    return _get_doc_from_file("subsubtrain_directory_pattern")


def discretization_threshold() -> str:
    return _get_doc_from_file("discretization_threshold")


def entropy_threshold() -> str:
    return _get_doc_from_file("entropy_threshold")


def min_size_leaf() -> str:
    return _get_doc_from_file("min_size_leaf")


def entropy_measure() -> str:
    return _get_doc_from_file("entropy_measure")


def number_of_tnorms() -> str:
    return _get_doc_from_file("number_of_tnorms")


def identifier() -> str:
    return _get_doc_from_file("identifier")


def class_name() -> str:
    return _get_doc_from_file("class")


def have_header() -> str:
    return _get_doc_from_file("have_header")


def encoding_input() -> str:
    return _get_doc_from_file("encoding_input")


def encoding_output() -> str:
    return _get_doc_from_file("encoding_output")


def format_input() -> str:
    return _get_doc_from_file("format_input")


def format_output() -> str:
    return _get_doc_from_file("format_output")


def delimiter_input() -> str:
    return _get_doc_from_file("delimiter_input")


def delimiter_output() -> str:
    return _get_doc_from_file("delimiter_output")


def quoting_input() -> str:
    return _get_doc_from_file("quoting_input")


def quoting_output() -> str:
    return _get_doc_from_file("quoting_output")


def quote_char_input() -> str:
    return _get_doc_from_file("quote_char_input")


def quote_char_output() -> str:
    return _get_doc_from_file("quote_char_output")


def verbosity() -> str:
    return _get_doc_from_file("verbosity")


if __name__ == '__main__':
    pass
