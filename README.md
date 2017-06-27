# ensemble_experimentation
## TODO
* Find an english name for the package
* Implement the `guess` option for the parameter --have-header with the help of this code snippet : https://docs.python.org/3/library/csv.html#csv.Sniffer.has_header
* Implement the `guess` option for the parameters --delimiter, --quoting, --quote-character and --encoding.
* Add more messages related to the verbosity
* Add some progress bars with the package : https://pypi.python.org/pypi/progressbar2
* Rewrite all path processing code with the package : https://pypi.python.org/pypi/path.py
* Save each directory path in the `env` module
* Save each database path in the `env` module
* Implement other format for the input database (each format must be changed to the CSV format during the preprocessing phase)
* Find and rename entry points, I propose : `fforest`, `fforest_preprocessing <DIR>`, `fforest_initialization <DIR> (without preprocessing)`, `fforest_learning <DIR>`, `fforest_reduction <DIR>`. Maybe implement just one entry point (`fforest`) then directly after the optional phase (`preprossing`, `initialisation`, `learning`, `reduction`) which'll be convert to an enum. Add a variable `completed_phase` in the `env` module.
* Add the file `environment.json` at the root of the main directory, which will contains informations about the database, and must be created right after the preprocessing phase. This file'll could then be loaded by each entry point thereafter.
