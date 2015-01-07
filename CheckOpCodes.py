__author__ = 'elichai2'

import transactionTools
import bitcoin
import bitcoin.rpc


def _check_OP_CODE(rawtx):
    CODE = 'OP_RETURN'
    if str(rawtx.vout[0]).find(CODE) > 0:
        print "This transaction contains the non-safe OP_CODE: " + CODE
        return True
    return False

mytx = 'eb31ca1a4cbd97c2770983164d7560d2d03276ae1aee26f12d7c2c6424252f29'
proxy = bitcoin.rpc.Proxy()
rawtx = transactionTools.getraw(proxy, mytx)
_check_OP_CODE(rawtx)