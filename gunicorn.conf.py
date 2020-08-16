import multiprocessing

from pathlib import Path

bind = "localhost:5000"
workers = min(multiprocessing.cpu_count(), 2)

accesslog = str(Path('log/access.log').absolute())
errorlog = str(Path('log/error.log').absolute())
