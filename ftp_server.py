from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import os

os.makedirs("./fake_mikrotik", exist_ok=True)
os.chmod("./fake_mikrotik", 0o777)

authorizer = DummyAuthorizer()
authorizer.add_user("admin", "password", "./fake_mikrotik", perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer
handler.passive_ports = range(2123, 2130)
handler.masquerade_address = "127.0.0.1"

server = FTPServer(("0.0.0.0", 2122), handler)
server.serve_forever()
