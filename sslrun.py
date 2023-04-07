'''
    This is a file that configures how your server runs
    You may eventually wish to have your own explicit config file
    that this reads from.

    For now this should be sufficient.

    Keep it clean and keep it simple, you're going to have
    Up to 5 people running around breaking this constantly
    If it's all in one file, then things are going to be hard to fix

    If in doubt, `import this`
'''

#-----------------------------------------------------------------------------

import sys
from bottle import run,request,route,run,static_file
from myapp import app
#-----------------------------------------------------------------------------
# You may eventually wish to put these in their own directories and then load 
# Each file separately

# For the template, we will keep them together

import model
import view
import controller
import cherrypy
        
#-----------------------------------------------------------------------------

# It might be a good idea to move the following settings to a config file and then load them
# Change this to your IP address or 0.0.0.0 when actually hosting
host = '0.0.0.0'

# Test port, change to the appropriate port to host
port = 443

# Turn this off for production
debug = True






@app.route('/getkeyword')
def gettarget():
    value=request.query.value
    print(value)
    model.showtrend(value)






cherrypy.tree.graft(app,"/")
cherrypy.server.unsubscribe()
server=cherrypy._cpserver.Server()
server.socket_host="0.0.0.0"
server.socket_port=443
server.ssl_certificate="server.crt"
server.ssl_private_key="server.key"
server.thread_pool=1
server.subscribe()
try:
    cherrypy.engine.start()
    cherrypy.engine.block()
except KeyboardInterrupt:
    cherrypy.engine.stop()


