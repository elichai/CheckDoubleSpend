__author__ = 'elichai2'
import bitcoin
from bitcoin.rpc import Proxy
from bitcoin.core import (lx, b2lx, b2x, x)
from bitcoin.wallet import (CBitcoinAddress, P2PKHBitcoinAddress)
from collections import namedtuple
import argparse
BlackList = namedtuple("BlackList", ['start', 'end', 'name'])
blacklist = [BlackList(0x06f1b6, 0x06f1b6, "SatoshiDice"),
             BlackList(0x74db37, 0x74db59, "BetCoin Dice"),
             BlackList(0xc4c5d7, 0xc4c5d7, "CHBS"),
             BlackList(0x434e54, 0x434e54, "Counterparty"),
             BlackList(0x069532, 0x069532, "SatoshiBones"),
             BlackList(0x06c06f, 0x06c06f, "SatoshiBones"),
             BlackList(0xda5dde, 0xda5dde, "Lucky Bit")]
proxy = Proxy()


def getraw(mytx):

    try:
        mytx = proxy.getrawtransaction(lx(mytx))
    except Exception, e:
        if str(e) == 'Proxy.getrawtransaction(): No information available about transaction (-5)':
            print "The transaction you entered isn't vaild, or haven't got to the mempool yet.\n" \
                "If you sure it's vaild try again in 10-15 seconds"
        else:
            print e
        exit()
    try:
        bitcoin.core.CheckTransaction(mytx)
    except Exception, e:
        print e

    return mytx


def check_output_address(mytx):

    print
    for vout in mytx.vout:
        pubkey = vout.scriptPubKey
        address = b2lx(CBitcoinAddress.from_scriptPubKey(pubkey))
        address = "".join(map(str.__add__, address[-2::-2], address[-1::-2]))
        #print address
        address = int(address, 16)
        for bl in blacklist:
            if hex(bl.start) <= hex(address) <= hex(bl.end):
                print "This address use by: " + bl.name
                return False
    return True

parser = argparse.ArgumentParser(description="Check if one of the outputs or inputs address's are belong to "
                                             "SPAM labeled addresses.")
parser.add_argument('TrantasctionID', help='The transactionID'
                                 ' of the transaction you want to check', type=str)
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
        exit()


rawtx = getraw(args.TrantasctionID)
if check_output_address(rawtx):
    print "Your transaction dosen't send money to SPAM addresses" \
          "or usses inputs from SPAM addresses"