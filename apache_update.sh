#!/bin/bash
git pull
cp -r ./src/wsgi/ ~
apachectl restart
