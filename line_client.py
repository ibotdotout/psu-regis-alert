from line import LineClient, LineContact
import ConfigParser
import os


class Line(object):

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

        email = config.get('LINE', 'email')
        password = config.get('LINE', 'password')

        try:
            self.client = LineClient(email, password)
        except:
            print("Line login failed")

    def send(self, target_id, message):

        try:
            target = self.client._client.findContactByUserid(target_id)
            c = LineContact(self.client, target)
            c.sendMessage(message)
        except:
            print("line id not found")

    def exist_id(self, target_id):

        try:
            target = self.client._client.findContactByUserid(target_id)
            result = True if target else False
        except:
            result = False

        return result
