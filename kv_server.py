#! /usr/bin/env python
#
from __future__ import print_function   # Defines the print function
# Impoprt kv_pair first because module web redirects stdout
import kv_pair
# This uses web.py, see http://webpy.org/ for details
import web
from web import form
import sys
from urlparse import urlparse
web.config.debug = False


def warning(*objs):
  print("WARNING: ", *objs, file=sys.stderr)
def info(*objs):
  print("INFORMATIONAL: ", *objs, file=sys.stderr)

render = web.template.render('templates/')

urls = (
    '/(.*)', 'any_url'
)
app = web.application(urls, globals())

register_form = form.Form(
    form.Textbox("name", description="name"),
    form.Textbox("value", description="value"),
    form.Button("submit", type="submit", description="submit") )

class any_url:        
  def GET(self, name):
    """This function has to parse the name looking for key-value pairs.  The
key-value pairs are delimited from the locator"""
    info("Locator name is %s" % name )
# From http://webpy.org/cookbook/input
    user_data = web.input()
    info("The type of user_data is", type(user_data))
    info("The key is %s" % user_data.key)
    value = kv_pair.get(name)
    info("Return status is %d" % value[1])
    if value[0] == None :
      warning("A value for locator %s was not found" % name)
      return "A value for locator %s was not found" % name
    else :
      info("A value for locator %s was not found" % name)
      return "found value %s for locator %s" % name


  def POST(self, arg):
    info(("called POST with arg type is %s, arg is" % type(arg)), arg)
    user_data = web.data() # you can get data use this method
    info("The type of user_data is", type(user_data))
    if type(user_data) == type('str') :
      info("user_data is a string %s" % user_data)
    parameter = user_data.split("=")
    info("The key is %s, the value is %s" % (parameter[0], parameter[1] ))
    kv_pair.put(parameter[0], parameter[1] )
    return "Inserted value %s at key %s" % (parameter[0], parameter[1] )

if __name__ == "__main__":
  info("Starting the application")
  app.run()
