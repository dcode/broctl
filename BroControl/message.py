# Message classes that are used by dbroctld for
# the communication in between different instances

import json
import pybroker


class BBaseMsg(object):
    def __init__(self, mtype):
        self.message = {}
        self.message['type'] = mtype
        self.name = None
        self.addr = None

    def type(self):
        return self.message['type']

    # dump is used to create a message that can be send via BrokerPeer
    # need to be overwritten if needed
    def dump(self):
        vec = pybroker.vector_of_data(1, pybroker.data("dbroctld"))
        vec.append(pybroker.data(str((json.dumps(self.name)))))
        vec.append(pybroker.data(str((json.dumps(self.addr)))))
        vec.append(pybroker.data(str(json.dumps(self.message))))
        return vec

    # to output the message for debugging purposes
    def str(self):
        return str(self.message)

    def json(self):
        return self.message


class BCmdMsg(BBaseMsg):
    def __init__(self, name, addr, payload):
        super(BCmdMsg, self).__init__("command")
        self.message['payload'] = payload
        self.name = name
        self.addr = addr


class BResMsg(BBaseMsg):
    def __init__(self, name, addr, cmd, payload):
        super(BResMsg, self).__init__(mtype="result")
        self.name = name
        self.addr = addr
        self.message['for'] = cmd
        self.message['payload'] = payload


class BroMsg(BBaseMsg):
    def __init__(self, event, args):
        super(BroMsg, self).__init__(event)
        self.message['args'] = args

    def dump(self):
        vec = pybroker.vector_of_data(1, pybroker.data(self.message['type']))
        if self.message['args']:
            for a in self.message['args']:
                vec.append(pybroker.data(str(a)))
        return vec
