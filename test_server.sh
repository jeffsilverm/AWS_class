#! /bin/bash
#
# This script uses curl to test the kv_server.py database.
#
PORT=8081
HOST=localhost
# Comment out H if you don't want to see the returned HTTP headers
H="-i"
#
#
echo "Set Daniel to green - method is PUT"
curl $H -d "Daniel=green" -X PUT  http://${HOST}:${PORT}
curl $H http://${HOST}:${PORT}?key=Daniel
echo "Set Daniel to blue - method is POST"
curl $H -d "Daniel=blue" http://${HOST}:${PORT}?Daniel
curl $H http://${HOST}:${PORT}?key=Daniel
#
echo "Testing a non-existant key - method is GET"
curl $H http://${HOST}:${PORT}?key=Reginald

echo "Testing for the existance of a key that exists using a HTTP HEAD verb"
curl $H -I http://${HOST}:${PORT}?Daniel
echo "Testing for the existance of a key that does not exist using a HTTP HEAD verb"
curl $H -I http://${HOST}:${PORT}?Reginald

echo "Deleting key Daniel - method is DELETE"
curl $H -X DELETE http://${HOST}:${PORT}?key=Daniel
echo "Verifying that Daniel is gone - method is GET"
curl $H http://${HOST}:${PORT}?key=Daniel




