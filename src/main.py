# Should be run, to start all DNS server etc.

# std libraries
from time import sleep
from json import loads as load_json
from typing import Callable
# local libraries
from dns.dns_server_batch import DnsServerBatch
from http_server.http_server_batch import HttpServerBatch


def started_as_main() -> bool:
    return __name__ == "__main__"


def main():
    dns_config, http_config = load_config()
    dns_servers = run_server_batch(DnsServerBatch, dns_config)
    http_servers = run_server_batch(HttpServerBatch, http_config)
    run_till_interrupt(dns_servers, http_servers)


def load_config(config_file: str = "../rsrc/config.json") -> ({str: str}, {str: str}):
    config_dic = _load_dict_from_json(config_file)
    dns_config = config_dic["DnsConfig"]
    http_config = config_dic["HttpConfig"]
    return dns_config, http_config


def _load_dict_from_json(filename: str) -> {}:
    with open(filename) as file:
        json_str = file.read()
    read_dic = load_json(json_str)
    return read_dic


def run_server_batch(
        batch_class: Callable, config: {str: str}
) -> DnsServerBatch or HttpServerBatch:
    server_batch = batch_class(config)
    server_batch.run_all()
    return server_batch


def run_till_interrupt(
        *stop_after_interrupt: (DnsServerBatch or HttpServerBatch)):
    try:
        _sleep_forever()
    except KeyboardInterrupt:  # Ctrl + C
        _stop_servers(stop_after_interrupt)


def _sleep_forever() -> None:
    while True:
        sleep(60)


def _stop_servers(servers: (DnsServerBatch or HttpServerBatch)) -> None:
    for server_batch in servers:
        server_batch.stop_all()
    print("Processing stopped, sockets will remain blocked.")


if started_as_main():
    main()