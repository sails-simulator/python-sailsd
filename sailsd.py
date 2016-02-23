import json
import socket

class Sailsd(object):
    def _send_message_bytes(self, msg):
        #TODO assert that msg is bytes
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('localhost', 3333))

        response = b''

        try:
            s.sendall(msg)

            amount_received = 0

            while amount_received < 1024:
                data = s.recv(24)
                amount_received += len(data)
                response += data
                if len(data) == 0:
                    break
        finally:
            s.close()

        return response

    def _send_message_dict(self, msg):
        s = json.dumps(msg).encode()
        ret = self._send_message_bytes(s)
        return json.loads(ret.decode('utf-8'))
