from datetime import datetime, timedelta

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.x509.oid import NameOID


def gencert(domain, days=10, key_size=2048):
    key = rsa.generate_private_key(public_exponent=65537, key_size=key_size, backend=default_backend())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, domain)])
    now = datetime.utcnow()

    certificate = x509.CertificateBuilder() \
        .subject_name(name) \
        .issuer_name(name) \
        .public_key(key.public_key()) \
        .serial_number(x509.random_serial_number()) \
        .not_valid_before(now) \
        .not_valid_after(now + timedelta(days=days)) \
        .sign(key, SHA256(), default_backend())

    return key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()), certificate.public_bytes(Encoding.PEM)


if __name__ == '__main__':
    sk, pk = gencert('necauqua.dev')
    print(sk.decode('utf-8'))
    print(pk.decode('utf-8'))
