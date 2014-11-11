#!/usr/bin/python
__author__ = 'elichai2'

Conflicted = -1
import bitcoin
bitcoin.SelectParams("mainnet")
from bitcoin.rpc import Proxy
from bitcoin.core import lx
import binascii
import time
BTC = 100000000.0
Mytx = "c15e198beb7b4b460c4828a02e7eb32ae0310c2cef9786576f6244e94d2c873d"
proxy = Proxy()

Myrawtx = proxy.getrawtransaction(lx(Mytx))

mempoolHash = set()
mempoolRaw = list()
mempoolHR = dict()
for i in range(1):
    mempoolHash = mempoolHash.union(set(proxy.getrawmempool()))
    print len(mempoolHash)
    time.sleep(1)

mempoolHash = list(mempoolHash)
for txid in mempoolHash:
    mempoolRaw.append(proxy.getrawtransaction(txid).
                    vin[0].prevout)

for i, txid in enumerate(mempoolHash):
    mempoolHash[i] = binascii.hexlify(txid)

mempoolHR = dict(zip(mempoolHash, mempoolRaw))

for key, value in mempoolHR.iteritems():
    if Myrawtx.vin[0].prevout == value:
        Conflicted = key

if Conflicted != -1:
    print "Your transaction is conflicted with this one: " + key

else:
    print "Your transaction seems to be safe"