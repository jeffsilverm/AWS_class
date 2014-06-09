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
SLEEP = 10.0  # seconds

def warning(*objs):
  print("WARNING: ", *objs, file=sys.stderr)
def info(*objs):
  print("INFORMATIONAL: ", *objs, file=sys.stderr)

render = web.template.render('templates/')

urls = (
    '/(.*)', 'any_url'
)
app = web.application(urls, globals())

render = web.template.render('templates')

define_form = form.Form(
    form.Textbox("name", description="name"),
    form.Textbox("value", description="value") )
query_form = form.Form(
    form.Button("insert", type="submit", description="insert"),
    form.Textbox("name", description="name to lookup"),
    form.Button("lookup", type="submet", description="Lookup" ))


    
class any_url:        
  def make_form(self):
    d = define_form()
    return render.define(f)


  def GET(self, name):
    """This function has to parse the name looking for key-value pairs.  The
key-value pairs are delimited from the locator"""
    info("In function GET: Locator name is %s" % name )
# From http://webpy.org/cookbook/input
    user_data = web.input()
#    info("The type of user_data is", type(user_data))
#    info("The attributes of user_data are %s" % dir(user_data))
#    info("The keys attribute of user data is %s" % str(user_data.keys()))
    query_keys = user_data.keys()
# If the query has no locator and no parameters, then it is an initial query
# so generate the form
    if name == "" and len(query_keys) == 0 :
      form_text = self.make_form()
      return form_text
    else :
      query_key = query_keys[0]
      value = kv_pair.get(query_key)
      info("Return status is %d" % value[1])
      if value[0] == None :
        warning("A value for key %s was not found" % query_key )
        raise web.notfound( "A value for key %s was not found\n" % query_key )
      else :
        info("A value for key %s was found" % query_key)
        return "found value %s for key %s\n" % ( value[0], query_key )


  def POST(self, arg):
    info(("called POST with arg type is %s, arg is" % type(arg)), arg)
    user_data = web.data() # you can get data use this method
    info("The type of user_data is", type(user_data))
    if type(user_data) == type('str') :
      info("user_data is a string %s" % user_data)
    parameter = user_data.split("=")
    info("The key is %s, the value is %s" % (parameter[0], parameter[1] ))
    status = kv_pair.put(parameter[0], parameter[1])
    if status == 403 :
      status = kv_pair.post ( parameter[0], parameter[1] )
      if status == 200 :
        return "Inserted key %s  value %s\n" % (parameter[0],parameter[1] )
      else :
        return "Updating and inserting didn't work - something else is wrong"
    elif status == 200 :
      return "Updated key %s  value %s\n" % (parameter[0],parameter[1] )
    else :
      warning("When updating key %key, the status return was %d should be 200" +\
              " or 403" % status )
      return "Something went horribly wrong"

  def DELETE(self, arg):
    info(("called DELETE with arg type is %s, arg is" % type(arg)), arg)
    user_data = web.input()
    query_keys = user_data.keys()
    query_key = query_keys[0]
    info("key is %s" % query_key)
    status = kv_pair.delete(query_key)
    info(("Deleted the K/V pair with key %s, status is %d" % (query_key, status)))
    return

  




    
if __name__ == "__main__":
  info("Starting the server")
  app.run()
