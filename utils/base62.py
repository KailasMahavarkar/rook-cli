import binascii

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode_base62(num):
    s = ""
    while num > 0:
        num, r = divmod(num, 62)
        s = BASE62[r]+s
    return s


def decode_base62(num):
    x, s = 1, 0
    for i in range(len(num)-1, -1, -1):
        s = int(BASE62.index(num[i])) * x + s
        x *= 62
    return s



def numfy(s, max_code=0x110000):
    # 0x110000 is max value of unicode character
    number = 0
    for e in [ord(c) for c in s]:
        number = (number * max_code) + e
    return number


def denumfy(number, max_code=0x110000):
    l = []
    while number != 0:
        l.append(chr(number % max_code))
        number = number // max_code
    return ''.join(reversed(l))



def str2num(string):
   return int(binascii.hexlify(string.encode("utf-8")), 16)


def num2str(number):
    return binascii.unhexlify(format(number, "x").encode("utf-8")).decode("utf-8")


def encode62(text: str):
    return encode_base62(str2num(text))

def decode62(text: str):
    return num2str(decode_base62(text))

