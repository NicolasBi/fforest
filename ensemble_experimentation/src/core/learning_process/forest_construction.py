""" Asynchronously create `t_norms` number of trees/fuzzy-trees inside each subsubtrain directory with the help of the
Salammbô executable, located inside the `bin` directory, at the root of the software. Then, compute booleans and result
vectors for each tree and save it.
"""
from multiprocessing import Process
from os import path
from typing import List, Dict

import ensemble_experimentation.src.getters.environment as env
from ensemble_experimentation.src.core.learning_process.classification_methods import methodnum_to_str
from ensemble_experimentation.src.core.learning_process.entropy_measures import EntropyMeasure
from ensemble_experimentation.src.file_tools.format import format_to_string
from ensemble_experimentation.src.vrac.file_system import dump_string, get_path
from ensemble_experimentation.src.vrac.iterators import grouper
from ensemble_experimentation.src.vrac.process import execute_and_get_stdout

HERE = path.abspath(path.dirname(__file__))
PATH_TO_SALAMMBO = HERE + "/../../../bin/Salammbo"
MANDATORY_OPTIONS = ["-R", "-L", "-M", "-N"]

# Key values
KEY_TRUECLASS = "trueclass"


def forest_construction():
    """ Asynchronously create `t_norms` number of trees/fuzzy-trees inside each subsubtrain directory with the help of
    the Salammbô executable, located inside the `bin` directory, at the root of the software. Then, compute booleans
    and result vectors for each tree and save it.
    """
    subtrain_dir_path = get_path(env.subtrain_database_path)
    chosen_options = _parameters_to_salammbo_options(discretization_threshold=str(env.discretization_threshold),
                                                     entropy_measure=env.entropy_measure,
                                                     number_of_tnorms=str(env.t_norms),
                                                     entropy_threshold=env.entropy_threshold,
                                                     min_size_leaf=env.minimal_size_leaf)
    counter_size = len(str(env.trees_in_forest))
    processes = list()
    for tree_index in range(1, env.trees_in_forest + 1):
        database_name = env.subsubtrain_directory_pattern % str(tree_index).zfill(counter_size)
        database_path = "{0}/{1}/{1}.{2}".format(subtrain_dir_path, database_name, format_to_string(env.format_output))
        process = Process(target=_tree_construction,
                          args=(database_path,
                                env.reference_database_path,
                                env.t_norms,
                                chosen_options,
                                env.vector_file_extension))
        processes.append(process)

    # Start the processes
    for process in processes:
        process.start()
        exit(0)

    # Wait for all processes to finish
    for process in processes:
        process.join()


def _parameters_to_salammbo_options(discretization_threshold: str, entropy_measure: EntropyMeasure,
                                    number_of_tnorms: str, entropy_threshold: str, min_size_leaf: str) -> List:
    """ Compute then return a list of options which'll be understood and used by the Salammbô executable, located inside
    the `bin` directory, at the root of the software.
    """
    options = list()

    # Discretization threshold
    options.append("-c")
    options.append(discretization_threshold)

    # Entropy measure
    if entropy_measure == EntropyMeasure.SHANNON:
        options.append("-u")

    # Number of t-norms
    options.append("-f")
    options.append(number_of_tnorms)

#    # Entropy threshold
#    options.append("-e")
#    options.append(entropy_threshold)

    # Min size leaf
#    if is_a_percentage(min_size_leaf):
#        options.append("-i")
#    else:
#        options.append("-I")
#    options.append(min_size_leaf)

    return options


def _tree_construction(path_to_database: str, path_to_reference_database: str, number_of_tnorms: int,
                       chosen_options: iter, vector_file_extension: str) -> None:
    """ Create `t-norm` number of tree inside a subsubtrain directory with the help of the Salammbô executable, located
    inside the `bin` directory, at the root of the software. Then, compute booleans and result vectors for each tree and
    save it.
    """
    lines = _construct_tree(path_to_database=path_to_database,
                            path_to_reference_database=path_to_reference_database,
                            chosen_options=chosen_options)
    print(lines)
    result = _parse_result(lines=lines,
                           number_of_tnorms=number_of_tnorms)
    print(result)
    _clean_result(result=result,
                  number_of_tnorms=number_of_tnorms)
    print(result)
    vectors = _get_boolean_vectors(result=result,
                                   number_of_tnorms=number_of_tnorms)
    print(vectors)
    _save_vectors(vectors=vectors,
                  subsubtrain_dir_path=get_path(path_to_database),
                  vector_file_extension=vector_file_extension)


