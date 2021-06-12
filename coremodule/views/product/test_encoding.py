# from hashlib import sha256
# import base64
# from Crypto import Random
# from Crypto.Cipher import AES


class GroceryEncryption(object):

    def __init__(self, key): 
        self.bs = 32
        self.key = hashlib.sha256(key.encode()).digest()

    def encryption(self, raw, iv):
        raw = raw.encode('utf8')
        raw = str(raw)
        raw = raw[2:-1]
        pad_encoder = PKCS7Encoder()
        raw = pad_encoder.encode(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        cipheredText = cipher.encrypt(raw)
        base64encData = base64.b64encode(cipheredText)
        encryptedData = str(base64encData)
        return encryptedData

    def decryption(self, encryptedData, iv):
        #encryptedData = encryptedData.replace("-sl-", "/").replace("b'","")[:-1]
        encryptedData = encryptedData.replace("-sl-", "/")
        pad_decoder = PKCS7Encoder()
        dec = base64.b64decode(encryptedData)
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return pad_decoder.decode(cipher.decrypt(dec).decode("utf-8"))

    def iv_on_decryption(self, encryptedData):
        enc = base64.b64decode(encryptedData)
        #print("======="+str(enc))
        #enc = encryptedData
        iv = enc[:AES.block_size]
        return iv

    def _padding(self, text):

        text_length = len(text)
        amount_to_pad = self.bs - (text_length % self.bs)
        if amount_to_pad == 0:
            amount_to_pad = self.bs
        pad = unhexlify('%02x' % amount_to_pad)
        return text + pad * amount_to_pad

    @staticmethod
    def _unpadding(argString):        
        return argString[:-ord(argString[len(argString)-1:])]

    def general_iv(self):
        return Random.new().read(AES.block_size)

def encrypt(raw):
        key = "secretkeyformmat"
        # bs = AES.block_size
        # iv = Random.new().read(bs)
        # iv = "1234567890123456"
        # print("kkl")
        # print(iv)
        # cipher = AES.new(AES_SECRET, AES.MODE_CBC, iv)
        # encrypted = cipher.encrypt(text.encode('ascii', 'ignore'))
        # print("kk")
        # print(encrypted)

        key = hashlib.sha256(key.encode()).digest()

        
        iv = Random.new().read(AES.block_size)


        raw = raw.encode('utf8')
        raw = str(raw)
        raw = raw[2:-1]
        pad_encoder = PKCS7Encoder()
        raw = pad_encoder.encode(raw)
        # print(key)
        # print(iv)
        # print("===="+str(raw))
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # print(cipher)


        cipheredText = cipher.encrypt(str.encode(raw))
        print(cipheredText)


def decryptttt(raw):
        key = "secretkeyformmat"

        key = hashlib.sha256(key.encode()).digest()

        
        iv = Random.new().read(AES.block_size)


        # raw = raw.encode('utf8')
        # raw = str(raw)
        # raw = raw[2:-1]
        # pad_encoder = PKCS7Encoder()
        # raw = pad_encoder.encode(raw)
        # print(key)
        # print(iv)
        # print("===="+str(raw))
        cipher = AES.new(key, AES.MODE_CBC, iv)
        print("k1")
        print(cipher)


        # cipheredText = cipher.encrypt(str.encode(raw))
        # print(cipheredText)
        print("k2")
        print(raw)
        decr_text = cipher.decrypt(raw)
        decr_text = decr_text.decode('utf8')

        print("k3")
        print(decr_text)


def get_encryption():
    try:
        strmsg = "This is input string"

        key = 'abcdefghijklmnop'  
        key1 = str.encode(key)

        iv = Random.new().read(AES.block_size)

        obj = AES.new(key1, AES.MODE_CBC, iv)
        encrypted = obj.encrypt(str.encode(strmsg))
        print(encrypted)
    except Exception as e:
        print(e)

