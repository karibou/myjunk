#!/usr/bin/python

import sys, os, time, socket
from M2Crypto import SSL, Err, httpslib

srv_host = 'localhost'
srv_port = 64000
srv_addr = (srv_host, srv_port)
srv_url = 'https://%s:%s/' % (srv_host, srv_port)
args = ['s_server', '-quiet', '-www',
        # '-cert', 'server.pem', Implicitly using this
        '-accept', str(srv_port)]
sleepTime = float(0.5)


def create_cert():
    with open("server.pem", "w") as cert:
        cert.write('''Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 1 (0x1)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=US, O=M2Crypto ca, CN=localhost
        Validity
            Not Before: Apr 29 06:58:18 2013 GMT
            Not After : Apr 27 06:58:18 2023 GMT
        Subject: C=US, O=M2Crypto server, CN=localhost
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
            RSA Public Key: (2048 bit)
                Modulus (2048 bit):
                    00:e3:f0:b7:01:45:6f:ba:6e:f1:15:64:e5:7f:84:
                    09:0f:82:f8:df:90:e1:2b:25:56:7c:65:c3:a3:eb:
                    83:d9:dd:b7:b9:1d:03:8f:1e:19:a2:f5:54:80:02:
                    7a:e1:56:a7:ab:87:c3:d9:93:b1:a1:6c:df:66:18:
                    2a:41:62:18:f0:0f:89:b7:2f:b0:7c:12:b3:a8:d0:
                    62:6b:e8:07:68:f4:5a:b7:69:8f:74:2e:d5:b3:83:
                    d2:0b:44:0d:78:b6:95:e8:2b:6f:a9:d4:1f:4f:a0:
                    9c:e3:13:b4:05:38:0d:a5:cc:a7:a5:26:ba:e5:8f:
                    73:c8:7a:5d:e7:d1:6b:98:8e:10:f5:8b:2f:00:05:
                    fd:1c:1b:b1:e6:3a:45:a1:25:c5:10:8f:12:b4:98:
                    c3:25:4c:15:8d:a6:4d:22:d4:11:de:5c:99:6d:31:
                    e9:88:86:14:a6:43:87:28:1c:9d:59:aa:6e:28:d6:
                    f9:db:92:4b:71:9b:54:3d:01:ab:74:cf:a3:01:f9:
                    59:64:a1:20:3a:fd:57:54:83:3b:d2:42:b5:c4:58:
                    80:7b:23:89:16:f5:9c:0d:bd:f9:63:d0:5c:bf:9a:
                    17:02:35:ee:54:92:e0:99:37:44:2e:aa:69:c0:c0:
                    2e:7e:f9:3c:a3:e8:e0:42:14:21:96:e0:31:04:05:
                    8c:15
                Exponent: 65537 (0x10001)
    Signature Algorithm: sha256WithRSAEncryption
        32:94:0b:18:c8:28:d5:87:f8:3c:81:70:a5:33:71:a7:b9:0c:
        2f:e1:10:fa:8f:af:d8:1e:1f:94:00:33:e7:ff:17:ba:8a:f1:
        d7:c0:61:22:cc:51:0e:ed:14:5d:b3:76:f1:df:74:29:b2:92:
        3f:1a:63:e9:a1:0c:ef:c1:78:fe:16:a7:56:9b:f3:13:5f:d3:
        b7:a9:0d:4c:3e:0f:1c:cc:bb:78:f4:2b:ec:0e:df:3b:30:b1:
        5e:be:c3:79:ab:bb:33:6c:c8:e7:aa:24:69:c1:24:f7:fc:99:
        92:8b:1c:37:6d:c7:80:04:95:df:45:16:33:0c:2a:4e:98:97:
        ae:d9:7d:a7:98:f4:91:31:0d:57:0b:78:24:3c:99:0a:19:c1:
        1c:93:5b:f5:97:46:4e:d8:15:74:1a:bf:25:3b:28:cf:3c:3f:
        93:47:48:95:14:8b:32:b5:fd:ec:66:bb:e0:09:3e:db:d2:eb:
        35:a6:76:3d:e5:8d:b4:d1:a3:44:78:b6:59:80:f9:55:4f:f5:
        c2:f4:8b:ab:f1:c2:7f:96:87:3c:92:d9:fd:5f:e7:f9:07:5a:
        9a:4c:b9:ae:94:aa:1f:a7:d8:5c:bd:87:07:49:f1:2f:0a:1f:
        08:3b:89:46:9f:6a:2b:5d:b7:81:90:44:13:16:66:69:cc:48:
        33:82:4a:a0
-----BEGIN CERTIFICATE-----
MIIC6zCCAdOgAwIBAgIBATANBgkqhkiG9w0BAQsFADA3MQswCQYDVQQGEwJVUzEU
MBIGA1UEChMLTTJDcnlwdG8gY2ExEjAQBgNVBAMTCWxvY2FsaG9zdDAeFw0xMzA0
MjkwNjU4MThaFw0yMzA0MjcwNjU4MThaMDsxCzAJBgNVBAYTAlVTMRgwFgYDVQQK
Ew9NMkNyeXB0byBzZXJ2ZXIxEjAQBgNVBAMTCWxvY2FsaG9zdDCCASIwDQYJKoZI
hvcNAQEBBQADggEPADCCAQoCggEBAOPwtwFFb7pu8RVk5X+ECQ+C+N+Q4SslVnxl
w6Prg9ndt7kdA48eGaL1VIACeuFWp6uHw9mTsaFs32YYKkFiGPAPibcvsHwSs6jQ
YmvoB2j0Wrdpj3Qu1bOD0gtEDXi2legrb6nUH0+gnOMTtAU4DaXMp6UmuuWPc8h6
XefRa5iOEPWLLwAF/RwbseY6RaElxRCPErSYwyVMFY2mTSLUEd5cmW0x6YiGFKZD
hygcnVmqbijW+duSS3GbVD0Bq3TPowH5WWShIDr9V1SDO9JCtcRYgHsjiRb1nA29
+WPQXL+aFwI17lSS4Jk3RC6qacDALn75PKPo4EIUIZbgMQQFjBUCAwEAATANBgkq
hkiG9w0BAQsFAAOCAQEAMpQLGMgo1Yf4PIFwpTNxp7kML+EQ+o+v2B4flAAz5/8X
uorx18BhIsxRDu0UXbN28d90KbKSPxpj6aEM78F4/hanVpvzE1/Tt6kNTD4PHMy7
ePQr7A7fOzCxXr7Deau7M2zI56okacEk9/yZkoscN23HgASV30UWMwwqTpiXrtl9
p5j0kTENVwt4JDyZChnBHJNb9ZdGTtgVdBq/JTsozzw/k0dIlRSLMrX97Ga74Ak+
29LrNaZ2PeWNtNGjRHi2WYD5VU/1wvSLq/HCf5aHPJLZ/V/n+Qdamky5rpSqH6fY
XL2HB0nxLwofCDuJRp9qK123gZBEExZmacxIM4JKoA==
-----END CERTIFICATE-----
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA4/C3AUVvum7xFWTlf4QJD4L435DhKyVWfGXDo+uD2d23uR0D
jx4ZovVUgAJ64Vanq4fD2ZOxoWzfZhgqQWIY8A+Jty+wfBKzqNBia+gHaPRat2mP
dC7Vs4PSC0QNeLaV6CtvqdQfT6Cc4xO0BTgNpcynpSa65Y9zyHpd59FrmI4Q9Ysv
AAX9HBux5jpFoSXFEI8StJjDJUwVjaZNItQR3lyZbTHpiIYUpkOHKBydWapuKNb5
25JLcZtUPQGrdM+jAflZZKEgOv1XVIM70kK1xFiAeyOJFvWcDb35Y9Bcv5oXAjXu
VJLgmTdELqppwMAufvk8o+jgQhQhluAxBAWMFQIDAQABAoIBAHaFatL5ZPAe0bKb
JQ4Z/JAZPQkaj0pc/sxuKb0pMATv2aEiagBX2WK3h/mL0JMs+MAjNv4CYwGZ18uB
Uy9uL6NboPMkk/Lf0pU7zYFoQ7oaHLVz6QizdaEDMQt0lkCnR+lR9Jzs1F8WF52n
WBrCm64TbTRdoB7PaZfbsMpiRT0r3nqcIOdha20Jus985Gez1BFNwTeCut+oljwA
Ko5wGaFNbUwFdzdnGF/Djq0lKIJ/DsRlIxhovCu3OnwtTkxt1t1ifBuJeoBJOee0
qMMgs7iW5R8qXmjJLLltLHFmvAGnt5t/UIQPYu7YCEdMa6EAszlIUwT0a5v11TZ2
e2C5rEECgYEA9fgLXf3vNRnibvAmC3lMlnE+9BEoml9O26tl9rwIWjBLEIlUJJIk
X/WOBfgx20oPt+vBG9C/Iam0vUz2xDZauNhqjPz9tZFznPpTZYqwS49xV6qpu7uT
Ah63ON5gX9AZoe+kvcljVihncbgEWbhNHgDhE+9Yj1HpJlv+ywpeeoUCgYEA7Txy
2J81V9pHcjSAc5sjry5V2QTf1AP+N/LdoL9JccoBtYhtWiEtbcByr6GNAYNlbKim
DoArd5Nsc5a6sJnMhab7cGZ8CzvpX9X+lQ0P189zbt/hSeV3VtYA2xSszir+moFU
nfdq5XOfJ+gxfkgjGcsEaBmxPSAGrDKFfivMKFECgYEA1xWb+wj+j9SeqJve6NGd
I0DL5+jJNJR7BKQQeX1bYGIygbdUmNYicLbtBlNOZY+RxyakqooTWIBpx87xSgqt
sk2sfrULtiYGjxJmsrhgCPLaDerymXMgzg3F8jii1aXHhE9mI39jGggizNI5G6uJ
496o8yGss0bRNfXkC/B5RXECgYA1NHtlTb9+5ntjh5bPVpnYLgIe29L/D64yCgve
g0gLdwyPE/vCXPJ9TM3rycV/82IJzoD/e4tEFBIckk9oT/Xoe5ykhreHJXafgbTI
5NcKxYHT+e3izs3G8dPbTnW6/zV+nUbG7rhQoW+uWYrQEYmdvURNvIVdehNFB0ed
FmGBIQKBgG5V1n/lhVJmaFvisaEZGUML18CngrdO9tdXhGQ1JxTtDnLrfUPdgKRQ
checcxJAYGul2ZdcWtC9BkMF+pMiSHBrR8cSgrXpPQgIszp/NL4dQXLJYP0LSXI9
BuE13LjbCQcCNsh451MauZV3tmk5/L58dhEp/SULOsjCejZAMc4O
-----END RSA PRIVATE KEY-----
''')


def start_server(args):
    pid = os.fork()
    if pid == 0:
        os.execvp('openssl', args)
    else:
        time.sleep(sleepTime)
        return pid


def stop_server(pid):
    os.kill(pid, 1)
    os.waitpid(pid, 0)


def test_HTTPSConnection():
    try:
        c = httpslib.HTTPSConnection(srv_host, srv_port)
        c.request('GET', '/')
        data = c.getresponse().read()
        c.close()
        return data
    except socket.error, arg:
        print "Error : {}".format(arg)
        return('')


def main():
    try:
        print "Creating server cert file"
        create_cert()
        print "Starting HTTPS server...",
        pid = start_server(args)
        print("PID is {}".format(pid))
        text = test_HTTPSConnection()
        if text.startswith("<HTML>"):
            print("Connection OK")
    except BaseException, arg:
        print "Error {}".format(arg)
    finally:
        os.remove("server.pem")
        stop_server(pid)


if __name__ == '__main__':
    main()
