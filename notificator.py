from twisted.internet import gtk2reactor
gtk2reactor.install()
from twisted.internet import reactor
from twisted.words.protocols.jabber import jid
from twisted.application import service
from wokkel.xmppim import MessageProtocol, AvailablePresence
from wokkel.client import XMPPClient
from twisted.scripts import twistd
from keepalive import KeepAlive
import pynotify

# Settings
username = 'user'
domain = 'jabber.org'
password = 'somepass'


class NotificationProtocol(MessageProtocol):
    def connectionMade(self):
        print "Connected!"
        self.send(AvailablePresence())

    def onMessage(self, msg):
        # TODO: Clean up this 'if'
        if msg["type"] == 'chat' and hasattr(msg, "body") and msg.body:
            print str(msg.body)
            notification = pynotify.Notification("Alert", str(msg.body))
            notification.show()

if __name__ == '__main__':
    pynotify.init("XMPP Notificator")
    xmppclient = XMPPClient(jid.internJID(username + "@" + domain + "/notificator"), password)
    mynotificator = NotificationProtocol()
    mynotificator.setHandlerParent(xmppclient)
    KeepAlive().setHandlerParent(xmppclient)
    xmppclient.startService()
    reactor.run()
