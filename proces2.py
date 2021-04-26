from spyne import Application, rpc, ServiceBase,String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import socket
import sys
import time


class HelloWorldService(ServiceBase):
    message ="pusta"
    @rpc(String ,  _returns=String)
    def writeMsg(ctx, msg):
        print('\t To ja proces 2. Mam wiadomosc:' +msg )
        try:
            s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)            
            s.sendto(msg.encode('utf-8'),('127.0.0.1',12345))   
            message = msg
            s.close()

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('localhost', 12345)
            sock.connect(server_address)
            sock.sendall(message)
            data = sock.recv(100)
            print >>sys.stderr, 'received "%s"' % data
            sock.close()
        except:
            print 'error:',sys.exc_info()[1]
            s.close()
        print "\tElo to ja proces, wysylam wiadomosc wyzej 2\n"
        return ''
    
    # def clnt():
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     server_address = ('localhost', 12345)
    #     sock.connect(server_address)

    #     try:
    #         sock.sendall(message)
    #         data = sock.recv(100)
    #         print >>sys.stderr, 'received "%s"' % data

    #      finally:
    #         sock.close()


application = Application([HelloWorldService],
    tns='ppr.hello',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8080, wsgi_app)
    server.serve_forever()
