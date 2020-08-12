import multiprocessing

from pathlib import Path

bind = "0.0.0.0:20999"
workers = min(multiprocessing.cpu_count(), 2)

accesslog = str(Path('log/access.log').absolute())
errorlog = str(Path('log/error.log').absolute())
