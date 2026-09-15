import psutil


def collect_system_summary() -> dict:
    total_processes = 0
    total_threads = 0
    running_processes = 0
    sleeping_processes = 0
    disk_sleep_processes = 0
    zombie_processes = 0

    for process in psutil.process_iter(
        ["status", "num_threads"]
    ):
        try:
            info = process.info

            status = info["status"]
            threads = info["num_threads"] or 0

            total_processes += 1
            total_threads += threads

            if status == psutil.STATUS_RUNNING:
                running_processes += 1

            elif status == psutil.STATUS_SLEEPING:
                sleeping_processes += 1

            elif status == psutil.STATUS_DISK_SLEEP:
                disk_sleep_processes += 1

            elif status == psutil.STATUS_ZOMBIE:
                zombie_processes += 1

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    login_users = len(psutil.users())

    return {
        "total_processes": total_processes,
        "total_threads": total_threads,
        "running_processes": running_processes,
        "sleeping_processes": sleeping_processes,
        "disk_sleep_processes": disk_sleep_processes,
        "zombie_processes": zombie_processes,
        "login_users": login_users,
    }