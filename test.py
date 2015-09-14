from multiaddr import MultiAddress

ma = MultiAddress("/ip6/1fff:0:a88:85a3::ac1f/tcp/1234")

print ma
print ma.as_bytes().__repr__()

ma2 = MultiAddress(ma.as_bytes())

print ma2
print ma2.as_bytes().__repr__()
