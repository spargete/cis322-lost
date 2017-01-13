git clone https://github.com/postgres/postgres -b REL9_5_STABLE --single-branch $HOME/postgres

curl http://www.gtlib.gatech.edu/pub/apache//httpd/httpd-2.4.25.tar.bz2 > httpd-2.4.25.tar.bz2
tar -xjf httpd-2.4.25

cd postgres
./configure --prefix=$1
make
make install

cd ../httpd-2.4.25
./configure --prefix=$1
make
make install