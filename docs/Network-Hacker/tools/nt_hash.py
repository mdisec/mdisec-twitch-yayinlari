import hashlib, binascii

hash = hashlib.new('md4', ''.encode('utf-16le')).digest()
print(binascii.hexlify(hash))