def _construct_tree(path_to_database: str, path_to_reference_database: str, chosen_options: iter) -> str:
    """ Call the Salammbô executable with the chosen options and parameters, then return the output. """
    parameters = MANDATORY_OPTIONS + chosen_options
    parameters.append(path_to_database)
    parameters.append(path_to_reference_database)
    print(parameters)
    return execute_and_get_stdout(PATH_TO_SALAMMBO, *parameters)


def _parse_result(lines: str, number_of_tnorms: int) -> dict:
    """ Parse lines outputted from the Salammbo executable.
    Construct a dictionary of result.
    Each key is an identifier of an instance and has for value another dictionary. Each of theses dictionary contains
    the "realclass" key, redirecting to the real class of an instance. They also contains a keys for each t-norm used to
    find a classification result. These keys redirect to a last dictionary containing the class found by this t-norm
    associated with a degree of membership.
    """
    # Each lines format is as follows :
    # Null T-NORM IDENTIFIER TRUECLASS [(FOUNDCLASSX MEMBERSHIPDEGREEX) (FOUNDCLASSY MEMBERSHIPDEGREEY) ...]
    result = dict()
    try:
        for tnorm_chunk in grouper(number_of_tnorms, lines.split("\n")):
            for instance in tnorm_chunk:
                print(instance)
                _, tnorm, identifier, true_class, *rest = instance.split()
                identifier = int(identifier)
                print(tnorm)
                print(identifier)
                print(true_class)
                print(rest)
                try:
                    result[identifier][methodnum_to_str(int(tnorm))] = {class_found: float(membership_degree)
                                                                        for class_found, membership_degree in
                                                                        grouper(2, rest)}
                except KeyError:  # Will be triggered at the first instance for each chunk
                    result[identifier] = dict()
                    result[identifier][KEY_TRUECLASS] = true_class
                    result[identifier][methodnum_to_str(int(tnorm))] = {class_found: float(membership_degree)
                                                                        for class_found,
                                                                        membership_degree in grouper(2, rest)}
    except ValueError:  # For the last empty line
        pass
    return result


def _clean_result(result: dict, number_of_tnorms: int) -> None:
    """ Map to every t-norm for each identifier of the result dictionary, True if this t-norm has correctly predicted
    the real class, or False otherwise.
    """
    for identifier in result.keys():
        real_class = result[identifier][KEY_TRUECLASS]
        for tnorm in range(number_of_tnorms):
            try:
                classes_found = result[identifier][methodnum_to_str(tnorm)]
                class_found = max(classes_found.keys(), key=(lambda key: classes_found[key]))
                result[identifier][methodnum_to_str(tnorm)] = class_found == real_class
            except KeyError:
                result[identifier][methodnum_to_str(tnorm)] = False
            except ValueError:
                result[identifier][methodnum_to_str(tnorm)] = False


def _get_boolean_vectors(result: dict, number_of_tnorms: int) -> Dict[str, List[bool]]:
    """ Construct a boolean vector for each t-norm with the result dictionary, parsed from the output of the Salammbô
    executable.
    """
    vectors = dict()
    for tnorm_number in range(number_of_tnorms + 1):
        tnorm_key = methodnum_to_str(tnorm_number)
        vectors[tnorm_key] = [result[identifier][tnorm_key] for identifier in result]
    return vectors


def _save_vectors(vectors: Dict[str, List[bool]], subsubtrain_dir_path: str, vector_file_extension: str) -> None:
    """ Dump the content of the vectors inside the subsubtrain directory. This method'll dump for each tnorm, a binary
    vector and a result vector.
    """
    for tnorm_name in vectors.keys():
        vector_path = "{}/{}.{}".format(subsubtrain_dir_path, tnorm_name, vector_file_extension)
        vector_content = vectors[tnorm_name]
        _save_boolean_vector(vector_path, vector_content)


def _save_boolean_vector(vector_content: str, vector: List[bool]) -> None:
    """ Dump the content of one boolean vector inside the subsubtrain directory. """
    content = "".join("1" if result else "0" for result in vector)
    dump_string(vector_content, content)


if __name__ == "__main__":
    pass
