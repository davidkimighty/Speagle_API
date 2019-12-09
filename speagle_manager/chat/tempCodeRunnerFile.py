import os
from binascii import hexlify
for x in range(2, 6):
    print(hexlify(os.urandom(16)))