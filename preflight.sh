#!/usr/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: ./preflight.sh <dbname>"
    exit;
fi

cd sql
bash import_data.sh $1 5432
cd ..
rm -rf osnap_legacy osnap_legacy.tar.gz

cp -r src/wsgi ~
