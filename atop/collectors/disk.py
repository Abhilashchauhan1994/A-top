import psutil


def collect_disk_metrics() -> dict:
    filesystems = []

    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)

            filesystems.append({
                "device": partition.device,
                "mountpoint": partition.mountpoint,
                "fstype": partition.fstype,
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "percent": usage.percent,
            })

        except (PermissionError, OSError):
            continue

    io = psutil.disk_io_counters()

    io_metrics={
        "read_bytes": 0,
        "write_bytes":0,
        "read_count": 0,
        "write_count":0,
    }

    if io:
        io_metrics={
            "read_bytes": io.read_bytes,
            "write_bytes": io.write_bytes,
            "read_count": io.read_count,
            "write_count": io.write_count,
        }
    return {
        "filesystems": filesystems,
        "io": io_metrics
    }