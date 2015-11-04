#!/usr/bin/env python

import sys
sys.path.append("/usr/lib/hive/apache-hive-1.2.1-bin/lib/py")
from hive_service import ThriftHive
from hive_service.ttypes import HiveServerException
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:
    transport = TSocket.TSocket('localhost', 9083)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    client = ThriftHive.Client(protocol)
    transport.open()

#    client.execute("CREATE TABLE r(a STRING, b INT, c DOUBLE)")
#    client.execute("LOAD TABLE LOCAL INPATH '/path' INTO TABLE r")
    client.execute("SELECT * FROM viki.user_attributes limit 1")
    while (1):
      row = client.fetchOne()
      if (row == None):
        break
      print row
#    client.ExecuteStatement("SELECT * FROM r")
    print client.fetchAll()

    transport.close()

except Thrift.TException, tx:
    print '%s' % (tx.message)
