import csv
import ensemble_experimentation.src.getters.get_default_value as gdv
import ensemble_experimentation.src.getters.get_parameter_name as gpn
from ensemble_experimentation.src.vrac import create_dir
import ensemble_experimentation.src.getters.environment as env
import ensemble_experimentation.src.getters.get_statistic_name as gsn


def _add_id(input_path: str, output_path: str, id_name: str, have_header: bool, delimiter: str):
    """ Add an identificator for each instance into the database.
    If the parameter id_name is provided, it'll be inserted as a header of the output_file.
    """
    with open(input_path) as input_file, open(output_path, "w") as output_file:
        output_writer = csv.writer(output_file, delimiter=delimiter)
        input_reader = csv.reader(input_file, delimiter=delimiter)

        if have_header:
            header = next(input_reader)
            header.insert(0, id_name)
            output_writer.writerow(header)

        for row_index, row in enumerate(input_reader):
            if row:
                row.insert(0, row_index)
                output_writer.writerow(row)


def preprocessing(args: dict):
    """ Prepare the original database to be splitted. """
    # Create the main directory of the application
    create_dir(args[gpn.main_directory()])

    original_has_been_modified = False
    if args[gpn.identifier()] is None:
        # We must add an identificator column
        _add_id(input_path=args[gpn.database()], output_path=env.statistics[gsn.preprocessed_database_path()],
                id_name=gdv.identifier(), have_header=args[gpn.have_header()], delimiter=args[gpn.delimiter()])
        original_has_been_modified = True

    if original_has_been_modified:
        # The database has been modified, we need to change the input path for the original split
        env.initial_split_input_path = env.statistics[gsn.preprocessed_database_path()]
    else:
        env.initial_split_input_path = env.statistics[gsn.database_path()]


if __name__ == '__main__':
    pass
