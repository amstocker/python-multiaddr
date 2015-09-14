from multiaddr import MultiAddress

ma = MultiAddress("/ip4/85.214.153.147/tcp/4001/ipfs/QmerTTan8gkTEugcb4DmFpAw8Z7bkDQfhoGh6AHzQaqD1Y")

print ma
print ma.as_bytes().__repr__()

ma2 = MultiAddress(ma.as_bytes())

print ma2
print ma2.as_bytes().__repr__()
