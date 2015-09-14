
from .exceptions import ProtocolException



class Protocol(object):
    
    def __init__(self, name, code, size):
        self._name = name
        self._code = code
        self._size = size

    @property
    def name(self):
        return self._name

    @property
    def code(self):
        return self._code

    @property
    def size(self):
        return self._size



__protocol_names = {
         'ip4' : Protocol( 'ip4',   4,  32),
         'tcp' : Protocol( 'tcp',   6,  16),
         'udp' : Protocol( 'udp',  17,  16),
        'dccp' : Protocol('dccp',  33,  16),
         'ip6' : Protocol( 'ip6',  41, 128),
        'sctp' : Protocol('sctp', 132,  16)
        }

__protocol_codes = dict([(p.code, p) for p in __protocol_names.values()])



def get_by_code(code):
    try:
        return __protocol_codes[int(code)]
    except:
        try:
            msg = "Invalid protocol code: {}".format(code)
        except:
            msg = "Invalid protocol code"
        raise ProtocolError(msg)


def get_by_name(name):
    try:
        return __protocol_names[str(name)]
    except:
        try:
            msg = "Invalid protocol name: {}".format(name)
        except:
            msg = "Invalid protocol name"
        raise ProtocolError(msg)
