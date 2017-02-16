This application should be run through wsgi with Apache.
app.py -- python code that is run when the webserver starts
lost.wsgi -- code that sets up the webserver. Runs automatically.
config.py -- python code that sets up the configuration for the webserver
lost_config.json -- config file that config.py accesses for its data