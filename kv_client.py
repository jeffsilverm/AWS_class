#! /usr/bin/env python
#
#
import random
import time
import sys
from urllib import urlopen


class Text(object) :
  """Creates a dictionary from a text file, and has methods to return random
words from the dictionary"""

  def __init__(self, filename):
    """This method creates and populates the dictionary"""
    self.d = {}
    f = open(filename, "r")
    corpus = f.read()
    f.close()
    corpus_list = corpus.split()
    self.counter = 0
    for w in corpus_list :
      self.d[self.counter] = w
      self.counter = self.counter + 1
    return

  def get_dict_size(self):
    return self.counter

  def get_word(self, idx ):
    return d[idx]

  def delete_word(self, idx ):
    d[idx] == None
    return
  

  def random_word( self ):
    """This method returns a random word from the dictionary"""
    i = random.randrange(self.counter)
    w = self.d[i]
    return w
    
class Server(object):
  """This class implements an interface to the server"""
  
  def __init__( name, port ):

  def get_word(

    url = "http://%s:%s" % (name, port)
    doc = urlopen(url).read()

    
  def call_server ( idx, op, text, expected_result=None ):
    """This method interacts with the server"""
    if op == 0 :
      w = self.get_word( idx )
      if w != expected_result :
        raise ValueError( "The server returned %s but should have returned %s" % \
                          (w, expected_result)
    elif op == 1 :
      self.put_word ( idx, word )
    elif op == 2 :
      self.delete_word ( idx )
      text.delete_word( idx )
    
    
    



if __name__ == "__main__" :
  answers = {}
  text = Text("pg158.txt")
  server_name = sys.argv[0]
  server_port = sys.argv[1]
  print "Forming a connection on http://%s:%s" % ( server_name, server_port )
  server = Server( server_name, server_port )
# Development test
  print "Hit control-C when satisfied that this works"  
#  while True:
#    print text.random_word()
  idx = random.randrange(text.counter)
  try :
    w = call_server( idx, 0, text, get_word(idx) )
  except ValueError:
    print "Populating the server with a corpus"
    server.populate_server( text )
  for i in range(1000):
    op = random.randrange(3)
    idx = random.randrange(text.counter) 
    call_server ( idx, op, text, get_word{idx) )
      

 
