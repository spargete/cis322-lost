#Curl the legacy data
curl https://classes.cs.uoregon.edu/17W/cis322/files/osnap_legacy.tar.gz > $HOME/osnap_legacy.tar.gz
#extract it
cd $HOME
tar -xzf osnap_legacy.tar.gz

#to run a command without jumping into the thing do psql -c "command"
#to use a file as a command use -f filename
cd osnap_legacy

psql -d $1 -p $2 -f $HOME/cis322-lost/sql/create_tables.sql
python3 $HOME/cis322-lost/sql/import_data.py > import_data.sql
#Here the python script just has to print the import statements
psql -d $1 -p $2 -f import_data.sql
rm import_data.sql
