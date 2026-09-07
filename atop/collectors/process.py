import psutil


def collect_process_metrics() -> dict:
    processes = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "username",
            "status",
            "memory_percent",
            "cpu_percent",
            "num_threads",
        ]
    ):
        try:
            info = process.info

            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "username": info["username"],
                "status": info["status"],
                "cpu_percent": info["cpu_percent"],
                "memory_percent": info["memory_percent"],
                "num_threads": info["num_threads"],
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    processes.sort(
        key=lambda process: process["cpu_percent"],
        reverse=True
    )

    return {
        "processes": processes[:20]
    }