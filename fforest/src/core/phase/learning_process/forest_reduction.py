import csv
from typing import Dict, List

import fforest.src.getters.environment as env
from fforest.src.file_tools.csv_tools import iter_rows, get_header
from fforest.src.vrac.maths import round_float


def forest_reduction() -> None:
    difficulty_vectors = \
        _compute_difficulty_vectors(number_of_trees=env.trees_in_forest,
                                    quality_vectors_dict=env.quality_vectors_paths,
                                    delimiter=env.delimiter_output,
                                    quoting=env.quoting_output,
                                    quote_char=env.quote_character_output,
                                    encoding=env.encoding_output,
                                    line_delimiter=env.line_delimiter_output)

    _dump_difficulty_vectors(difficulty_vectors=difficulty_vectors,
                             difficulty_vectors_paths=env.difficulty_vectors_paths,
                             delimiter=env.delimiter_output,
                             quoting=env.quoting_output,
                             quote_char=env.quote_character_output,
                             encoding=env.encoding_output,
                             line_delimiter=env.line_delimiter_output,
                             skip_initial_space=True)


def _compute_difficulty_vectors(number_of_trees: int, quality_vectors_dict: Dict[str, List], delimiter: str,
                                quoting: int, quote_char: str, encoding: str,
                                line_delimiter: str) -> Dict[str, Dict[str, float]]:
    """ Compute a difficulty vector for each t-norm used. A difficulty vector correspond to the sum of all true class's
    % of membership for all quality vectors. It assign a classification difficulty to an example from the reference
    database.
    """
    difficulty_vectors = dict()
    for tnorm in quality_vectors_dict.keys():
        difficulty_vectors[tnorm] =\
            _compute_difficulty_vector(quality_vectors_paths=quality_vectors_dict[tnorm],
                                       number_of_trees=number_of_trees,
                                       delimiter=delimiter,
                                       quoting=quoting,
                                       quote_char=quote_char,
                                       encoding=encoding,
                                       line_delimiter=line_delimiter)
    return difficulty_vectors


def _compute_difficulty_vector(quality_vectors_paths: List[str], number_of_trees: int, delimiter: str, quoting: int,
                               quote_char: str, encoding: str, line_delimiter: str) -> Dict[str, float]:
    """ Compute a difficulty vector for one t-norm. A difficulty vector correspond to the sum of all true class's % of
    membership for all quality vectors. It assign a classification difficulty to an example from the reference database.
    """
    difficulty_vector = dict()
    for vector_path in quality_vectors_paths:
        quality_vector = _get_quality_vector(vector_path=vector_path,
                                             number_of_trees=number_of_trees,
                                             delimiter=delimiter,
                                             quoting=quoting,
                                             quote_char=quote_char,
                                             line_delimiter=line_delimiter,
                                             encoding=encoding,
                                             skip_initial_space=True)

        try:
            difficulty_vector = {instance: difficulty_vector[instance] + quality_vector[instance] for
                                 instance in quality_vector.keys()}
        except KeyError:
            difficulty_vector = {instance: quality_vector[instance] for instance in quality_vector.keys()}

    # Round wrong floating values
    for instance in difficulty_vector.keys():
        difficulty_vector[instance] = round_float(difficulty_vector[instance])
    return difficulty_vector


def _get_quality_vector(vector_path: str, number_of_trees: int, delimiter: str, quoting: int, quote_char: str,
                        line_delimiter: str, encoding: str = "utf8", skip_initial_space: bool = True) -> Dict[str, int]:
    """ Construct an quality vector for one t-norm. An quality vector correspond to a dictionary mapping one instance
    to its true class and all classes found by a tree, along with their % of membership.
    """
    quality_vector = dict()

    # Extract classes from the header
    classes = get_header(path=vector_path, encoding=encoding, delimiter=delimiter, quoting=quoting,
                         quote_char=quote_char, line_delimiter=line_delimiter,
                         skip_initial_space=skip_initial_space)[2:]

    for row in iter_rows(path=vector_path, encoding=encoding, delimiter=delimiter, quoting=quoting,
                         quote_char=quote_char, line_delimiter=line_delimiter, skip_initial_space=skip_initial_space,
                         skip_header=True):
        identifier, true_class, *rest = row
        membership = rest[classes.index(true_class)]
        quality_vector[identifier] = membership / number_of_trees

    return quality_vector


def _dump_difficulty_vectors(difficulty_vectors: Dict[str, Dict[str, float]], difficulty_vectors_paths: Dict[str, str],
                             delimiter: str, quoting: int, quote_char: str,
                             encoding: str, line_delimiter: str, skip_initial_space: bool = True) -> None:
    """ Dump all the difficulty vectors into their proper directory. """
    for tnorm in difficulty_vectors.keys():
        _dump_difficulty_vector(vector_path=difficulty_vectors_paths[tnorm],
                                difficulty_vector=difficulty_vectors[tnorm],
                                delimiter=delimiter,
                                quoting=quoting,
                                quote_char=quote_char,
                                encoding=encoding,
                                line_delimiter=line_delimiter,
                                skip_initial_space=skip_initial_space)


def _dump_difficulty_vector(vector_path: str, difficulty_vector: Dict[str, float], delimiter: str, quoting: int,
                            quote_char: str, line_delimiter: str, encoding: str = "utf8",
                            skip_initial_space: bool = True) -> None:
    """ Dump the content of a difficulty vector for one t-norm. A difficulty vector correspond to the sum of all true
    class's % of membership for all quality vectors. It assign a classification difficulty to an example from the
    reference database.
    """
    with open(vector_path, "w", encoding=encoding, newline=line_delimiter) as file:
        writer = csv.writer(file, delimiter=delimiter, quoting=quoting, quotechar=quote_char,
                            skipinitialspace=skip_initial_space)
        for identifier in difficulty_vector.keys():
            row = [identifier, difficulty_vector[identifier]]
            writer.writerow(row)


if __name__ == "__main__":
    pass
