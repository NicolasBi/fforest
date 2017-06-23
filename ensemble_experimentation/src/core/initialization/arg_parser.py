""" This module contains all functions related to parsing command-line arguments for all entry points of the package.
It uses the `docopt` package (listed as a dependencie) to easily combine the tedious task of writing documentation
and parsing arguments.
#TODO: We can gain time by not formatting the helping message twice, but by directly formatting the documentation from
#      the format dictionary
"""
import docopt

import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_default_value as gdv
import ensemble_experimentation.src.getters.get_global_variable as ggv
import ensemble_experimentation.src.getters.get_parameter_documentation as gpd
import ensemble_experimentation.src.getters.get_parameter_name as gpn
import ensemble_experimentation.src.getters.get_statistic_name as gsn
from ensemble_experimentation.src.core.initialization.arg_cleaner import clean_args
from ensemble_experimentation.src.vrac.file_system import get_filename

_FORMAT_DICTIONARY = dict(
    # Documentation
    doc_usage=gpd.usage(),
    doc_training_value=gpd.training_value(),
    doc_reference_value=gpd.reference_value(),
    doc_trees_in_forest=gpd.trees_in_forest(),
    doc_initial_split_method=gpd.initial_split_method(),
    doc_reference_split_method=gpd.reference_split_method(),
    doc_subsubtrain_split_method=gpd.subsubtrain_split_method(),
    doc_train_name=gpd.train_name(),
    doc_test_name=gpd.test_name(),
    doc_preprocessed_db_name=gpd.preprocessed_database_name(),
    doc_subtrain_name=gpd.subtrain_name(),
    doc_reference_name=gpd.reference_name(),
    doc_subsubtrain_name_pattern=gpd.subsubtrain_name_pattern(),
    doc_statistics_name=gpd.statistics_file_name(),
    doc_header_name=gpd.header_name(),
    doc_tree_file_extension=gpd.tree_file_extension(),
    doc_vector_file_extension=gpd.vector_file_extension(),
    doc_header_extension=gpd.header_extension(),
    doc_difficulty_vector_prefix=gpd.difficulty_vector_prefix(),
    doc_quality_vector_prefix=gpd.quality_vector_prefix(),
    doc_main_directory=gpd.main_directory(),
    doc_subtrain_directory=gpd.subtrain_directory(),
    doc_subsubtrain_directory_pattern=gpd.subsubtrain_directory_pattern(),
    doc_discretization_threshold=gpd.discretization_threshold(),
    doc_entropy_threshold=gpd.entropy_threshold(),
    doc_min_size_leaf=gpd.min_size_leaf(),
    doc_entropy_measure=gpd.entropy_measure(),
    doc_number_of_tnorms=gpd.number_of_tnorms(),
    doc_help=gpd.help_doc(),
    doc_identifier=gpd.identifier(),
    doc_class_name=gpd.class_name(),
    doc_have_header=gpd.have_header(),
    doc_encoding_input=gpd.encoding_input(),
    doc_encoding_output=gpd.encoding_output(),
    doc_format_input=gpd.format_input(),
    doc_format_output=gpd.format_output(),
    doc_delimiter_input=gpd.delimiter_input(),
    doc_delimiter_output=gpd.delimiter_output(),
    doc_quoting_input=gpd.quoting_input(),
    doc_quoting_output=gpd.quoting_output(),
    doc_quote_char_input=gpd.quote_char_input(),
    doc_quote_char_output=gpd.quote_char_output(),

    # Parameters
    param_database=gpn.database(),
    param_training_value=gpn.training_value(),
    param_reference_value=gpn.reference_value(),
    param_trees_in_forest=gpn.trees_in_forest(),
    param_initial_split_method=gpn.initial_split_method(),
    param_reference_split_method=gpn.reference_split_method(),
    param_subsubtrain_split_method=gpn.subsubtrain_split_method(),
    param_train_name=gpn.train_name(),
    param_test_name=gpn.test_name(),
    param_preprocessed_db_name=gpn.preprocessed_database_name(),
    param_subtrain_name=gpn.subtrain_name(),
    param_reference_name=gpn.reference_name(),
    param_subsubtrain_name_pattern=gpn.subsubtrain_name_pattern(),
    param_statistics_name=gpn.statistics_file_name(),
    param_header_name=gpn.header_name(),
    param_tree_file_extension=gpn.tree_file_extension(),
    param_vector_file_extension=gpn.vector_file_extension(),
    param_header_extension=gpn.header_extension(),
    param_difficulty_vector_prefix=gpn.difficulty_vector_prefix(),
    param_quality_vector_prefix=gpn.quality_vector_prefix(),
    param_main_directory=gpn.main_directory(),
    param_subtrain_directory=gpn.subtrain_directory(),
    param_subsubtrain_directory_pattern=gpn.subsubtrain_directory_pattern(),
    param_discretization_threshold=gpn.discretization_threshold(),
    param_entropy_threshold=gpn.entropy_threshold(),
    param_min_size_leaf=gpn.min_size_leaf(),
    param_entropy_measure=gpn.entropy_measure(),
    param_number_of_tnorms=gpn.number_of_tnorms(),
    param_help=gpn.help_param(),
    param_identifier=gpn.identifier(),
    param_class_name=gpn.class_name(),
    param_have_header=gpn.have_header(),
    param_encoding_input=gpn.encoding_input(),
    param_encoding_output=gpn.encoding_output(),
    param_format_input=gpn.format_input(),
    param_format_output=gpn.format_output(),
    param_delimiter_input=gpn.delimiter_input(),
    param_delimiter_output=gpn.delimiter_output(),
    param_quoting_input=gpn.quoting_input(),
    param_quoting_output=gpn.quoting_output(),
    param_quote_char_input=gpn.quote_char_input(),
    param_quote_char_output=gpn.quote_char_output(),

    # Default values
    default_training_value=gdv.training_value(),
    default_reference_value=gdv.reference_value(),
    default_trees_in_forest=gdv.trees_in_forest(),
    default_initial_split_method=gdv.initial_split_method(),
    default_reference_split_method=gdv.reference_split_method(),
    default_subsubtrain_split_method=gdv.subsubtrain_split_method(),
    default_train_name=gdv.train_name(),
    default_test_name=gdv.test_name(),
    default_subtrain_name=gdv.subtrain_name(),
    default_reference_name=gdv.reference_name(),
    default_subsubtrain_name_pattern=gdv.subsubtrain_name_pattern(),
    default_statistics_name=gdv.statistics_file_name(),
    default_header_name=gdv.header_name(),
    default_tree_file_extension=gdv.tree_file_extension(),
    default_vector_file_extension=gdv.vector_file_extension(),
    default_header_extension=gdv.header_extension(),
    default_difficulty_vector_prefix=gdv.difficulty_vector_prefix(),
    default_quality_vector_prefix=gdv.quality_vector_prefix(),
    default_subtrain_directory=gdv.subtrain_directory(),
    default_subsubtrain_directory_pattern=gdv.subsubtrain_directory_pattern(),
    default_discretization_threshold=gdv.discretization_threshold(),
    default_entropy_threshold=gdv.entropy_threshold(),
    default_min_size_leaf=gdv.min_size_leaf(),
    default_entropy_measure=gdv.entropy_measure(),
    default_number_of_tnorms=gdv.number_of_tnorms(),
    default_identifier=gdv.identifier(),
    default_encoding_input=gdv.encoding_input(),
    default_encoding_output=gdv.encoding_output(),
    default_format_input=gdv.format_input(),
    default_format_output=gdv.format_output(),
    default_delimiter_input=gdv.delimiter_input(),
    default_delimiter_output=gdv.delimiter_output(),
    default_quoting_input=gdv.quoting_input(),
    default_quoting_output=gdv.quoting_output(),
    default_quote_char_input=gdv.quote_char_input(),
    default_quote_char_output=gdv.quote_char_output(),

    # Miscellaneous
    global_name=ggv.name()
)


