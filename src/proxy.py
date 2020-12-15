# std imports
import requests
import socket
# local imports
from logger import logger
from request_server import RequestServer


class Proxy:
    """
    A Proxy which uses the local recursive resolver,
    if the requested name end with a KNOWN_ENDING.
    For unknown name endings a normal DNS lookup will be used.
    """

    KNOWN_ENDINGS = ("fuberlin", "telematik")
    REC_RES_ADDRESS = ("127.0.0.10", 53053)

    @classmethod
    def _resolve_locally(cls, requested_server: str) -> str:
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        client_sock.sendto(requested_server.encode(), Proxy.REC_RES_ADDRESS)
        data, _ = client_sock.recvfrom(4096)

        # TODO: Get DnsMessage from data and get ip addr. and return it


        return ""

    def __init__(self, ip_address: str = "127.0.0.100", port: int = 80):
        self.server = RequestServer(
            ip_address, port, self.handle_request, use_udp=False
        )

    def handle_request(self, request: str) -> str:
        """
        Handles a HTTP GET request, for which the name is passed
        - e.g. 127.0.0.1/my.domain will look for 'my.domain'.

        """
        header = request.split("\n")[0]
        requested_server = header.split(" ")[1][1:]
        logger.log(f"Proxy got request for {requested_server}.", flush=True)
        if requested_server.split(".")[-1] in Proxy.KNOWN_ENDINGS:
            requested_server = Proxy._resolve_locally(requested_server)
        resp = requests.get(f"http://{requested_server}")
        return resp.text

    def run(self) -> None:
        logger.log("----------\nStarting Proxy", flush=True)
        self.server.open_socket()
        self.server.run()

    def stop(self) -> None:
        """
        Stops listening for requests.
        The socket won't be removed.
        """
        self.server.stop_listening()
