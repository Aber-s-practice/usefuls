# Usefuls

Some useful script by Python3.6+.

All script will be auto register by setup.py.

## Install

It is strongly recommended to use [pipx](https://github.com/pipxproject/pipx) for installation to ensure a clean environment.

```bash
pipx install git+https://github.com/abersheeran/usefuls
```

## Commands

Commands always like `py-xxx`

### DNS

```
> py-dns --help
Usage: py-dns [OPTIONS] DOMAIN
              [[A|AAAA|CNAME|MX|NAPTR|NS|PTR|SOA|SRV|TXT|any]]

Options:
  -NS, --name-server TEXT  DNS Server
  --help                   Show this message and exit.
```
