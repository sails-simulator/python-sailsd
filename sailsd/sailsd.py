import json
import socket

class Sailsd(object):
    '''
    Low-level control to the sailsd API. Not much is defined here, just direct
    interaction to the API.
    '''
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

    def request(self, *attributes):
        '''
        Request one or more attribute from sailsd. These should be the names
        of each attribute as a string, for example:

            >>> sailsd.request('latitude')
        '''
        return self._send_message_dict({'request': attributes})

    def set(self, **kwargs):
        set_values = {k.replace('_', '-'):v for k, v in kwargs.items()}
        return self._send_message_dict({'set': set_values})
