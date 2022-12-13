import json


class Message:
    def __init__(self, timestamp, topic, content):
        self.timestamp = timestamp
        self.topic = topic
        self.content = content

    def to_json(self):
        message_format = """
            {
                "timestamp": #TIMESTAMP,
                "topic": "#TOPIC",
                "content": #CONTENT
            }
        """

        message = message_format.replace("#TIMESTAMP", str(self.timestamp))
        message = message.replace("#TOPIC", self.topic)
        message = message.replace(
            "#CONTENT", json.dumps(self.content, indent=2))

        return message.encode('UTF-8')

    @staticmethod
    def from_json(data):
        parsed_data = json.loads(data)

        timestamp = parsed_data['timestamp']
        topic = parsed_data['topic']
        content = parsed_data['content']

        return Message(timestamp, topic, content)
