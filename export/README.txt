Export scripts for exporting from a LOST database.
export_data.sh -- Usage: ./export_data.sh <dbname> <output dir> Runs the SQL scripts to fetch the data from the database, outputting them to .csv files in the output directory specified.
export_users.sql -- Fetches user data from the database, outputting username, password, role name, and whether or not they are an active user to stdout. Export_data redirects that to users.csv
export_facilities.sql -- Fetches facility data from the database, outputting fcode and common name to stdout. Export_data redirects that to facilities.csv
export_assets.sql -- Fetches asset data from the database, outputting asset tag, description, original location, intake date, and disposal date (or 'NULL') to stdout. Export_data redirects that to assets.csv
export_transfers.sql -- Fetches transfer request data from the database, outputting asset tag, username of requester, request date, username of approver, approval date, source facility fcode, destination facility fcode, load time, and unload time to stdout. Export_data redirects that to transfers.csv
