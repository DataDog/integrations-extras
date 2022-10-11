# TLS for tests

## Prerequisite

- https://github.com/cloudflare/cfssl

## Generate Certificate Authority

This command generates `ca.pem` and `ca-key.pem` that are used to generate the client/server certificates.

```bash
cfssl gencert -initca ca-csr.json | cfssljson -bare ca
```

## Generate client certificate

This command generates `client.pem` and `client-key.pem`.

```bash
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json client-csr.json | cfssljson -bare client
```

## Generate server certificate

This command generates `server.pem` and `server-key.pem`.

```bash
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -hostname=localhost server-csr.json | cfssljson -bare server
```