def _init_statistics(args: dict) -> None:
    """ Initialize the `statistics` dictionary located inside the `env` module. """
    env.statistics[gsn.database_path()] = args[gpn.database()]
    env.statistics[gsn.database_name()] = get_filename(args[gpn.database()])
    env.statistics[gsn.preprocessed_database_path()] = "{}/{}".format(args[gpn.main_directory()],
                                                                      args[gpn.preprocessed_database_name()])
    env.statistics[gsn.train_path()] = "{}/{}".format(args[gpn.main_directory()], args[gpn.train_name()])
    env.statistics[gsn.test_path()] = "{}/{}".format(args[gpn.main_directory()], args[gpn.test_name()])
    env.statistics[gsn.subtrain_path()] = "{}/{}/{}".format(args[gpn.main_directory()], args[gpn.subtrain_directory()],
                                                            args[gpn.subtrain_name()])
    env.statistics[gsn.reference_path()] = "{}/{}/{}".format(args[gpn.main_directory()], args[gpn.subtrain_directory()],
                                                             args[gpn.reference_name()])


def parse_args_main_entry_point() -> None:
    global _FORMAT_DICTIONARY

    documentation = """{global_name}

Usage:
  {doc_usage}

Options:
  # Splitting values
  {param_training_value}=VALUE                {doc_training_value}
  {param_reference_value}=VALUE               {doc_reference_value}
  {param_trees_in_forest}=VALUE               {doc_trees_in_forest}

  # Splitting methods
  {param_initial_split_method}=METHOD         {doc_initial_split_method}
  {param_reference_split_method}=METHOD       {doc_reference_split_method}
  {param_subsubtrain_split_method}=METHOD     {doc_subsubtrain_split_method}

  # File names
  {param_train_name}=NAME                     {doc_train_name}
  {param_test_name}=NAME                      {doc_test_name}
  {param_preprocessed_db_name}=NAME           {doc_preprocessed_db_name}
  {param_subtrain_name}=NAME                  {doc_subtrain_name}
  {param_reference_name}=NAME                 {doc_reference_name}
  {param_statistics_name}=NAME                {doc_statistics_name}
  {param_header_name}=NAME                    {doc_header_name}
  {param_subsubtrain_name_pattern}=NAME       {doc_subsubtrain_name_pattern}
  {param_difficulty_vector_prefix}=PREFIX     {doc_difficulty_vector_prefix}
  {param_quality_vector_prefix}=PREFIX        {doc_quality_vector_prefix}
  {param_tree_file_extension}=NAME            {doc_tree_file_extension}
  {param_vector_file_extension}=NAME          {doc_vector_file_extension}
  {param_header_extension}=NAME               {doc_header_extension}

  # Directories names
  {param_main_directory}=NAME                 {doc_main_directory}
  {param_subtrain_directory}=NAME             {doc_subtrain_directory}
  {param_subsubtrain_directory_pattern}=NAME  {doc_subsubtrain_directory_pattern}
  
  # Salammbô parameters
  {param_discretization_threshold}=VALUE      {doc_discretization_threshold}
  {param_entropy_threshold}=VALUE             {doc_entropy_threshold}
  {param_min_size_leaf}=SIZE                  {doc_min_size_leaf}
  {param_entropy_measure}=<measure>             {doc_entropy_measure}
  {param_number_of_tnorms}=INT                {doc_number_of_tnorms}

  # Miscellaneous
  {param_help}                                  {doc_help}
  {param_identifier}=ID                      {doc_identifier}
  {param_class_name}=NAME                     {doc_class_name}
  {param_have_header}                           {doc_have_header}
  {param_encoding_input}=ENCODING                  {doc_encoding_input}
  {param_encoding_output}=ENCODING                  {doc_encoding_output}
  {param_format_input}=FORMAT                    {doc_format_input}
  {param_format_output}=FORMAT                    {doc_format_output}
  {param_delimiter_input}=CHAR                      {doc_delimiter_input}
  {param_delimiter_output}=CHAR                      {doc_delimiter_output}
  {param_quoting_input}=QUOTING                     {doc_quoting_input}
  {param_quoting_output}=QUOTING                     {doc_quoting_output}
  {param_quote_char_input}=CHAR                     {doc_quote_char_input}
  {param_quote_char_output}=CHAR                     {doc_quote_char_output}
""".format(**_FORMAT_DICTIONARY).format(**_FORMAT_DICTIONARY)

    arguments = docopt.docopt(documentation, version=ggv.version(), help=True)
    print(arguments)
    cleaned_arguments = clean_args(arguments)
    print(arguments)
    env.arguments = arguments
    env.cleaned_arguments = cleaned_arguments

    _init_statistics(cleaned_arguments)


def parse_args_forest_entry_point() -> dict:
    pass


def parse_args_forest_reduction_entry_point() -> dict:
    pass


if __name__ == "__main__":
    pass
