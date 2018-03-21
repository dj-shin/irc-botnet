class BaseMessageHandler:
    def __init__(self, transport, loop, settings=None):
        self.transport = transport
        self.loop = loop
        self.settings = settings

    def handle(self, message):
        if message.command == 'PING':
            self.transport.write('PONG :pingis\n'.encode())

    def send_message(self, channel, message):
        self.transport.write('PRIVMSG {channel} :{message}\n'.format(
            channel=channel,
            message=message
        ).encode())

    def join_channel(self, channel, password=None):
        self.transport.write('JOIN {channel}{password}\n'.format(
            channel=channel,
            password=' ' + password if password is not None else ''
        ).encode())

    def part_channel(self, channel):
        self.transport.write('PART {channel}\n'.format(
            channel=channel
        ).encode())
