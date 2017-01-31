create_tables.sql -- initial creation of tables
import_data.sh -- Downloads, parses, and imports the legacy data from the given location.
import_data.py -- Run by import_data.sh, creates a temporary .sql file with all of the statements required. import_data.sh deletes this temporary file after running.