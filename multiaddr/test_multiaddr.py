from ipfstools.multiaddr import MultiAddress

ma = MultiAddress("/ip4/127.0.0.1/tcp/4001/ipfs/QmerTTan8gkTEugcb4DmFpAw8Z7bkDQfhoGh6AHzQaqD1Y")

print ma
print len(ma.str_repr)
print ma.as_bytes().__repr__()
print len(ma.as_bytes())

ma2 = MultiAddress(ma.as_bytes())

print ma2
print len(ma2.str_repr)
print ma2.as_bytes().__repr__()
print len(ma2.as_bytes())
