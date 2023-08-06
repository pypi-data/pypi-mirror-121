from typing import List
from binascii import hexlify, unhexlify

import time

class ApduRequest:
    def __init__(self, class_, instruction, p1, p2, data=None):
        self.class_ = class_
        self.instruction = instruction
        self.p1 = p1
        self.p2 = p2
        if data is None:
            data = []
        if isinstance(data, bytes):
            data = list(data)
        self.data = data

    def __repr__(self):
        return f"cla={self.class_:02x}, ins={self.instruction:02x}, p1={self.p1:02x}, p1={self.p2:02x}, cd[{len(self.data):02x}]={hexlify(bytes(self.data)).decode()}"

    def to_sequence(self):
        return [
            self.class_,
            self.instruction,
            self.p1,
            self.p2,
            len(self.data),
            *self.data
        ]

    def to_bytes(self):
        return bytes(self.to_sequence())

class ApduResponse:
    def __init__(self, data: List[int], sw1: int, sw2: int):
        self.data = data
        self.sw1 = sw1
        self.sw2 = sw2

    def __str__(self):
        return hexlify(bytes(self.body) + bytes([self.sw1, self.sw2])).decode('utf8')

    def __repr__(self):
        return (
            (f"[{len(self.body)}]".encode() if self.body else b"") 
            + (hexlify(bytes(self.body)) + (b" " if self.data else b"") 
            + hexlify(bytes([self.sw1, self.sw2])))
        ).decode('utf8')

    def __len__(self):
        return len(self.data)

    @property
    def body(self):
        return bytes(self.data)

    @property
    def sw(self):
        return self.sw1*0x100 + self.sw2

class Applet:
    def __init__(self, connection, debug=False):
        self.debug = debug
        self.connection = connection

    def transmit(self, apduRequest, handleRequestChaining=True, handleResponseChaining=True):
        if self.debug:
            start = time.time()
        if handleRequestChaining and len(apduRequest.data) > 0xFF:
            for i in range(0, len(apduRequest.data), 0xFF):
                chunk = apduRequest.data[i:i + 0xFF]
                is_last_chunk = i + 0xFF >= len(apduRequest.data)
                chunkRequest = ApduRequest(
                    # apduRequest.class_ & (0x00 if is_last_chunk else 0x10),
                    apduRequest.class_ | (0x00 if is_last_chunk else 0x10),
                    apduRequest.instruction,
                    apduRequest.p1,
                    apduRequest.p2,
                    chunk
                )
                if self.debug:
                    print(">>-", repr(chunkRequest))
                apduResponse = ApduResponse(*self.connection.transmit(chunkRequest.to_sequence()))
                if self.debug:
                    print("<<-", repr(apduResponse))
        else:    
            if self.debug:
                print(">>>", repr(apduRequest))
            apduResponse = ApduResponse(*self.connection.transmit(apduRequest.to_sequence()))
        if handleResponseChaining:
            response_chain = []
            response_chain.extend(apduResponse.body)
            if self.debug:
                print("<<-", repr(apduResponse))
            while apduResponse.sw1 == 0x61:
                apduResponse = ApduResponse(*self.connection.transmit(ApduRequest(0x00, 0xc0, 0x00, 0x00).to_sequence()))
                if self.debug:
                    print("<<-", repr(apduResponse))
                response_chain.extend(apduResponse.body)
            apduResponse = ApduResponse(response_chain, apduResponse.sw1, apduResponse.sw2)
        if self.debug:
            print("<<<", repr(apduResponse), f"({(time.time()-start)*1000:0.0f} ms)")
        return apduResponse

class PivApplet(Applet):

    INS_VERIFY = 0x20
    INS_CHANGE_PIN = 0x24
    INS_RESET_PIN = 0x2C
    INS_GEN_AUTH = 0x87
    INS_GET_DATA = 0xCB
    INS_PUT_DATA = 0xDB
    INS_GEN_ASYM = 0x47
    INS_GET_RESPONSE = 0xC0

    TAG_CERT_9E = 0x01
    TAG_CHUID = 0x02
    TAG_FINGERPRINTS = 0x03
    TAG_CERT_9A = 0x05
    TAG_SECOBJ = 0x06
    TAG_CARDCAP = 0x07
    TAG_FACE = 0x08
    TAG_PRINTED_INFO = 0x09
    TAG_CERT_9C = 0x0A
    TAG_CERT_9D = 0x0B
    TAG_KEYHIST = 0x0C
    TAG_CERT_82 = 0x0D
    TAG_CERT_8C = 0x17

    PIV_ALG_DEFAULT = 0x00
    PIV_ALG_3DES = 0x03
    PIV_ALG_RSA1024 = 0x06
    PIV_ALG_RSA2048 = 0x07
    PIV_ALG_AES128 = 0x08
    PIV_ALG_AES192 = 0x0A
    PIV_ALG_AES256 = 0x0C
    PIV_ALG_ECCP256 = 0x11
    PIV_ALG_ECCP384 = 0x14

    PIV_ALG_ECCP256_SHA1 = 0xf0
    PIV_ALG_ECCP256_SHA256 = 0xf1
    PIV_ALG_ECCP384_SHA1 = 0xf2
    PIV_ALG_ECCP384_SHA256 = 0xf3
    PIV_ALG_ECCP384_SHA384 = 0xf4


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def authPin(self, pin: str):
        PIN_MAX_LENGTH = 8
        return self.transmit(ApduRequest(
            0x00, self.INS_VERIFY,
            0x00,
            0x80,
            (pin.encode() + b'\xFF'*PIN_MAX_LENGTH)[:PIN_MAX_LENGTH]
        ))

    def getData(self, tag_id):
        return self.transmit(ApduRequest(
            0x00, self.INS_GET_DATA,
            0x3F, # magic constant
            0xFF, # magic constant
            [0x5C, 0x03, 0x5F, 0xC1, tag_id]
        ))

    def genAuth(self, algorithm, slot, data):
        return self.transmit(ApduRequest(
            0x00, self.INS_GEN_AUTH,
            algorithm,
            slot,
            data
        ))

