import enum
import fforest.src.getters.environment as env


@enum.unique
class Phase(enum.IntEnum):
    NONE = 0
    PREPROCESSING = 1
    INITIALIZATION = 2
    LEARNING = 3
    REDUCTION = 4
    QUALITY = 5
    CLASSES_MATRICES = 6
    ENDING = 7


class UnknownPhase(Exception):
    def __init__(self, phase_name: str):
        Exception.__init__(self, "The phase \"{phase_name}\" doesn't"
                                 " exists".format(phase_name=phase_name))


def str_to_phase(string: str) -> Phase:
    string = string.lower()
    if string == "none":
        return Phase.NONE
    elif string == "preprocessing":
        return Phase.PREPROCESSING
    elif string == "initialization":
        return Phase.INITIALIZATION
    elif string == "learning":
        return Phase.LEARNING
    elif string == "reduction":
        return Phase.REDUCTION
    elif string == "quality":
        return Phase.QUALITY
    elif string == "classes_matrices":
        return Phase.CLASSES_MATRICES
    elif string == "ending":
        return Phase.ENDING
    else:
        raise UnknownPhase(string)


def phase_to_str(phase: Phase) -> str:
    if phase == Phase.NONE:
        return "none"
    elif phase == Phase.PREPROCESSING:
        return "preprocessing"
    elif phase == Phase.INITIALIZATION:
        return "initialization"
    elif phase == Phase.LEARNING:
        return "learning"
    elif phase == Phase.REDUCTION:
        return "reduction"
    elif phase == Phase.QUALITY:
        return "quality"
    elif phase == Phase.CLASSES_MATRICES:
        return "classes_matrices"
    elif phase == Phase.ENDING:
        return "ending"
    else:
        return "unknown"


def get_next_phase(phase: Phase) -> Phase:
    if phase == Phase.ENDING:
        return Phase.NONE

    for next_phase in Phase:
        if phase.value + 1 == next_phase.value:
            return next_phase


def increment_phase() -> None:
    env.current_phase = get_next_phase(env.current_phase)
