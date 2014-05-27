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

TABLE_NAME = 'kv_pairs'

conn = DynamoDBConnection()
table_list = conn.list_tables()
# The table_list is a dictionary with a single key, the value of which is
# a list of tables associated with this account.  If TABLE_NAME is not in
# that list, then create the table, otherwise, just connect to it.
if TABLE_NAME not in table_list[u'TableNames'] :
  kv_pairs = Table.create(TABLE_NAME, schema=[ HashKey('key')],
     throughput={ 'read': 5, 'write': 15, })
else :
  kv_pairs = Table(TABLE_NAME)


def get ( key ):
  """This function returns the value associated with the key, and an HTTP
status code.  Traps the
exception boto.dynamodb2.exceptions.ItemNotFound if the key isn't present
which would return a 403 error (looking at RFC 2616, that seems to be the
status code that fits the best, but recognize that it is not the best fit)"""
  try:
    value = kv_pairs.get_item(key=key)
    return ( value['value'], 200 )
  except boto.dynamodb2.exceptions.ItemNotFound:
    return ( None, 403 )


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

def put ( key, new_value )
  """This updates a key-value pair in the database.  If the key is not
present, then it returns 403, otherwise, it returns 200"""
  try:
    old_value = kv_pairs.get_itme(key=key)
  except boto.dynamodb2.exceptions.ItemNotFound:
    return 403
  old_value['value'] = new_value
  old_value.save(overwrite=True)
  return 200

if __name__ == "__main__" :
  check_dict = {}   # This dictionary is used to verify that the database
			# is working correctly

  def test_get( key ):
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
    post ( key, value )
    check_dict[key] = value
# Verify that the key really inserted the value into the database
    assert value = get ( key )[0]

  def test_delete ( key ):
    print "Testing deleting key %s from the database" % key
    status = delete ( key )
    if key in check_dict :
      assert status == 200
      del check_dict[key]
# Verify that the key is really gone.  This should fail
      status = get ( key )
      assert status == 403
      print "key-value pair was deleted"
    else:
      assert status == 403
      print "The key was never in the database"

  def test_put ( key, value ):
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
 

  test_post("Roger", 17)
  test_get("Roger")
  test_post("Eric", 20)
  test_post("Karen", 204)
  test_post("Janie", 12)
  test_get("Janie")
  test_put("Janie", -3)
  test_get("Janie")
  test_get("Michael")
  test_put("Michael", 3421)
  test_delete("Michael")
  test_delete("Michael")


