import threading, webbrowser, cgi, BaseHTTPServer, SimpleHTTPServer, os, sys, json
from subprocess import *

PORT = 8080

if len( sys.argv ) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print "Port is not an int. Defaulting to 8080"
        PORT = 8080

def start_server():
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, DebugServerHandler)
    server.serve_forever()

class DebugServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    # Server methods
    def getPostData(self):
      result = {}
      form = cgi.FieldStorage(
          fp=self.rfile,
          headers=self.headers,
          environ={'REQUEST_METHOD':'POST',
                   'CONTENT_TYPE':self.headers['Content-Type'],
      })

      for item in form.list:
        result[item.name] = item.value
      return result

    def end_headers(self):
      SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

    def do_POST(self):
      try:
        # Handle the command from the web client
        post = self.getPostData()
        for k,v in post.iteritems():
            print(k, v)

        # Process response and headers
        self.send_response(200)
        self.end_headers()
      except Exception as e:
        print("Could not write debug to file")


if __name__ == "__main__":
    print( "Started web server on port: %s" % (PORT))
    start_server()
