from base64 import b64encode, urlsafe_b64encode, b64decode, urlsafe_b64decode
import sys


def tobytes(x, raw=False):
    if isinstance(x, str):
        if not raw:
            if x == '-':
                return sys.stdin.buffer.read()
            if x.startswith('@'):
                filename = x[1:]
                if filename == '-':
                    return sys.stdin.buffer.read()
                with open(filename, 'rb') as f:
                    return f.read()
        x = x.encode('utf8')
    return x

def tofile(bytes, file):
    if file is None:
        return False
    if isinstance(file, str):
        if file == '-':
            sys.stdout.buffer.write(bytes)
        with open(file, 'wb') as f:
            f.write(bytes)
    else:
        file.write(bytes)
    return True

def b64enc(x, urlsafe=True):
    return (urlsafe_b64encode if urlsafe else b64encode)(x)

def b64dec(x, urlsafe=True):
    return (urlsafe_b64decode if urlsafe else b64decode)(x)
