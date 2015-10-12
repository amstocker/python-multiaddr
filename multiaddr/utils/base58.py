"""
Base 58 encoding library.
"""
ALPHABET = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'

        
def b58encode(num):
    """
    Returns num in a base58-encoded string.
    """
    encode = ''
    if (num < 0):
        return ''
    while (num >= 58):  
        mod = num % 58
        encode = ALPHABET[mod] + encode
        num = num / 58
    if (num):
        encode = ALPHABET[num] + encode
    return encode


def b58decode(s):
    """
    Decodes the base58-encoded string s into an integer.
    """
    decoded = 0
    multi = 1
    s = s[::-1]
    for char in s:
        decoded += multi * ALPHABET.index(char)
        multi = multi * 58
    return decoded

