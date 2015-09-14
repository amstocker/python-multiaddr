from . import protocols
from . import conversion
from .exceptions import AddressException, ProtocolException



def raise_invalid(string):
    try:
        msg = "Invalid address: {}".format(string)
    except:
        msg = "Invalid address"
    raise AddressException(msg)



class MultiAddrBuffer(bytearray):

    @staticmethod
    def from_tuples(tuples):
        addr = MultiAddrBuffer()
        for part in tuples:
            addr.add(part)
        return addr
    
    def to_bytes(self):
        return bytes(self)

    def add(self, part):
        proto = part[0]
        addr = conversion.to_bytes(proto, part[1])
        self.extend(conversion.proto_to_bytes(proto.code))
        self.extend(addr)



def string_to_tuples(string):
    """
    Converts a multiaddr string into a list of tuples corresponding to each
    address part.
    """
    parts = string.split('/')[1:]
    
    # parts list should be even length
    if len(parts) % 2:
        raise_invalid(string)

    tuples = []

    for i in range(0, len(parts), 2):
        proto = protocols.get_by_name(parts[i])
        tuples.append((proto, parts[i+1]))
    
    return tuples


def tuples_to_bytes(tuples):
    """
    Converts a list of tuples corresponding to the parts of a MultiAddress into
    a bytes object.
    """
    return MultiAddrBuffer.from_tuples(tuples)


def bytes_to_tuples(addr):
    """
    Converts the binary format of a multiaddr into its string representation.
    """
    tuples = []

    i = 0
    while i < len(addr):
        code = conversion.proto_from_bytes(addr[i])
        proto = protocols.get_by_code(code)
        string = conversion.to_string(proto, addr[i+1:i+1+(proto.size//8)])
        tuples.append((proto, string))

        i += 1+(proto.size//8)

    return tuples


def tuples_to_string(tuples):
    """
    Converts a list of tuples into string representation.
    """
    return '/' + '/'.join(['/'.join((t[0].name, str(t[1]))) for t in tuples])


def string_to_bytes(string):
    """
    Converts a multiaddr string into its binary format.
    """
    return tuples_to_bytes(string_to_tuples(string))


def bytes_to_string(addr):
    """
    Converts a multiaddr in binary format to its string representation.
    """
    return tuples_to_string(bytes_to_tuples(addr))

        
def parse_addr(addr):
    """
    Returns the parsed string and binary formats of a given multiaddr.
    """
    try:
        # If the address given can be decoded into ASCII then it is likely the
        # string representation of a multiaddr.  Otherwise, we assume it is in
        # binary representation.  (We do this because we can't use isinstance
        # to differentiate between a byte string and an ascii string in 2.x)
        addr.decode('ascii')
        valid = True
    except:
        valid = False
    if valid:
        return addr, string_to_bytes(addr)
    else:    
        return bytes_to_string(addr), addr
