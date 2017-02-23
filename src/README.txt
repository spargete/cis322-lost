This application should be run through wsgi with Apache.
app.py -- python code that is run when the webserver starts
lost.wsgi -- code that sets up the webserver. Runs automatically.
config.py -- python code that sets up the configuration for the webserver
lost_config.json -- config file that config.py accesses for its data
templates/create_user.html -- shows a form that adds a user to the database
templates/incorrect_credentials.html -- shows a page that tells the user that they didn't enter the correct credentials
templates/user_added.html -- shows a page that informs the user that their credentials were added to the database
templates/user_exists.html -- shows a page that informs the user that the username they picked already existed in the database
templates/login.html -- shows a form that checks the database for the credentials the user entered
templates/dashboard.html -- shows a bit of text that tells the user what their username is, links to the add/remove assets and facilities page
templates/add_facility.html -- shows a table with all the facilities currently in the system and a form to add them
templates/add_asset.html -- shows a table with all the assets currently in the system and a form to add them
templates/asset_exists.html -- shows some text that tells the user that the asset tag they are trying to create is already in the system
templates/facility_exists.html -- shows some text that tells the user that the name or fcode they are trying to create is already in the system
