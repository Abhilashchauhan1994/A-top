from atop.collectors.cpu import collect_cpu_metrics
from atop.collectors.disk import collect_disk_metrics
from atop.collectors.memory import collect_memory_metrics
from atop.collectors.network import collect_network_metrics
from atop.collectors.process import collect_process_metrics
from atop.collectors.system import collect_system_summary


def collect_metrics() -> dict:
    return {
        "cpu": collect_cpu_metrics(),
        "memory": collect_memory_metrics(),
        "disk": collect_disk_metrics(),
        "network": collect_network_metrics(),
        "process": collect_process_metrics(),
        "system": collect_system_summary(),
    }