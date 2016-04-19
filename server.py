import threading, webbrowser, cgi, BaseHTTPServer, SimpleHTTPServer, os, sys, json
from time import gmtime, strftime
from subprocess import *

PORT = 8080
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        print "Port is not an int. Defaulting to 8080"
        PORT = 8080

LOG_FILE_PREFIX = "out"
if len(sys.argv) > 2:
  LOG_FILE_PREFIX = sys.argv[2]

def start_server():
    server_address = ("", PORT)
    server = BaseHTTPServer.HTTPServer(server_address, DebugServerHandler)
    server.serve_forever()

class DebugServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    # Server methods
    def getPostData(self):
    
      postvars = {}
      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      if ctype == 'multipart/form-data':
          postvars = cgi.parse_multipart(self.rfile, pdict)
      elif ctype == 'application/x-www-form-urlencoded':
          length = int(self.headers.getheader('content-length'))
          postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)

      return postvars 

    def end_headers(self):
      SimpleHTTPServer.SimpleHTTPRequestHandler.end_headers(self)

    def do_POST(self):
      # Handle the command from the web client
      content_len = int(self.headers.getheader('content-length', 0))
      post_body = self.rfile.read(content_len)
      jsonObj = json.loads(post_body)
      time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
      for (k, v) in jsonObj.iteritems():
        with open("%s.%s.log" % (LOG_FILE_PREFIX, k), "a+") as f:
          f.write("%s, %s\n" %(time, v))

      # Process response and headers
      self.send_response(200)
      self.send_header( "Access-Control-Allow-Origin", "*" )
      self.end_headers()


if __name__ == "__main__":
    print( "Started web server on port: %s" % (PORT))
    start_server()
