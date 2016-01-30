from twisted.web import http, proxy
from twisted.internet import reactor
from twisted.python import log
import sys
 
schermo = sys.stdout
 
log.startLogging(open('myproxy.log', 'w'))
 
class MyProxyClient(proxy.ProxyClient):
    def handleHeader(self, key, value):
        s = "Ricevuto header: " + key
        s+= ", " + value
        schermo.write(s + "\n")
        proxy.ProxyClient.handleHeader(self, key, value)
 
class MyProxyClientFactory(proxy.ProxyClientFactory):
    protocol = MyProxyClient
 
class MyProxyRequest(proxy.ProxyRequest):
    protocols = {'http': MyProxyClientFactory}
    ports = {'http': 80}
 
# non è necessario:
#   def process(self):
#       proxy.ProxyRequest.process(self)
 
class MyProxy(proxy.Proxy):
    requestFactory = MyProxyRequest
 
 
f = http.HTTPFactory()
f.protocol = MyProxy
reactor.listenTCP(8080, f)
 
try:
    reactor.run()
except KeyboardInterrupt:
    reactor.stop()
