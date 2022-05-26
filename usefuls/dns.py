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


async def query(
    method: str, nameserver: str, timeout: float, domain: str, dns_type: str
) -> dns.message.Message:
    query = dns.message.make_query(domain, dns_type)
    if method == "udp":
        func = dns.asyncquery.udp
    elif method == "tcp":
        func = dns.asyncquery.tcp
    elif method == "tls":
        func = dns.asyncquery.tls
    elif method == "https":
        func = dns.asyncquery.https
    result = await func(query, nameserver, timeout=timeout)
    return result


def display_result(result: dns.message.Message) -> None:
    for line in "\n".join([str(a) for a in result.answer]).splitlines():
        print(" " * 2 + line)


@click.command()
@click.option("-NS", "--nameserver", help="DNS Server")
@click.option(
    "-M",
    "--method",
    type=click.Choice(["udp", "tcp", "tls", "https"], case_sensitive=False),
    default="udp",
)
@click.option("-T", "--timeout", type=float, default=3)
@click.argument("domain")
@click.argument(
    "dns-type",
    type=click.Choice(DNS_TYPE + ["ALL"], case_sensitive=False),
    default="ALL",
)
def main(
    domain: str = None,
    dns_type: str = "ALL",
    nameserver: str = None,
    method: str = "udp",
    timeout: float = 3,
):
    if nameserver is None:
        nameserver = dns.resolver.BaseResolver().nameservers[0]
    if dns_type == "ALL":
        dns_types = DNS_TYPE
    else:
        dns_types = [dns_type.upper()]
    click.secho(f"Querying {domain} {dns_types} records, from {nameserver}", fg="green")

    tasks = []
    for _dns_type in dns_types:
        task = asyncio.ensure_future(
            query(method, nameserver, timeout, domain, _dns_type)
        )
        task.add_done_callback(
            lambda future: click.secho(str(future.exception()), fg="red")
            if future.exception()
            else display_result(future.result())
        )
        tasks.append(task)
    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))


if __name__ == "__main__":
    main()
