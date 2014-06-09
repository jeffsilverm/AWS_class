#! /usr/bin/env python
#
# This python program implements a simple web server for the kv_pair.py DB
# interface


from cgi import parse_qs, escape
import kv_pair
from wsgiref.simple_server import make_server

def application(environ, start_response):

   method = environ['REQUEST_METHOD']
   if method == "POST" or method == "PUT" :
      response_body = []
# the environment variable CONTENT_LENGTH may be empty or missing
      try:
         request_body_size = int(environ.get('CONTENT_LENGTH', 0))
      except (ValueError):
         request_body_size = 0

# When the method is POST the query string will be sent
# in the HTTP request body which is passed by the WSGI server
# in the file like wsgi.input environment variable.
      request_body = environ['wsgi.input'].read(request_body_size)
      d = parse_qs(request_body)
      print d.keys()
# There should be only one key/value pair in the query
      key = d.keys()[0]
# Always escape user input to avoid script injection
      key = escape(key)
      value = d[key][0]
      value = escape(value)
      if method == "POST" :
         status = kv_pair.post(key, value)
      else :
         status = kv_pair.put(key, value)
      if status == 200:
         status = "200 OK"
      elif status == 403 :
         status = "403 Bad value for key " + key
      else :
         status = str(status)+" Strange"
   elif method == "GET" :
      query_string = environ['QUERY_STRING']
      query_string_list = query_string.split("=")
      if len(query_string_list) == 2 :
         key = query_string_list[1]
         value, status = kv_pair.get( key )
         if status == 200 :
            response_body = ["found %s = %s\n" % (key, value)]
            status = '200 OK'
         else :
            response_body = ["Didn't find %s\n" % key]
            status = "403 Bad value for key " + key
      else :
         response_body = ["Bad request, argument should be 'key=KEY'\n"]
         status = "400 Bad Request"
   elif method == "DELETE" :
      key = environ['QUERY_STRING']
      status = kv_pair.delete( key )
      response_body = ["Deleted %s\n" % key]
      if status == 200:
         status = "200 OK"
      elif status == 403 :
         status = "403 Bad value for key %s\n" % key
      else :
         status = str(status)+" Strange\n"      
   else :
      response_body = ["Bad request"]
      status = '400 Bad request.  Method is %s\n' % method

   response_body = '\n'.join(response_body)+"\n"

   # So the content-lenght is the sum of all string's lengths
   content_length = len( response_body )

   response_headers = [('Content-Type', 'text/plain'),
                  ('Content-Length', str(content_length))]

   start_response(status, response_headers)

# Convert the response body to a list which is processed more efficiently
# by the WSGI code.  Also, there is a bug somewhere.  response_body should be
# a string, not unicode.  Not sure why.
   return [str(response_body)]

httpd = make_server('0.0.0.0', 8081, application)
print "The server is running"
# Now it is serve_forever() in instead of handle_request().
# In Windows you can kill it in the Task Manager (python.exe).
# In Linux a Ctrl-C will do it.
httpd.serve_forever()
