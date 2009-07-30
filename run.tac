import sys
import os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)
sys.path.append(os.path.join(HERE, 'wokkel'))
from twisted.application import service
from twisted.words.protocols.jabber import jid
from wokkel.client import XMPPClient
from nnprotocol import NetworkNotifyProtocol
from textoutput import TextNotificationOutput as NotificationOutput
import settings

application = service.Application("echobot")

xmppclient = XMPPClient(jid.internJID(settings.login + '/' + settings.host), settings.password)
xmppclient.logTraffic = False
output = NotificationOutput()
notifier = NetworkNotifyProtocol(output, settings.host, settings.login)
notifier.setHandlerParent(xmppclient)
notifier.sendNotification('A Summary', 'Some body text', 'Network Notification Daemon')
xmppclient.setServiceParent(application)
