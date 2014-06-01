#! /usr/bin/env python
#
# This script implements a simple key-value store using DynamoDB.  Input
# is a key and the return is a value.  Operations include
# (These verbs are from RFC 2616 section 9) 
# http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html
# GET - given a key, return the corresponding value
# POST - insert a key-value pair in the database, error if the key already exists
# PUT - update a key-value pair in the database, error if the key does not already exist
# DELETE - deletes a key-value pair from the database
#
# This assumes that access credentials are stored in the file ~/.boto

import boto.dynamodb2
from boto.dynamodb2.table import Table
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.fields import HashKey
from boto.exception import JSONResponseError
import time

TABLE_NAME = 'kv_pairs'

conn = DynamoDBConnection()
table_list = conn.list_tables()
# The table_list is a dictionary with a single key, the value of which is
# a list of tables associated with this account.  If TABLE_NAME is not in
# that list, then create the table, otherwise, just connect to it.
if TABLE_NAME in table_list[u'TableNames'] :
# Make sure that the database is new, otherwise leftovers from previous runs
# may cause some of the tests to fail.
  kv_pairs = Table(TABLE_NAME)
  kv_pairs.delete()
# now that the table is gone, recreate it
while True :
  time.sleep(10)    # it takes some time for the table to delete
  try:
    kv_pairs = Table.create(TABLE_NAME, schema=[ HashKey('key')],
     throughput={ 'read': 5, 'write': 15, })
  except JSONResponseError:
    print "The table %s still isn't deleted.... waiting" % TABLE_NAME
  else:
    break
    

print "Created table %s" % TABLE_NAME
time.sleep(10)
#  kv_pairs = Table(TABLE_NAME)
#  print "Table %s already exists: connecting to it" % TABLE_NAME


def get ( key ):
  """This function returns the value associated with the key, and an HTTP
status code.  Traps the
exception boto.dynamodb2.exceptions.ItemNotFound if the key isn't present
which would return a 403 error (looking at RFC 2616, that seems to be the
status code that fits the best, but recognize that it is not the best fit).
However, sometimes, get doesn't throw the ItemNotFound exception.  In that
case, the value of value['value'] is None"""
  try:
    value = kv_pairs.get_item(key=key)
  except boto.dynamodb2.exceptions.ItemNotFound:
    return ( None, 403 )
  if value['value'] == None :
    return ( None, 403)
  else :
    return ( value['value'], 200 )


def post ( key, value ):
  """ This subroutine adds the key-value pair to the database, and returns 
200. If the key is already present, then it throws a 
boto.dynamodb2.exceptions.ConditionalCheckFailedException and returns 403"""
  try :
    kv_pairs.put_item(data={'key':key,'value':value})
    return 200
  except boto.dynamodb2.exceptions.ConditionalCheckFailedException:
    return 403

def delete ( key ) :
  """This deletes the key-value pair from the database.  If the key is not
present, then it returns 403, otherwise, it returns 200"""
  try:
    kv_pairs.delete_item(key=key)
    return 200
  except boto.dynamodb2.exceptions.ItemNotFound:
    return 403

def put ( key, new_value ):
  """This updates a key-value pair in the database.  If the key is not
present, then it returns 403, otherwise, it returns 200"""
  try:
    old_value = kv_pairs.get_item(key=key)
  except boto.dynamodb2.exceptions.ItemNotFound:
    return 403
  if old_value['value'] == None :
    return 403
  old_value['value'] = new_value
  try:
    old_value.save(overwrite=True)
# Sometimes, save raises a ValidationException, I don't know why
# According to https://sourcegraph.com/github.com/boto/boto/symbols/python/boto/opsworks/exceptions/ValidationException
# ValidationException inherits from JSONResponseError
  except JSONResponseError:
    print "Something went wrong updating the database.  ValidationcwException was\
raised."
    print "The type of old_value is "+str(type(old_value))
    return 500		# I hate to do this
  return 200

if __name__ == "__main__" :
  check_dict = {}   # This dictionary is used to verify that the database
			# is working correctly

  def test_get( key ):
    print "Getting key %s from database" % key
    value = get ( key )
    if key in check_dict :
      print "The value for key %s is %s" % ( key, value )
      assert value[0] == check_dict[key]
      assert value[1] == 200
    else :
      print "key %s does not exist in database" % key
      assert value[0] == None
      assert value[1] == 403


  def test_post( key, value ):
    print "Inserting key %s with value %s" % ( key, value )
    status = post ( key, value )
    if key not in check_dict:
      assert status == 200
      check_dict[key] = value
# Verify that the key really inserted the value into the database
      assert value == get ( key )[0]
    else:
      print "Tried to insert a key that was already in the database"
      assert status == 403
      
  def test_delete ( key ):
    print "Testing deleting key %s from the database" % key
    status = delete ( key )
    if key in check_dict :
      print "key-value pair was deleted"
      assert status == 200
      del check_dict[key]
# Verify that the key is really gone.  This should fail
      status = get ( key )
      assert status == 403
    else:
      print "The key was never in the database"
      assert status == 200

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
 
  
  while True:
    try:
      test_post("Roger", 17)
    except JSONResponseError:
      print "Trying to insert a key-value pair failed.  Perhaps the database isn't ready yet"
      time.sleep(5)
    else:
      print "The database is ready now"
      break
  test_get("Roger")
  test_post("Eric", 20)
  test_post("Karen", 204)
  test_post("Janie", 12)
  test_get("Janie")
  test_put("Janie", -3)
  test_get("Janie")
  test_get("Randall")
  test_put("Randall", 3421)
  test_delete("Randall")
  test_delete("Randall")


