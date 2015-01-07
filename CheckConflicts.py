#!/usr/bin/python
__author__ = 'elichai2'

import bitcoin
bitcoin.SelectParams("mainnet")
import bitcoin.rpc
import time
import argparse
import transactionTools
proxy = bitcoin.rpc.Proxy()
from bitcoin.core import b2lx
import sys


def _generate_mempool(tx):
    mempool = set()
    mempoolDic = dict()

    for i in range(3):
        mempool = mempool.union(set(proxy.getrawmempool()))
        time.sleep(1)
    mempool = list(mempool)
    for txid in mempool: #print b2lx(txid)
        rawtx = transactionTools.getraw(proxy, txid)
        for input in rawtx.vin:
            mempoolDic[input] = txid
    return mempoolDic


def _check_conflicted(mempool, myrawtx, mytxid):
    for input, txid in mempool.iteritems():
        for myinput in myrawtx.vin:
            print '\nmy:'
            print myinput.prevout
            print '\nhis:'
            print input.prevout
            if myinput.prevout == input.prevout and txid != mytxid:
                print "Your transaction is conflicted with this one: " + b2lx(txid)
                return txid
    return None


parser = argparse.ArgumentParser(description="Check if there are any conflicted"
                                             "transaction in the mempool")
parser.add_argument('TrantasctionID', help='The transactionID '
                                           'of the transaction you want to check', type=str)
parser.add_argument('-t', '--testnet', help='Use the Testnet instead of the Mainnet',
                    action="store_true", dest='testnet')
parser.add_argument('--conf', help='Specify configuration file (default: bitcoin.conf)',
                    action='store', type=str, dest='conf')
args = parser.parse_args()
if args.testnet:
        bitcoin.SelectParams("testnet")
if args.conf:
    try:
        proxy.__init__(btc_conf_file=args.conf)
    except Exception, e:
        print e
        sys.exit(0)

myrawtx = transactionTools.getraw(proxy, args.TrantasctionID)
mempool = _generate_mempool(myrawtx)

result = _check_conflicted(mempool, myrawtx, args.TrantasctionID)

if result:
    print b2lx(result)
else:
    print 'No conflicts'
"""
3. get mempool from other nodes.
"""

"""
print b2lx(myrawtx.vin[0].prevout.hash)
print myrawtx.vin[0].prevout
print transactionTools.getraw(proxy, '1638a64e571a2be44aff38e45f53869c74f04331e1bf7d0d69edb86e143e501f')
"""
