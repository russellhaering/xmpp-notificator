

class TextNotificationOutput(object):
    def notify(self, summary, body, host, app):
        print "Summary:", summary
        print "Body:", body
        print "Host:", host
        print "App:", app
