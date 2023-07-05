# works with both python 2 and 3
from __future__ import print_function
import africastalking


from confluent_kafka import Consumer


def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf


props = read_ccloud_config("client.properties")
props["group.id"] = "python-group-1"
props["auto.offset.reset"] = "earliest"

consumer = Consumer(props)
consumer.subscribe(["topic_0"])


class SMS:
    def __init__(self):
        self.username = "YOUR_USERNAME"
        self.api_key = "YOUR_API_KEY"

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self, message):
        # Set the numbers you want to send to in international format
        recipients = ["+254722386231", "+254730909899"]

        # Set your shortCode or senderId
        sender = "shortCode or senderId"
        try:
            # Thats it, hit send and we'll take care of the rest.
            response = self.sms.send(message, recipients, sender)
            print(response)
        except Exception as e:
            print('Encountered an error while sending: %s' % str(e))

    def consume_messages(self):
        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is not None and msg.error() is None:
                    message = "{value:12}".format(
                        value=msg.value().decode('utf-8'))
                    print(message)
                    self.send(message)
        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()


if __name__ == '__main__':
    SMS().consume_messages()
