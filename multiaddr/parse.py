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

        if proto.name == protocols.IP4:
            addr = conversion.ip4_string_to_bytes(part[1])
        elif proto.name == protocols.IP6:
            addr = conversion.ip6_string_to_bytes(part[1])
        elif proto.name == protocols.TCP:
            addr = conversion.port_to_bytes(part[1])
        elif proto.name == protocols.UDP:
            addr = conversion.port_to_bytes(part[1])
        else:
            msg = "Protocol not implemented: {}".format(proto.name)
            raise AddressException(msg)

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
        # check if valid
        proto = protocols.get_by_name(parts[i])
        
        tuples.append((proto, parts[i+1]))
    
    return tuples


def tuples_to_bytes(tuples):
    """
    Converts a list of tuples corresponding to the parts of a MultiAddress into
    a bytes object.
    """
    return MultiAddrBuffer.from_tuples(tuples).to_bytes()


def parse_addr(string):
    """
    Returns the binary format of a MultiAddress.
    """
    return tuples_to_bytes(string_to_tuples(string))
