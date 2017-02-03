import json
import os
import pathlib

with open(lost_config.json) as conf:
	c = json.load(conf)
	dbname = c['database']['dbname']
	dbhost = c['database']['dbhost']
	dbport = c['database']['dbport']
	secret_key = c['session']['secret_key']