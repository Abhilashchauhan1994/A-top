import psutil

def collect_cpu_metrics() -> dict:
    return {
        "usage": psutil.cpu_percent(interval=None),
        "cpu_cores": psutil.cpu_count(logical=True),
        "load_average": psutil.getloadavg()
    }