import psutil


def collect_network_metrics() -> dict:
    interfaces = psutil.net_io_counters(pernic=True)

    network = {}

    for name, stats in interfaces.items():
        network[name] = {
            "bytes_sent": stats.bytes_sent,
            "bytes_recv": stats.bytes_recv,
            "packets_sent": stats.packets_sent,
            "packets_recv": stats.packets_recv,
            "errin": stats.errin,
            "errout": stats.errout,
            "dropin": stats.dropin,
            "dropout": stats.dropout,
        }

    return {
        "interfaces": network,
    }