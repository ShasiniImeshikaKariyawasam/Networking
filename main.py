import signal # Allow socket destruction on Ctrl+C
import sys

def shutdownServer(sig, unused):
    """
    Shutsdown server from a SIGINT recieved signal
    """
    server.shutdown()
    sys.exit(1)

signal.signal(signal.SIGINT, shutdownServer)
server = server()
server.start()
print("Press Ctrl+C to shut down server.")
