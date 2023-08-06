def _infer_threads() -> int:
    from os import cpu_count
    found_cpus = cpu_count()
    if found_cpus is None:
        threads = 4
    else:
        threads = found_cpus - 1
    return threads
