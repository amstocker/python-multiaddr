from . import parse



class MultiAddress(object):
    
    def __init__(self, address):
        self.address = address
        self._bytes = parse.parse_addr(address)

    def __repr__(self):
        return "<{}:{}>".format(self.__class__, self.address)
