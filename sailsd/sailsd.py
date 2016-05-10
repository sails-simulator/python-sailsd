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

            >>> sailsd.request('speed')
            {'speed': 4.59422737529291
            >>> sailsd.request('heading', 'latitude')
            {'heading': 0.7459227808181, 'latitude': 0.004578511779640}
        '''
        return self._send_message_dict({'request': attributes})

    def set(self, **kwargs):
        '''
        Set attributes in sailsd.

            >>> sailsd.set(rudder_angle=0.2)
            {}
            >>> sailsd.set(latitude=0)
            {}

        The attributes you are likely to be able to set are:

            - ``latitude``
            - ``longitude``
            - ``sail-angle``
            - ``heading``
            - ``rudder-angle``
            - ``wind-speed``
            - ``wind-angle``

        but there could be others.
        '''
        set_values = {k.replace('_', '-'):v for k, v in kwargs.items()}
        return self._send_message_dict({'set': set_values})
