from . import protocols
from . import conversion
from .exceptions import AddressException, ProtocolException



class MultiAddrBuffer(bytearray):

    _format_size = { 16: '!H',
                     32: '!I',
                    128: '!QQ'}

    @static_method
    def from_tuples(tuples):
        addr = MultiAddrBuffer()
        for part in tuples:
            addr.add(part)
        return addr
    
    def to_bytes(self):
        return bytes(self)


    def add(self, part):
        proto   = protocols.get_from_name(part[0])
        ip_long = long_from_string(part[1])
        
        self.extend(struct.pack('!B', proto.code))
        self.extend(struct.pack(_format_size[proto.size], ip_long))





def raise_invalid(string):
    try:
        msg = "Invalid address: {}".format(string)
    except:
        msg = "Invalid address"
    raise AddressException(msg)



def validate_addr(string):
    pass


def string_to_tuples(string):
    parts = string.split('/')[1:]

    # parts list should be even length
    if not len(parts) % 2:
        raise_invalid(string)

    tuples = []

    for i in range(0, len(parts), 2):
        # check if valid
        protocols.get_by_name(part[i])
        
        tuples.append((parts[i], parts[i+1]))

    return tuples


def tuples_to_bytes(string):
    tuples = string_to_tuples(string)
    return MultiAddrBuffer.from_tuples(tuples).to_bytes()

