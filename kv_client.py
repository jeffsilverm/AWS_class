#! /usr/bin/env python
#
#
import random
import time
import sys
from urllib import urlopen
import httplib
import kv_pair
import re

HOST = sys.argv[1]
PORT = sys.argv[2]

# See https://docs.python.org/2/library/httplib.html#httpconnection-objects
http_conn = httplib.HTTPConnection(HOST, PORT, timeout=10)

# "found value green for key Daniel"
prog = re.compile(r"$found value .* for key .*")

def delete( key ):
  http_conn.request("DELETE", "?%s" % key )
# an HTTPResponse instance see
# https://docs.python.org/2/library/httplib.html#httpresponse-objects
  response = http_conn.getresponse()
  status = response.status
  reason = response.reason    # Reason phrase returned by server.
  print "The response to deleting %s was %s %s" % (key, status, reason )
  return status

def post ( key, value ):
  http_conn.request("POST", "", body="%s=%s" % (key, value), headers="")
  response = http_conn.getresponse()
  status = response.status
  reason = response.reason    # Reason phrase returned by server.
  print "The response to posting $s was %s %s" % (key, status, reason )
  return status

def get ( key ) :
  http_conn.request("GET", "?%s" % key, body="", headers="")
  response = http_conn.getresponse()
  body = response.read()
# The body contains a string of the form "found value green for key Daniel"
# https://docs.python.org/2/library/re.html#match-objects
  m = prog.match(body)
  if m == None :
    print "No values were found in the response string %s" % body
  else :
    value = m.group(1)
    key = m.group(2)
  status = response.status
  reason = response.reason    # Reason phrase returned by server.
  print "The response to get $s was %s %s" % (key, status, reason )
  print "The value returned was %s" % value
  return status

def post ( key, value ):
  http_conn.request("PUT", "", body="%s=%s" % (key, value), headers="")
  response = http_conn.getresponse()
  status = response.status
  reason = response.reason    # Reason phrase returned by server.
  print "The response to posting $s was %s %s" % (key, status, reason )
  return status




if __name__ == "__main__" :
  def test_get( key ):
    print "Getting key %s from database" % key
    value = get ( key )
    if key in check_dict :
      print "The value for key %s is %s" % ( key, value )
      assert value[0] == check_dict[key], \
             "Database returned wrong value: %s should have returned %s" % \
             (value[0], check_dict[key])
      assert value[1] == 200, "Database call did not return 200"
    else :
      print "key %s does not exist in database" % key
      assert value[0] == None, \
             "Database should have returned None but returned %s" % value[0]
      assert value[1] == 403, \
             "Database should have returned 403 but returned %d" % value[1]


  def test_post( key, value ):
    print "Inserting key %s with value %s" % ( key, value )
    status = post ( key, value )
    if key not in check_dict:
      if DEBUG :
        assert status == 200, \
          "Key %s not in check_dict and should be because DEBUG is True." + \
          "Status is %d" % (key, status)
      else :
        assert status == 403 or status == 200, \
          "key % is not in check_dict, and we don't know if it should be because"+\
          "it's not in check_dict.  Status is %d" % ( key, status )
      check_dict[key] = value
# Verify that the key really inserted the value into the database
      assert value == get ( key )[0]
    else:
      print "Tried to insert a key that was already in the database." +\
      "Should have used put instead of post"
      assert status == 403
      
  def test_delete ( key ):
    print "Testing deleting key %s from the database" % key
    status = delete ( key )
    if key in check_dict :
      print "key-value pair was deleted"
      assert status == 200, \
          "Status was %d should have been 200 when removing a key that exists" % status
      del check_dict[key]
# Verify that the key is really gone.  This should fail
      status = get ( key )
      assert status == (None, 403),"Status was %s should have been a tuple (None,403)"%\
             str( status )
    else:
      print "The key was not in the database"
      assert status == 200,"Status was %d should have been 200 after attempting to "+\
             "delete a key from the database that should not have been there"
  def test_put ( key, value ):
    print "Testing updating key %s with value %s" % ( key, value )
    status = put ( key, value )
    if key in check_dict :
      assert status == 200
      check_dict[key] = value
      value = get ( key )
      assert value[0] == check_dict[key]
      assert value[1] == 200
    else :
      print "Key %s is not in check_dict" % key
# A little consistency check to make sure that the database and the dictionary
# really are in sync.
      value = get ( key )
      assert value[0] == None
      assert value[1] == 403 

########################################################## 



  check_dict = {}

    
    
  
  test_delete("Dillon")    # He may already be in the table
  test_post("Dillon", "From the remote client")
  test_get("Dillon")
  test_delete("Devin")
  test_post("Devin", 20)
  test_get("Devin")
  test_put("Devin", 22)
  test_get("Devin")
  test_delete("Janie")
  test_post("Janie", 12)
  test_get("Janie")
  test_put("Janie", -3)
  test_get("Janie")
  kv_pair.delete("Randall")
  try:
    check_dict["Randall"] = -12.3
    test_get("Randall")   # This should throw an error because Randall is in the check_dict
  except AssertionError:
    print "Threw an expected Assertion error getting a non-existant key - all is well"
  else :
    assert True,"Did *not* throw an expected Assertion Error"
  try:
    test_put("Randall", 3421)
  except AssertionError:
    print "Threw an expected Assertion error - all is well.  Tried to update a non-existant key"
  else :
    assert True,"Did *not* throw an expected Assertion Error"
# GET, HEAD, PUT
  test_delete("Janie")
  test_delete("Janie")  # Test that delete is idempotent
  test_put("Devin", "Green")
  test_get("Devin")
  test_put("Devin", "Green")  # Test that put is idempotent
  test_get("Devin")
  test_get("Devin")
  while True:
    op = raw_input("Enter I to insert, U to update, D to delete, or G to get ")
    op = op.upper()
    key = raw_input("Enter a key ")
    if op == "I" :
      value = raw_input("Enter a value for key %s " % key )
      try :
        post ( key, value )
      except boto.dynamodb2.exceptions.ConditionalCheckFailedException:
        print "Probably the key %s already has a value.  let's see" % key
        value = get ( key )
        print "Yes, the value is %s" % value
    elif op == "U" :
      value = raw_input("Enter a value for key %s" % key )
      try :
        put ( key, value )
      except boto.dynamodb2.exceptions.ConditionalCheckFailedException:
        print "Probably the key %s already doesn't a value.  let's see" % key
        try :
          value_1 = get( key )
        except boto.dynamodb2.exceptions.ConditionalCheckFailedException:
          print "I was right - there is no value for key %s" % key
        else :
          print "Something else must be wrong.  Key %s has value %s" % \
                (key, value_1)
    elif op == "D" :
      delete ( key )
    elif op == "G" :
      value = get ( key )
      print "The value of %s is %s" % ( key, value )
    else :
      print "You didn't enter I, U, D, or G!"

