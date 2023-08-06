from datetime import datetime as dt
from pathlib import Path
from enum import Enum, unique
import numpy as np
import re

REGEX_DT_FILENAME = re.compile("^.*(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})-(?P<hour>\d{2})(?P<minutes>\d{2}).*")

@unique
class Subtest(Enum):
    STARTUP = 0
    CHARUP = 1
    CHARDOWN = 2
    TEMPDOWN = 3
    STRESS = 4
    INIT = 10
    TEMPADJ = 11
    TEMPSTAB = 12

def dt_from_filename(dt_string):
    m = REGEX_DT_FILENAME.search(dt_string)
    if m == None: return None
    d = {k: int(v) for k, v in m.groupdict().items()}
    return dt(d["year"], d["month"], d["day"], d["hour"], d["minutes"])

def create_dt_flag():
    now = dt.now()
    return f"{now.year:04d}{now.month:02d}{now.day:02d}-{now.hour:02d}{now.minute:02d}"

def estimator(l, a, b):
    sorted_data = list(l) if hasattr(l, "__iter__") else [l]
    sorted_data.sort()
    prob_data = list(((np.arange(1, len(sorted_data) + 1) - a) / (len(sorted_data) + b)) * 100)
    return sorted_data, prob_data

def benard_estimator(l):
    return estimator(l, 0.3, 0.4)

def remove_data_recursively(data_dir: Path):
    for x in data_dir.iterdir():
        if x.is_dir(): remove_data_recursively(x)
        else: x.unlink()
    for x in data_dir.iterdir():
        if x.is_dir(): x.rmdir()

if __name__ == "__main__":
    l = [0.5, 1, 3.25, 4.85, 2.25]
    df = benard_estimator(l)
    df["test"] = [10,30,50,70,90]

