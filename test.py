from multiaddr import MultiAddress

ma = MultiAddress("/ip4/127.0.0.1/udp/1234")

print ma
print ma.as_bytes().__repr__()

ma2 = MultiAddress(ma.as_bytes())

print ma2
print ma2.as_bytes().__repr__()
