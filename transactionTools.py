__author__ = 'elichai2'

import bitcoin
from bitcoin.core import (lx, x)
import sys


def getraw(proxy, mytx):

    try:
            mytx = proxy.getrawtransaction(lx(mytx))

    except Exception, e:
        if str(e) == 'Proxy.getrawtransaction(): No information available about transaction (-5)':
            print "The transaction you entered isn't vaild, or haven't got to the mempool yet.\n" \
                "If you sure it's vaild try again in 10-15 seconds"
            sys.exit(0)

        if str(e) == 'Non-hexadecimal digit found':
            try:
                mytx = proxy.getrawtransaction(mytx)
            except:
                if str(e) == 'Proxy.getrawtransaction(): No information available about transaction (-5)':
                    print "The transaction you entered isn't vaild, or haven't got to the mempool yet.\n" \
                          "If you sure it's vaild try again in 10-15 seconds"
                    sys.exit(0)
                else:
                    print e
                    sys.exit(0)

        else:
            print e
            sys.exit(0)
    try:
        bitcoin.core.CheckTransaction(mytx)
    except Exception, e:
        print e

    return mytx
