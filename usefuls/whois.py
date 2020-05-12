#!/usr/bin/python3
import os
import re
import socket
from functools import wraps

import click
import requests as req
from mecache import File


file = File(os.path.join(os.environ["HOME"], ".usefuls", "cache", "whois.cache"))


class WhoisError(Exception):
    pass


class SuffixDontExists(WhoisError):
    pass


class NoWhoisServer(WhoisError):
    pass


def punycode(domain):
    result = []
    for _ in domain.split("."):
        try:
            _.encode("ascii")
            result.append(_)
        except UnicodeEncodeError:
            result.append("xn--" + _.encode("punycode").decode("ascii"))
    return ".".join(result)


@file.cache(30 * 24 * 60 * 60, lambda suffix: suffix)
def whois_server(suffix):
    resp = req.get(
        "https://www.iana.org/domains/root/db/" + suffix + ".html", timeout=3
    )
    if resp.status_code == 404:
        raise SuffixDontExists("此域名后缀不存在")

    try:
        return re.search(r"WHOIS Server:</b>\s*(?P<whois>.*)", resp.text).group("whois")
    except AttributeError:
        raise NoWhoisServer("未找到此域名的 Whois 服务器")


def whois(server, domain):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server, 43))
        s.send(domain.encode("UTF-8") + b"\r\n")
        result = bytearray()
        while True:
            data = s.recv(4096)
            if not len(data):
                break
            result.extend(data)
        s.close()
    return bytes(result).decode("utf-8")


def parse(whois_data):
    # TODO better parse
    data = re.sub(">>>[\s\S]+", "", whois_data)
    return data


@click.command()
@click.argument("domain", required=True)
def main(domain: str = None):
    data = parse(whois(whois_server(domain.split(".")[-1]), domain))
    print(data)


if __name__ == "__main__":
    main()
