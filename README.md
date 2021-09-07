# Usefuls

Some useful script by Python3.6+.

All script will be auto register by setup.py.

## Install

It is strongly recommended to use [pipx](https://github.com/pipxproject/pipx) for installation to ensure a clean environment.

```bash
pipx install git+https://github.com/abersheeran/usefuls
```

In China, you can also install from [Gitee](https://gitee.com/abersheeran/usefuls)

```bash
pipx install git+https://gitee.com/abersheeran/usefuls
```

## Commands

Commands always like `py-xxx`. So, you can type `py-` and then use `Tab` to use autocomplete.

### dns

Need `dnspython`, run `pipx inject usefuls dnspython`.

```
> py-dns --help
Usage: py-dns [OPTIONS] DOMAIN
              [[A|AAAA|CNAME|MX|NAPTR|NS|PTR|SOA|SRV|TXT|ALL]]

Options:
  -NS, --name-server TEXT  DNS Server
  --help                   Show this message and exit.
```

### whois

Need `requests` and `mecache`, run `pipx inject usefuls requests mecache`.

```
> py-whois --help
Usage: py-whois [OPTIONS] DOMAIN

Options:
  --help  Show this message and exit.
```

### ping

```
> py-ping --help
Usage: py-ping [OPTIONS] TARGET

Options:
  --timeout FLOAT                [default: 1.3]
  --packet-size INTEGER          [default: 32]
  --interval FLOAT               [default: 0.5]
  --max-number-of-times INTEGER  [default: 4]
  --ipv4 / --ipv6                [default: ipv4]
  --help                         Show this message and exit.
```

### tcping

Need `pysocks`, run `pipx inject usefuls pysocks`.

```
Usage: py-tcping [OPTIONS] TARGET...

Options:
  --timeout FLOAT                [default: 1.3]
  --interval FLOAT               [default: 0.5]
  --max-number-of-times INTEGER  [default: 4]
  --proxy TEXT
  --help                         Show this message and exit.
```
