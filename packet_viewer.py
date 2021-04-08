# TO BE USED WITH https://github.com/Tocutoeltuco/tfmplugins
# Credits to @Athesdrake for Xor decryption
# I recommend using this script with Windows Terminal, it looks really nice :]

import datetime
import zlib
from tfmplugins.tfm.packet import Packet
import colored
from colored import stylize
import os
import struct


class Plugin:
    def __init__(self):
        self.xor_key = None
        self.current_XML = None
        self.show_sent_packets = 0
        self.show_received_packets = 0
        self.show_channel_chat = 1
        self.commands = ['printxml', 'channelchat', 'sentpackets', 'receivedpackets']
        self.name = os.path.basename(__file__)
        self.load()

    def save(self):
        if self.xor_key is not None:
            with open('xor_key.bin', 'wb') as f:
                f.write(self.xor_key)

    def load(self):
        if os.path.exists('xor_key.bin'):
            with open('xor_key.bin', 'rb') as f:
                data = f.read()
                if len(data) == 20:
                    self.xor_key = data

    async def tear_down(self):
        self.save()

    async def packet_sent(self, client, conn, fingerprint, packet):
        # This method will be executed when the script detects an outbound
        # packet (that is sent to the server).
        # client is an instance of TFMClient
        # conn is an instance of TFMConnection
        # fingerprint is an int, the fingerprint of the packet
        # packet is an instance of Packet
        CCC = packet.readCode()
        if self.show_sent_packets == 1:
            print(stylize("Sent, CCC = {}, buffer = {}".format(CCC, packet.buffer[3:]), colored.fg(46)))

        if CCC == (6, 26):
            if self.xor_key is not None:
                # if we have the XOR key, decrypt the packet
                packet.xor_cipher(self.xor_key, fingerprint, 3)
                # extract the string's length
                length = packet.read16()

                # check if the length is correct
                if length + packet.pos == len(packet.buffer):
                    # if it is, then the XOR key is correct
                    # and we can extract the command
                    command = packet.readBytes(length).decode().lower()
                    print(stylize(f'Command sent: {command}', colored.fg(226)))
                    if command == 'printxml':
                        print(stylize("XML = {}".format(self.current_XML), colored.fg(53)))
                    elif command == 'sentpackets':
                        self.show_sent_packets = 1 - self.show_sent_packets
                    elif command == 'receivedpackets':
                        self.show_received_packets = 1 - self.show_received_packets
                    elif command == 'channelchat':
                        self.show_channel_chat = 1 - self.show_channel_chat
                    elif command == 'help':
                        msg = '[~] Available commands: '
                        for i in self.commands:
                            msg = msg + '\n - ' + i
                        print(stylize(msg, colored.fg(182)))
                else:
                    # otherwise, the XOR key is not correct
                    # so we reset it
                    self.xor_key = None
                    print(stylize('The XOR key was wrong :c', colored.fg(1)))

            if self.xor_key is None:
                # if we don't have the XOR key or it has been reseted
                # then read the whole packet
                encrypted = packet.readBytes(len(packet.buffer) - packet.pos)

                if len(encrypted) == 20:
                    # if the packet is 20 long (/AAAAAAAAAAAAAAAAAA)
                    # then create the expected data
                    data = struct.pack('>H', 18) + b'A' * 18
                    # decrypt it
                    cycled = bytes(a ^ b for a, b in zip(encrypted, data))
                    # compute the offset
                    offset = 19 - (fingerprint % 20)
                    # rearrange the key
                    self.xor_key = cycled[offset:] + cycled[:offset]
                    # and boom black magic it works!
                    print(stylize(f'OwO I got the XOR key: {self.xor_key.hex(" ")}', colored.fg(2)))

    async def packet_received(self, client, conn, packet):
        # This method will be executed when the script detects an inbound
        # packet (that is sent to the client).
        # client is an instance of TFMClient
        # conn is an instance of TFMConnection
        # packet is an instance of Packet
        if len(packet.buffer) < 2:
            pass

        CCC = packet.readCode()

        if self.show_received_packets == 1:
            print(stylize("Received, CCC = {}, buffer = {}".format(CCC, packet.buffer[2:]), colored.fg(46)))

        if CCC == (6, 6):  # room message
            author = packet.readUTF()
            message = packet.readUTF()
            current_time = datetime.datetime.now()
            print(stylize("[{}] [{}]".format(current_time.strftime("%H:%M"), author), colored.fg(23)) + stylize(
                " {}".format(message), colored.fg(7)))
        elif CCC == (60, 3):  # tribulle message
            source = packet.read16()  # protocol, describes contents of the packet

            if source == 0x41:  # tribe message
                author = packet.readUTF()
                message = packet.readUTF()
                current_time = datetime.datetime.now()
                print(stylize("• [{}] [{}] {}".format(current_time.strftime("%H:%M"), author, message), colored.fg(35)))
            elif source == 0x21:  # friend disconnected
                name = packet.readUTF()
                print(stylize("{} has disconnected. :(".format(name), colored.fg(234)))
            elif source == 0x20:  # friend connected
                name = packet.readUTF()
                print(stylize("{} just connected!".format(name), colored.fg(234)))
            elif source == 0x5a:  # tribemember disconnected
                name = packet.readUTF()
                current_time = datetime.datetime.now()
                print(
                    stylize("• [{}] {} has disconnected.".format(current_time.strftime("%H:%M"), name), colored.fg(42)))
            elif source == 0x58:  # tribemember connected
                name = packet.readUTF()
                current_time = datetime.datetime.now()
                print(stylize("• [{}] {} just disconnected!".format(current_time.strftime("%H:%M"), name),
                              colored.fg(42)))
            elif source == 0x42:  # whisper sent
                sender = packet.readUTF()
                packet.read16()  # idk
                communityid = packet.read16()
                receiver = packet.readUTF()
                message = packet.readUTF()
                print(stylize("from [{}] to [{}] {}".format(sender, receiver, message), colored.fg(166)))
            elif source == 0x40 and self.show_channel_chat == 1:  # global chat message
                sender = packet.readUTF()
                packet.read32()  # what the fuck?
                chatname = packet.readUTF()
                message = packet.readUTF()
                print(stylize(">#{} [{}] {}".format(chatname, sender, message), colored.fg(167)))
        elif CCC == (5, 2):  # map received
            mapcode = packet.read32()
            playercount = packet.read16()  # players in the room
            roundcode = packet.read8()  # the round of this room
            packet.read16()  # idk
            compressedXML = packet.readString()
            author = packet.readString()
            if compressedXML:
                xml = zlib.decompress(compressedXML).decode()  # decompressed XML
                print(stylize(
                    "[~] {} loaded made by {}. {} players in the room. Round {}.".format(mapcode, author.decode(),
                                                                                         playercount, roundcode),
                    colored.bg(53)))
                self.current_XML = xml  # we store the xml to print it later
        elif CCC == (5, 21):  # joined room
            official = packet.read8()  # is room oficial?
            roomname = packet.readUTF()  # the target name
            community = packet.readUTF()  # commu name
            print(stylize("[~] Joined room {}.".format(roomname), colored.bg(23)))
            print(stylize("commu = {}, official = {}".format(community, official), colored.fg(23)))


plugin = Plugin()
