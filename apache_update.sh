#!/bin/bash
git pull
cp -r $HOME/cis322-lost/src/wsgi/ ~
apachectl restart
