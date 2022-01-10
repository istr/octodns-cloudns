## ClouDNSProvider provider for octoDNS

An [octoDNS](https://github.com/octodns/octodns/) provider that targets [ClouDNS](https://www.cloudns.net/wiki/).

### Installation

#### Command line

```
pip install octodns_cloudns
```

#### requirements.txt/setup.py

Pinning specific versions or SHAs is recommended to avoid unplanned upgrades.

##### Versions

```
# Start with the latest versions and don't just copy what's here
octodns==0.9.14
octodns_cloudns==0.0.1
```

##### SHAs

```
# Start with the latest/specific versions and don't just copy what's here
-e git+https://git@github.com/octodns/octodns.git@9da19749e28f68407a1c246dfdf65663cdc1c422#egg=octodns
-e git+https://git@github.com/octodns/octodns_cloudns.git@ec9661f8b335241ae4746eea467a8509205e6a30#egg=octodns_cloudns
```

### Configuration

ClouDNS allows sub accounts for resellers or to lock and limit access.
For API authentication one of three options could be given exclusively:
`auth_id` for a primary account id, `sub_auth_id` for a sub account,
identified by id, or `sub_auth_user` for sub account, identified by name.

```yaml
providers:
  cloudns:
    class: octodns_cloudns.ClouDNSProvider
    auth_id:
    auth_password:
    sub_auth_id: {for sub accounts}
    sub_auth_user: {alternative for sub accounts}
```

### Support Information

#### Records

ClouDNSProvider supports A, AAAA, ALIAS, CAA, CNAME, MX, NAPTR, NS, PTR,
SSHFP, SPF, SRV, and TXT.

ClouDNSProvider DOES NOT support DNAME, LOC, URLFWD.

ClouDNSProvider could support DNSSEC (DS) and TLSA as well as CERT records.

#### Dynamic

ClouDNSProvider supports dynamic records only when you opt for a special (paid) plan.

### Developement

See the [/script/](/script/) directory for some tools to help with the development process. They generally follow the [Script to rule them all](https://github.com/github/scripts-to-rule-them-all) pattern. Most useful is `./script/bootstrap` which will create a venv and install both the runtime and development related requirements. It will also hook up a pre-commit hook that covers most of what's run by CI.
