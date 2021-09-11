import asyncio

import click
import dns.message
import dns.asyncquery
import dns.resolver

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


async def query(nameserver: str, domain: str, dns_type: str) -> dns.message.Message:
    query = dns.message.make_query(domain, dns_type)
    result = await dns.asyncquery.udp(query, nameserver)
    return result


def display_result(result: dns.message.Message) -> None:
    for line in "\n".join([str(a) for a in result.answer]).splitlines():
        print(" " * 2 + line)


@click.command()
@click.option("-NS", "--nameserver", help="DNS Server")
@click.argument("domain")
@click.argument(
    "dns-type",
    type=click.Choice(DNS_TYPE + ["ALL"], case_sensitive=True),
    default="ALL",
)
def main(domain: str = None, dns_type: str = "ALL", nameserver: str = None):
    if nameserver is None:
        nameserver = dns.resolver.BaseResolver().nameservers[0]
    if dns_type == "ALL":
        dns_types = DNS_TYPE
    else:
        dns_types = [dns_type]
    click.secho(f"Querying {domain} {dns_types} records, from {nameserver}", fg="green")

    tasks = []
    for _dns_type in dns_types:
        task = asyncio.ensure_future(query(nameserver, domain, _dns_type))
        task.add_done_callback(lambda future: display_result(future.result()))
        tasks.append(task)
    loop.run_until_complete(asyncio.gather(*tasks))


if __name__ == "__main__":
    main()
