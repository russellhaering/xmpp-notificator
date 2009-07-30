import sys
sys.path.append('/wokkel')
from twisted.words.xish import domish
from wokkel.subprotocols import XMPPHandler
from wokkel.xmppim import MessageProtocol, AvailablePresence

"""
An Example Notification Element:

<notification host='zeppelin' source='irssi'>
  <summary>Something Happened</summary>
  <body>Some Detail About What Happened</body>
</notification> 
"""

class NetworkNotifyProtocol(MessageProtocol):
    def __init__(self, output, hostname, targetjid, *args, **kwargs):
        self.output = output
        self.hostname = hostname
        self.targetjid = targetjid
        MessageProtocol.__init__(self, *args, **kwargs)

    def connectionInitialized(self):
        self.xmlstream.addObserver('/message', self.onMessage)

    def connectionMade(self):
        print "Connected!"
        #self.send(AvailablePresence())

    def connectionLost(self, reason):
        print "Disconnected!"

    def onMessage(self, message):
        print str(message)

        if hasattr(message, "body") and hasattr(message.body, "notification"):
            notification = message.body.notification
            print "Notification Received"
            print notification.toXml()
            self.output.notify(str(notification.summary), str(notification.body), notification['host'], notification['app'])

    def sendNotification(self, summary, body, app):
        message = domish.Element((None, 'message'))
        message['to'] = self.targetjid
        message.addElement('notification')
        notification = message.notification
        notification['host'] = self.hostname
        notification['app'] = app
        notification.addElement('summary', content=summary)
        notification.addElement('body', content=body)
        print "Sending Notification"
        print message.toXml()
        self.send(message)
