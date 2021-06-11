import ipaddress
import random
import select
import socket
import string
import struct
import sys
import time
from typing import Generator, Union

import click


def generate_chesksum(data: bytes) -> int:
    """
    生成 ICMP 校验位
    """
    n = len(data)
    count = sum(data[i] + ((data[i + 1]) << 8) for i in range(0, n - n % 2, 2))
    count += n % 2 and data[-1]
    count = (count >> 16) + (count & 0xFFFF)
    count += count >> 16
    answer = ~count & 0xFFFF
    return (answer >> 8) | (answer << 8 & 0xFF00)


def ping(
    dst_address: Union[ipaddress.IPv4Address, ipaddress.IPv6Address],
    timeout: float = 1.3,
    packet_size: int = 32,
    interval: float = 0.5,
    max_number_of_times: int = 4,
) -> Generator[int, None, None]:
    """
    ICMP ping
    """
    for i in range(max_number_of_times):
        payload_body = "".join(random.choices(string.ascii_lowercase, k=packet_size)).encode("ascii")
        checksum = generate_chesksum(struct.pack(">BBHHH32s", 8, 0, 0, 0, i + 1, payload_body))
        icmp_packet = struct.pack(">BBHHH32s", 8, 0, checksum, 0, i + 1, payload_body)
        if dst_address.version == 4:
            rawsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        else:
            rawsocket = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_ICMPV6)
        send_request_ping_time = time.time()
        rawsocket.sendto(icmp_packet, (str(dst_address), 0))
        what_ready = select.select([rawsocket], [], [], timeout)
        if what_ready[0] == []:  # Timeout
            yield -1
        else:
            time_received = time.time()
            received_packet, _ = rawsocket.recvfrom(1024)
            icmp_header = received_packet[20:28]
            icmp_type, *_, sequence_id = struct.unpack(">BBHHH", icmp_header)
            if icmp_type == 0 and sequence_id == i + 1:
                yield round((time_received - send_request_ping_time) * 1000)
            else:
                yield -icmp_type

            time.sleep(interval)


@click.command()
@click.argument("target", required=True)
@click.option("--timeout", type=float, default=1.3, show_default=True)
@click.option("--packet-size", type=int, default=32, show_default=True)
@click.option("--interval", type=float, default=0.5, show_default=True)
@click.option("--max-number-of-times", type=int, default=4, show_default=True)
@click.option("--ipv4/--ipv6", "use_ipv4", type=bool, default=True, help="[default: ipv4]")
def main(target: str, timeout: float, packet_size: int, interval: float, max_number_of_times: int, use_ipv4: bool):
    try:
        for family, *_, address in socket.getaddrinfo(target, 0):
            if use_ipv4 and family == socket.AF_INET:
                dst_addr = address[0]
            elif not use_ipv4 and family == socket.AF_INET6:
                dst_addr = address[0]
        dst_addr = ipaddress.ip_address(dst_addr)
    except (socket.gaierror, UnboundLocalError):
        click.secho(f"Ping request could not find host {target}. Please check the name and try again.", fg="red")
        sys.exit(1)

    print(f"Pinging {target} [{dst_addr}] with {packet_size} bytes of data:")
    exit_code = 1  # exit code
    for cast_time in ping(dst_addr, timeout=timeout, packet_size=packet_size, interval=interval, max_number_of_times=max_number_of_times):
        if cast_time == -1:
            click.secho("Ping timeout", fg="yellow")
        elif cast_time < 0:
            click.secho(f"ICMP type: {-cast_time}", fg="yellow")
        else:
            exit_code = 0
            print(f"Reply from {dst_addr}: bytes={packet_size} time={cast_time}ms")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
