This application should be run through wsgi with Apache.
app.py -- python code that is run when the webserver starts
lost.wsgi -- code that sets up the webserver. Runs automatically.
config.py -- python code that sets up the configuration for the webserver
lost_config.json -- config file that config.py accesses for its data
login.html -- the login page
logout.html -- the logout page
report_filter.html -- the page to filter which report and what data to show
facility_report.html -- page which is shown when "Facility report" is checked on the report_filter page
transit_report.html -- page which is shown when "Transit report" is checked on the report_filter page