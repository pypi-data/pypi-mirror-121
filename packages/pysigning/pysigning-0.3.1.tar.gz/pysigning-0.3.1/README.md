# pysigning

> Python library and CLI scripts for signing and verifying data


## Install

```
pip3 install -U pysigning
```

## Usage

### Generate a random signing key for testing

```
# generate private key as "sign.key"
openssl genrsa -out sign.key 2048

# get private key's public key as "sign.crt"
openssl rsa -in sign.key -pubout -out sign.crt
```

### CLI

Generate a signature for the file `LICENSE` using the private key `sign.key`
```
$ pysigning sign @LICENSE --key sign.key
gdFNOO9cwpYXWv9TfulFauNQ5S1WXXIQAuXC4qQB9vyOMhZW0hOl0fvyyHC1pNzZAOrpUNEoQuvvs6w2r0TdzcMsA_finu5RVVzzko4kQuOWM6Tw3CX6ln82h8z2gWyKRhIC71pScpy7MJO8IEFBBPqQbR5NDFvGVh9F69S3pVZzf4xqrkcBBWoJr2DjD-VFQ6S5hFA0PQ685cDY26hB07MWoLVHFz5jyqDfDmGqNRb5bY7fUzmJCdY5wdLExrrJQJaZhU9Ak_HAA3zsmvy0OSRTNJY7BIwVdopQ_dN-CdTLQgsoEfqpvLVp6HLRuZWhftnMlkmq0vTypgh24kYyCg==
```

Verify the signature of the file `LICENSE` using the public key `sign.crt`
```
$ pysigning sign @LICENSE --key sign.key | pysigning verify @LICENSE - --key sign.crt
True
```

### Library

```py
import pysigning

# Generate a signature for the file `LICENSE` using the private key `sign.key`
sig = pysigning.sign('@LICENSE', key="sign.key")
print(sig)

# Verify the signature of the file `LICENSE` using the public key `sign.crt`
assert pysigning.verify('@LICENSE', sig, key="sign.crt")
```

## License

MIT

## Contact

A library by [Shawn Presser](https://www.shawwn.com). If you found it useful, please consider [joining my patreon](https://www.patreon.com/shawwn)!

My Twitter DMs are always open; you should [send me one](https://twitter.com/theshawwn)! It's the best way to reach me, and I'm always happy to hear from you.

- Twitter: [@theshawwn](https://twitter.com/theshawwn)
- Patreon: [https://www.patreon.com/shawwn](https://www.patreon.com/shawwn)
- HN: [sillysaurusx](https://news.ycombinator.com/threads?id=sillysaurusx)
- Website: [shawwn.com](https://www.shawwn.com)

