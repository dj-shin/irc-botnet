import re


class IRCMessageParser:
    def __init__(self, context=b''):
        self.context = context

    def parse(self):
        message = IRCMessage(self.context)
        self.context = IRCMessage.prog.sub(b'', self.context, 1)
        return message

    def parsable(self):
        return IRCMessage.valid(self.context)

    def append(self, data):
        self.context += data


class IRCMessage:
    prog = re.compile(b'^(?::(([^@!\ ]*)(?:(?:!([^@]*))?@([^\ ]*))?)\ )?([^\ ]+)((?:\ [^:\ ][^\ ]*){0,14})(?:\ :?(.*))?\r\n')

    @classmethod
    def valid(cls, data):
        return cls.prog.match(data) is not None

    def __init__(self, data):
        parse = self.prog.match(data)
        if parse:
            self.prefix = parse.group(1).decode('utf-8', 'ignore') if parse.group(1) else None
            self.nick = parse.group(2).decode('utf-8', 'ignore') if parse.group(2) else None
            self.username = parse.group(3).decode('utf-8', 'ignore') if parse.group(3) else None
            self.hostname = parse.group(4).decode('utf-8', 'ignore') if parse.group(4) else None
            self.command = parse.group(5).decode('utf-8', 'ignore') if parse.group(5) else None
            self.params = parse.group(6).split(b' ')[1:]
            if parse.group(7):
                self.params.append(parse.group(7))
            for i in range(len(self.params)):
                self.params[i] = self.params[i].decode('utf-8', 'ignore')

    @property
    def channel(self):
        if self.command in ['JOIN', 'MODE', 'PRIVMSG', 'KICK']:
            return self.params[0]
        elif self.command in ['INVITE']:
            return self.params[1]
        else:
            return None

    @property
    def text(self):
        if self.command in ['PRIVMSG']:
            return self.params[1]
        elif self.command in ['KICK']:
            return self.params[2]
        else:
            return None

    def __repr__(self):
        return '<IRCMessage : {} {!r} {!r} {!r} {!r} {}>'.format(
                self.command, self.prefix, self.nick, self.username, self.hostname, self.params)
