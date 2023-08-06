# FAIRification Genomic Data Tracks JSON Schema validation, Python edition

The JSON schema should be compliant with JSON Schema Draft04, Draft06 or Draft07 specifications.

So, this validation program uses libraries compliant with that specification.

The installation instructions are in [INSTALL.md](INSTALL.md) .

## History

The roots of this code come from [https://github.com/inab/benchmarking-data-model/tree/0.4.0/toolsForValidation](https://github.com/inab/benchmarking-data-model/tree/0.4.0/toolsForValidation).

Its development was later followed at [https://github.com/fairtracks/fairtracks_validator/], where implementations in other programming languages were also hosted. Python code gained traction and real modularisation there.

As this Python code is relevant to several research projects, it has been split from its latest repo, keeping the core and original extensions at [https://github.com/inab/python-extended-json-schema-validator](https://github.com/inab/python-extended-json-schema-validator), and keeping these specific FAIRTracks extensions at [https://github.com/fairtracks/fairtracks_validator_python](https://github.com/fairtracks/fairtracks_validator_python).

## Usage

```bash
python jsonValidate.py --help
```
```
usage: fairGTrackJsonValidate.py [-h] [--log-file LOGFILENAME] [--log-format LOGFORMAT] [-q] [-v] [-d] [-V] [-C CONFIGFILENAME]
                                 [--cache-dir CACHEDIR] [--report REPORTFILENAME] [--verbose-report]
                                 [--invalidate | --read-only] [--warm-up | --lazy-load]
                                 json_schema_or_dir [json_file_or_dir [json_file_or_dir ...]]

Validate JSON against JSON Schemas with extensions (version 0.9.7)

positional arguments:
  json_schema_or_dir    The JSON Schema file or directory to validate and use
  json_file_or_dir      The JSON files or directories to be validated

optional arguments:
  -h, --help            show this help message and exit
  --log-file LOGFILENAME
                        Store messages in a file instead of using standard error and standard output
  --log-format LOGFORMAT
                        Format of log messages
  -q, --quiet           Only show engine warnings and errors
  -v, --verbose         Show verbose (informational) messages
  -d, --debug           Show debug messages (use with care, as it could potentially disclose sensitive contents)
  -V, --version         show program's version number and exit
  -C CONFIGFILENAME, --config CONFIGFILENAME
                        Configuration file (used by extensions)
  --cache-dir CACHEDIR  Caching directory (used by extensions)
  --report REPORTFILENAME
                        Store validation report (in JSON format) in a file
  --verbose-report      When this flag is enabled, the report also embeds the json contents which were validated
  --invalidate          Caches are invalidated on startup
  --read-only           When this flag is enabled, the caches are read-only, avoiding expensive operations related to the caches
  --warm-up             Caches are warmed up on startup
  --lazy-load           Caches are warmed up in a lazy way
```

Next lines run validations using test data:

```bash
git clone https://github.com/fairtracks/fairtracks_validator/
python fairGTrackJsonValidate.py fairtracks_validator/test-data/foreignProperty_simple/schemas/ fairtracks_validator/test-data/foreignProperty_simple/good_validation/
python fairGTrackJsonValidate.py fairtracks_validator/test-data/foreignProperty_simple/schemas/ fairtracks_validator/test-data/foreignProperty_simple/bad_validation/
```

And this is an asciinema recording a previous version of FAIRTracks Validator:

[![asciicast](https://asciinema.org/a/279252.svg)](https://asciinema.org/a/279252)
