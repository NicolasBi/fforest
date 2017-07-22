""" This module contains all functions related to phases.

"""
import enum
from typing import Callable, List

import fforest.src.getters.environment as env
from fforest.src.core.phase.ending.exit_code import EXIT_SUCCESS


@enum.unique
class Phase(enum.IntEnum):
    PARSING = 0
    PREPROCESSING = 1
    INITIAL_SPLIT = 2
    REFERENCE_SPLIT = 3
    SUBSUBTRAIN_SPLIT = 4
    LEARNING = 5
    REDUCTION = 6
    QUALITY = 7
    CLASSES_MATRICES = 8
    CLUSTERING_TREES = 9
    ENDING = 10
    NONE = 11


class UnknownPhase(Exception):
    def __init__(self, phase_name: str):
        Exception.__init__(self, "The phase \"{phase_name}\" doesn't"
                                 " exists".format(phase_name=phase_name))


def str_to_phase(string: str) -> Phase:
    """ Return the enum value associated with the name `string`, case insensitive. """
    string = string.lower()
    for phase_name, phase_value in zip(Phase.__members__.keys(), Phase.__members__.values()):
        if string == phase_name.lower():
            return phase_value
    raise UnknownPhase(string)


def phase_to_str(phase: Phase) -> str:
    """ Return the name of a phase as a lowercase str. """
    return phase.name.lower()


def phase_processable(phase_to_compute, last_phase_computed) -> bool:
    """ Check if a phase can be processed. A phase is processable if at least the phase preceding it has been completed,
    thus the values of the `Phase` enums and their unicity are important.
    """
    return phase_to_compute.value <= last_phase_computed.value + 1


def call_all_phases(starting_phase: Phase, parsing_function: Callable) -> None:
    phases_entry_points = _load_phases_entry_points(parsing_function)
    for phase_index in range(starting_phase.value, len(phases_entry_points)):
        phases_entry_points[phase_index]()
        _increment_phase()


def _increment_phase() -> None:
    _exit_if_last_phase()
    env.current_phase = _get_next_phase(env.current_phase)


def _exit_if_last_phase() -> None:
    if env.current_phase == env.last_phase:
        if env.current_phase.value < Phase.ENDING.value:
            # If the ending phase has not been processed
            from fforest.src.core.phase.ending.ending import ending
            ending()
        else:
            exit(EXIT_SUCCESS)


def _get_next_phase(phase: Phase) -> Phase:
    for next_phase in Phase.__members__.values():
        if phase.value + 1 == next_phase.value:
            return next_phase


def _load_phases_entry_points(parsing_function: Callable) -> List[Callable]:
    """ Return a list containing all entry point for each phase in the exact same order of the phases' values. The
    parsing function is
    """
    from fforest.src.core.phase.preprocessing.preprocessing import preprocessing
    from fforest.src.core.phase.initialization.initial_split import initial_split
    from fforest.src.core.phase.initialization.reference_split import reference_split
    from fforest.src.core.phase.learning_process.subsubtrain_split import subsubtrain_split
    from fforest.src.core.phase.learning_process.forest_construction import forest_construction
    from fforest.src.core.phase.learning_process.forest_reduction import forest_reduction
    from fforest.src.core.phase.performance_evaluation.forest_quality import forest_quality
    from fforest.src.core.phase.performance_evaluation.classes_matrices import classes_matrices
    from fforest.src.core.phase.performance_evaluation.clustering_trees import clustering_trees
    from fforest.src.core.phase.ending.ending import ending

    return [parsing_function, preprocessing, initial_split, reference_split, subsubtrain_split, forest_construction,
            forest_reduction, forest_quality, classes_matrices, clustering_trees, ending]
