class Message:
    def __init__(self, sender_endpoint, message_type, data):
        self.sender_endpoint = sender_endpoint
        self.message_type = message_type
        self.data = data
