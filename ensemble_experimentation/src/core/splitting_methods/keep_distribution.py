from typing import Tuple

from ensemble_experimentation.src.vrac import is_an_int


def keep_distribution():
    pass


def keep_distribution2(content, row_limit, out_writer_train, out_writer_test, class_name, number_of_rows: int) ->\
        Tuple[int, int]:
    row_count_train, row_count_test = 0, 0
    # We store rows into the distribution dictionary
    distribution_dictionary = dict()

    if is_an_int(class_name):
        class_name = int(class_name)
    for row in content:
        if row[class_name] in distribution_dictionary:
            distribution_dictionary[row[class_name]].append(row)
        else:
            distribution_dictionary[row[class_name]] = [row]

    # Then we distribute the rows proportionally
    percentage_train = row_limit / number_of_rows
    # If the class name is an index
    if isinstance(class_name, int):
        for class_name in distribution_dictionary.keys():
            # Distribute to train
            rows_to_give = int(round(len(distribution_dictionary[class_name]) * percentage_train))
            row_count_train += rows_to_give
            for _ in range(rows_to_give):
                out_writer_train.writerow(distribution_dictionary[class_name].pop(0))

            # Then the rest to test
            for row in distribution_dictionary[class_name]:
                out_writer_test.writerow(row)
                row_count_test += 1
    # If it's a name
    else:
        for class_name in distribution_dictionary.keys():
            # Distribute to train
            rows_to_give = int(round(len(distribution_dictionary[class_name]) * percentage_train))
            row_count_train += rows_to_give
            for _ in range(rows_to_give):
                out_writer_train.writerow(distribution_dictionary[class_name].pop(0).values())

            # Then the rest to test
            for row in distribution_dictionary[class_name]:
                out_writer_test.writerow(row.values())
                row_count_test += 1

    return row_count_train, row_count_test