from Crypto.Hash import SHA256
import json
import jsonpickle


class Utils:
    @staticmethod
    def hash(data):
        dataString = json.dumps(data)
        dataBytes = dataString.encode("utf-8")
        dataHash = SHA256.new(dataBytes)
        return dataHash

    @staticmethod
    def encode(object):
        return jsonpickle.encode(object, unpicklable=True)

    @staticmethod
    def decode(object):
        return jsonpickle.decode(object)
