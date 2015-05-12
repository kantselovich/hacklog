from zope.interface import implements

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet

from hacklog.server import SyslogServer, SyslogReader 


class Options(usage.Options):
    optParameters = [["config", "c", 'conf/server.conf', "path to configuration file."]]


class MyServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = "hacklog"
    description = "Syslog server for detection of compromised user accounts"
    options = Options

    server = SyslogServer()

    def makeService(self, options):
        """
        Construct a UDP Server
        """
        self.server.config_file = options['config']
 
        self.server.start()
	self.server.init()

	return internet.UDPServer(self.server.port, SyslogReader())


# Now construct an object which *provides* the relevant interfaces
# The name of this variable is irrelevant, as long as there is *some*
# name bound to a provider of IPlugin and IServiceMaker.

serviceMaker = MyServiceMaker()
