__author__ = 'elichai2'

from bitcoin.rpc import Proxy
from bitcoin.core import (lx, b2lx, b2x, x)
from bitcoin.wallet import (CBitcoinAddress, P2PKHBitcoinAddress)
from collections import namedtuple

BlackList = namedtuple("BlackList", ['start', 'end', 'name'])
blacklist = [BlackList(0x06f1b6, 0x06f1b6, "SatoshiDice"),
             BlackList(0x74db37, 0x74db59, "BetCoin Dice"),
             BlackList(0xc4c5d7, 0xc4c5d7, "CHBS"),
             BlackList(0x434e54, 0x434e54, "Counterparty"),
             BlackList(0x069532, 0x069532, "SatoshiBones"),
             BlackList(0x06c06f, 0x06c06f, "SatoshiBones"),
             BlackList(0xda5dde, 0xda5dde, "Lucky Bit")]
Mytx = "c07379db7e6ff5facd9b943cf15ed4fc515259b47ae80d3d3aecdb022a894922"
proxy = Proxy()

Mytx = proxy.getrawtransaction(lx(Mytx))
for vout in Mytx.vout:
    pubkey = vout.scriptPubKey
    address = b2lx(CBitcoinAddress.from_scriptPubKey(pubkey))
    address = "".join(map(str.__add__, address[-2::-2], address[-1::-2]))
    #print address
    print hex(int("06c06f6d92abacec42e8126f9f15649b931e0b27", 16))
    address = int(address, 16)
    print hex(address)
    for bl in blacklist:
        if hex(bl.start) <= hex(address) <= hex(bl.end):
            print "This address use by: " + bl.name