import socket
import sys
import time
from urllib.parse import urlsplit

import click
import socks


def set_proxy(ctx, param, value):
    if not value:
        return
    split_result = urlsplit(value)
    socks.set_default_proxy(
        socks.PROXY_TYPES[split_result.scheme.upper()],
        split_result.hostname,
        split_result.port,
        rdns=True,
        username=split_result.username,
        password=split_result.password,
    )
    socket.socket = socks.socksocket
    click.secho(f"Set proxy: {split_result.geturl()}", fg="blue")


@click.command()
@click.argument("target", type=(str, int))
@click.option("--timeout", type=float, default=1.3, show_default=True)
@click.option("--interval", type=float, default=0.5, show_default=True)
@click.option("--max-number-of-times", type=int, default=4, show_default=True)
@click.option("--proxy", expose_value=False, callback=set_proxy)
def main(target: str, timeout: float, interval: float, max_number_of_times: int):
    print(f"TCP connect to {target}:")
    exit_code = 1  # exit code
    for _ in range(max_number_of_times):
        start_time = time.time()
        try:
            connection = socket.socket()
            connection.settimeout(timeout)
            connection.connect(target)
        except socket.timeout:
            click.secho("Connect timeout", fg="yellow")
        except socks.ProxyError as e:
            click.secho(f"Proxy error: {e}", fg="red")
        else:
            end_time = time.time()
            cast_time = round((end_time - start_time) * 1000)
            exit_code = 0
            print(
                f"Connecting to {connection.getpeername()} from {connection.getsockname()}: {cast_time}ms"
            )
            connection.close()
            time.sleep(interval)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
