""" This module will create a "classes matrices" directory, and compute a "class matrix" for each class and for each
triangular norm.
A class matrix depends of a specific class and link one instance to the % of membership a fuzzy tree gave it for this
class.
"""
import os
from typing import List, Dict

import fforest.src.getters.environment as env
from fforest.src.file_tools.csv_tools import get_column, dump_csv_content, get_columns
from fforest.src.file_tools.dialect import Dialect
from fforest.src.vrac.file_system import create_dir

KEY_IDENTIFIER = "ID"


def classes_matrices() -> None:
    _create_directories(classes_matrices_directories=env.classes_matrices_directories_path,
                        possibles_classes=env.possible_classes)

    _compute_classes_matrices(possible_classes=env.possible_classes,
                              tnorms=env.t_norms_names,
                              reference_database_path=env.reference_database_path,
                              classes_matrices_paths=env.classes_matrices_files_paths,
                              forest_paths=env.salammbo_vectors_paths,
                              dialect=env.dialect_output)


def _create_directories(classes_matrices_directories: Dict[str, str], possibles_classes: List[str]) -> None:
    """ Create the directories for the "class matrix" files, and one directory for each class. """
    for class_name in possibles_classes:
        create_dir(classes_matrices_directories[class_name])


def _compute_classes_matrices(possible_classes: List[str], tnorms: List[str], reference_database_path: str,
                              classes_matrices_paths: Dict[str, Dict[str, str]], forest_paths: Dict[str, str],
                              dialect: Dialect) -> None:
    identifiers = get_column(path=reference_database_path,
                             column=0,
                             have_header=False,
                             dialect=dialect)
    for class_name in possible_classes:
        for tnorm in tnorms:
            _compute_class_matrix(class_name=class_name,
                                  tnorm=tnorm,
                                  identifiers=identifiers,
                                  class_matrix_path=classes_matrices_paths[class_name][tnorm],
                                  forest_paths=forest_paths,
                                  dialect=dialect)


def _compute_class_matrix(class_name: str, tnorm: str, identifiers: List[str], class_matrix_path: str,
                          forest_paths: Dict[str, str], dialect: Dialect) -> None:
    global KEY_IDENTIFIER

    content = list()
    matrix = {identifier: list() for identifier in identifiers}

    # Construct header
    content.append([KEY_IDENTIFIER] + [identifier for identifier in identifiers])

    # Construct matrix
    for tree_path in forest_paths[tnorm]:
        columns = get_columns(path=tree_path, columns=[0, class_name], have_header=True, dialect=dialect)
        for identifier, membership in columns:
            matrix[identifier].append(membership)

    # Dump matrix
    for tree_index, tree_path in enumerate(forest_paths[tnorm]):
        content.append([os.path.dirname(tree_path)] + [matrix[identifier][tree_index] for identifier in identifiers])
    dump_csv_content(path=class_matrix_path,
                     content=content,
                     dialect=dialect)
