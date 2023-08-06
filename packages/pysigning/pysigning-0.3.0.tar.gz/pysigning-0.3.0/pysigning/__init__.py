from .crypto import RSA, SHA256, PKCS1_v1_5
from .util import tobytes, b64enc, b64dec
import argh
import sys

class SignatureFailedToVerifyError(ValueError):
    pass

def sign(message, key="sign.key", passphrase=None, no_urlsafe=False, raw=False):
    with open(key, 'rb') as f:
        private_key = RSA.importKey(f.read(), passphrase=passphrase)
    message = tobytes(message, raw)
    signer = PKCS1_v1_5.new(private_key)
    digest = SHA256.new()
    digest.update(message)
    signature = signer.sign(digest)
    sig64 = b64enc(signature, urlsafe=not no_urlsafe).decode('utf8')
    return sig64

def verify(message, signature, *, key="sign.crt", passphrase=None, no_urlsafe=False, raw=False):
    with open(key, 'rb') as f:
        public_key = RSA.importKey(f.read(), passphrase=passphrase)
    message = tobytes(message, raw)
    signature = tobytes(signature)
    verifier = PKCS1_v1_5.new(public_key)
    digest = SHA256.new()
    digest.update(message)
    sig64 = b64dec(signature, urlsafe=not no_urlsafe)
    ok = verifier.verify(digest, sig64)
    return ok

def token(message, key="sign.key", passphrase=None, raw=False, header='{"alg":"RS256"}'):
    encoded_header = b64enc(tobytes(header), urlsafe=True)
    encoded_body = b64enc(tobytes(message, raw), urlsafe=True)
    signature = sign(encoded_header+b'.'+encoded_body, key=key, passphrase=passphrase).encode('utf8')
    jws = encoded_header + b'.' + encoded_body + b'.' + signature
    return jws.decode('utf8')
