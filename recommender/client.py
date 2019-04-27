from select import select
from warnings import warn
import socket

class Client(object):
    def __init__(
            self,
            host,
            port,
            timeout = 0.2,
            max_size = 1024
            ):
        self.addr = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timeout = timeout
        self.max_size = max_size

    def record(self, did, pid):
        return self._call('RECR', did, pid, False)

    def recommend(self, did, pid):
        return self._call('RECM', did, pid, True)

    def record_recommend(self, did, pid):
        return self._call('RR', did, pid, True)

    def person_history(self, pid):
        return self._call('PH', '', pid, True)

    def _call(self, method, did, pid, need_response):
        sent = self._send(','.join([method, str(did), str(pid)]))
        if not need_response:
            return sent
        if sent and self._is_ready():
            response = self._recv()
            if len(response) > 0:
                res = response.split(',')
                if res[0] == 'OK':
                    return res[1:]
                warn('Received error response: {}'.format(res[0]))
        return []

    def _send(self, msg):
        return self.sock.sendto(bytes(msg, 'ascii'), self.addr)

    def _recv(self):
        return self.sock.recvfrom(self.max_size)[0].decode('ascii')

    def _is_ready(self):
        rlist, _, _ = select([self.sock], [], [], self.timeout)
        return len(rlist) > 0


