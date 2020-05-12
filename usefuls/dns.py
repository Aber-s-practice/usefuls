import asyncio
from typing import Dict, List

import click
import aiodns

try:
    import uvloop

    uvloop.install()
except ImportError:
    pass

loop = asyncio.get_event_loop()

DNS_TYPE = [
    "A",
    "AAAA",
    "CNAME",
    "MX",
    "NAPTR",
    "NS",
    "PTR",
    "SOA",
    "SRV",
    "TXT",
]


def get_dns_info(dns_resp) -> Dict[str, str]:
    return {
        attr: getattr(dns_resp, attr)
        for attr in dir(dns_resp)
        if not attr.startswith("_")
    }


async def query(domain: str, dns_type: str) -> List[Dict[str, str]]:
    resolver = aiodns.DNSResolver()
    try:
        record = await resolver.query(domain, dns_type)
    except aiodns.error.DNSError as e:
        return [{"status": "failed", "message": e.args[1]}]

    if isinstance(record, list):
        if not record:
            result = [
                {
                    "status": "failed",
                    "message": "DNS server returned answer with no data",
                }
            ]
        else:
            result = [get_dns_info(_record) for _record in record]
    else:
        result = [get_dns_info(record)]

    return result


def display_dns_info(data: List[Dict[str, str]], prefix: str = "") -> None:
    for line in data:
        for key, value in line.items():
            if key == "type":
                continue
            print(prefix + key, ":", value)
        print("")


@click.command()
@click.argument("domain")
@click.argument(
    "dns-type",
    type=click.Choice(DNS_TYPE + ["any"], case_sensitive=True),
    default="any",
)
def main(domain: str = None, dns_type: str = "any"):
    print("----------> DNS INFO <----------")
    if dns_type == "any":
        results = loop.run_until_complete(
            asyncio.gather(
                *[query(domain, _dns_type) for _dns_type in DNS_TYPE],
                return_exceptions=True,
            )
        )
        for index, _result in enumerate(results):
            print("TYPE:", DNS_TYPE[index])
            display_dns_info(_result, "   ")
    else:
        display_dns_info(loop.run_until_complete(query(domain, dns_type)))


if __name__ == "__main__":
    main()
