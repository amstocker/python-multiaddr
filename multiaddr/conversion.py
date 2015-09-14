from socket import AF_INET6, inet_aton, inet_ntoa, inet_ntop, inet_pton
import struct



 ########
 # IPv4 #
 ########

def ip4_string_to_bytes(string):
    """
    Converts an ip4 address from string representation to a bytes object.
    """
    return bytes(inet_aton(string))


def ip4_bytes_to_long(ip4):
    """
    Converts an ip4 address from byte representation to a long.
    """
    return struct.unpack('!L', ip4)[0]


def ip4_long_to_bytes(ip4):
    """
    Converts an ip4 address from long representation to a bytes object.
    """
    return bytes(struct.pack('!L', ip4))


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
    return bytes(inet_pton(AF_INET6, string))


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
    return bytes(struct.pack('!QQ', a, b))


def ip6_bytes_to_string(ip6):
    """
    Converts an ip6 address from long representation to a string.
    """
    return inet_ntop(AF_INET6, ip6)



 ########
 # MISC #
 ########

def port_to_bytes(port):
    """
    Converts a port number to an unsigned short.
    """
    return bytes(struct.pack('!H', int(port)))


def port_from_bytes(port):
    """
    Converts a port number from a bytes object to an int.
    """
    return struct.unpack('!H', port)[0]


def proto_to_bytes(code):
    """
    Converts a protocol code into an unsigned char.
    """
    return bytes(struct.pack('!B', int(code)))


def proto_from_bytes(code):
    """
    Converts a protocol code from a bytes oject to an int.
    """
    return struct.unpack('!B', code)[0]
