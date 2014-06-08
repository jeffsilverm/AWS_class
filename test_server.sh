#! /bin/bash
#
# This script uses curl to test the kv_server.py database.
#
PORT=8080
HOST=localhost
# Comment out H if you don't want to see the returned HTTP headers
H="-i"
#
#
curl $H -d "Daniel=green"  http://${HOST}:${PORT}
curl $H http://${HOST}:${PORT}?Daniel
curl $H -d "Daniel=blue" http://${HOST}:${PORT}?Daniel
curl $H http://${HOST}:${PORT}?Daniel
#
echo "Testing a non-existant key"
curl $H http://${HOST}:${PORT}?Reginald

echo "Testing for the existance of a key that exists using a HTTP HEAD verb"
curl $H -I http://${HOST}:${PORT}?Daniel
echo "Testing for the existance of a key that does not exist using a HTTP HEAD verb"
curl $H -I http://${HOST}:${PORT}?Reginald




