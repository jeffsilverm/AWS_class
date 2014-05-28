!# /usr/bin/env python
#
# This uses web.py, see http://webpy.org/ for details
import web
from web import form
import kv_pair

render = web.template.render('templates/')

urls = (
    '/(.*)', 'any_url'
)
app = web.application(urls, globals())

my_form = 

class any_url:        
    def GET(self, name):
        if not name: 
            name = 'World'
        return 'Hello, ' + name + '!'

if __name__ == "__main__":
    app.run()
