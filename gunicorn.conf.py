import multiprocessing

from pathlib import Path

bind = "0.0.0.0:5000"
workers = min(multiprocessing.cpu_count(), 2)
