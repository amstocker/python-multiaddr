from socket import AF_INET6, inet_aton, inet_ntoa, inet_ntop, inet_pton
import struct

from . import protocols



 ########
 # IPv4 #
 ########

def ip4_string_to_bytes(string):
    """
    Converts an ip4 address from string representation to a bytes object.
    """
    return inet_aton(string)


def ip4_bytes_to_long(ip4):
    """
    Converts an ip4 address from byte representation to a long.
    """
    return struct.unpack('!L', ip4)[0]


def ip4_long_to_bytes(ip4):
    """
    Converts an ip4 address from long representation to a bytes object.
    """
    return struct.pack('!L', ip4)


def ip4_bytes_to_string(ip4):
    """
    Converts an ip4 address from long representation to a string.
    """
    return inet_ntoa(ip4)



 ########
 # IPv6 #
 ########

def ip6_string_to_bytes(string):
    """
    Converts an ip6 address from string representation to a bytes object.
    """
    return inet_pton(AF_INET6, string)


def ip6_bytes_to_long(ip6):
    """
    Converts an ip6 address from byte representation to a long.
    """
    a, b = struct.unpack('!QQ', ip6)
    return (a << 64) | b


def ip6_long_to_bytes(ip6):
    """
    Converts an ip6 address from 16 byte long representation to a bytes object.
    """
    a, b = ip6 >> 64, ip6 % (2<<64)
    return struct.pack('!QQ', a, b)


def ip6_bytes_to_string(ip6):
    """
    Converts an ip6 address from long representation to a string.
    """
    return inet_ntop(AF_INET6, ip6)



 ########
 # Misc #
 ########

def port_to_bytes(port):
    """
    Converts a port number to an unsigned short.
    """
    return struct.pack('!H', int(port))


def port_from_bytes(port):
    """
    Converts a port number from a bytes object to an int.
    """
    return struct.unpack('!H', port)[0]


def proto_to_bytes(code):
    """
    Converts a protocol code into an unsigned char.
    """
    return encode_uvarint(code)


def proto_from_bytes(code):
    """
    Converts a protocol code from a bytes oject to an int.
    """
    return decode_uvarint(code)[0]



 ###############################
 # MultiHash Encoding/Decoding #
 ###############################

B58_ALPHABET = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'

        
def b58encode(num):
    """
    Returns num in a base58-encoded string.
    """
    encode = ''
    if (num < 0):
        return ''
    while (num >= 58):  
        mod = num % 58
        encode = B58_ALPHABET[mod] + encode
        num = num / 58
    if (num):
        encode = B58_ALPHABET[num] + encode
    return encode


def b58decode(s):
    """
    Decodes the base58-encoded string s into an integer.
    """
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * B58_ALPHABET.index(char)
        multi = multi * 58
    return decoded


# ref:  https://developers.google.com/protocol-buffers/docs/encoding?hl=en
def encode_uvarint(value):
    buf = bytearray()
    bits = value & 0x7f
    value >>= 7
    while value:
        buf.append(chr(0x80|bits))
        bits = value & 0x7f
        value >>= 7
    buf.append(chr(bits))
    return bytes(buf)


def decode_uvarint(buf):
    size = result = shift = 0
    while True:
        b = ord(buf[size])
        result |= ((b & 0x7f) << shift)
        size += 1
        if not (b & 0x80):
            return result, size
        shift += 7


def multihash_to_bytes(string):
    """
    Converts a multihash string as an unsigned varint.
    """
    return encode_uvarint(b58decode(string))


def multihash_to_string(mhash):
    """
    Converts a uvarint encoded multihash into a string.
    """
    return b58encode(decode_uvarint(mhash)[0])




def to_bytes(proto, string):
    """
    Properly converts address string or port to bytes based on given protocol.
    """
    if proto.name == protocols.IP4:
        addr = ip4_string_to_bytes(string)
    elif proto.name == protocols.IP6:
        addr = ip6_string_to_bytes(string)
    elif proto.name == protocols.TCP:
        addr = port_to_bytes(string)
    elif proto.name == protocols.UDP:
        addr = port_to_bytes(string)
    elif proto.name == protocols.IPFS:
        addr = multihash_to_bytes(string)
    else:
        msg = "Protocol not implemented: {}".format(proto.name)
        raise AddressException(msg)
    return addr


def to_string(proto, addr):
    """
    Properly converts bytes to string or int representation based on the given
    protocol.  Returns string representation of address and the number of bytes
    from the buffer consumed.
    """
    if proto.name == protocols.IP4:
        size = proto.size//8
        string = ip4_bytes_to_string(addr[:size])
    elif proto.name == protocols.IP6:
        size = proto.size//8
        string = ip6_bytes_to_string(addr[:size])
    elif proto.name == protocols.TCP:
        size = proto.size//8
        string = port_from_bytes(addr[:size])
    elif proto.name == protocols.UDP:
        size = proto.size//8
        string = port_from_bytes(addr[:size])
    elif proto.name == protocols.IPFS:
        varint, size = decode_uvarint(addr)
        string = b58encode(varint)
    else:
        msg = "Protocol not implemented: {}".format(proto.name)
        raise AddressException(msg)
    return string, size
