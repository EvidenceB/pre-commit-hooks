import sys
import os
from typing import Set

FAIL = 1
SUCCESS = 0

def extract_set_keys(f: str) -> Set[str]:
    output_set = set()
    with open(f, "r") as finput:
        for line in finput:
            if "=" not in line:
                continue
            k = line.split("=")[0]
            output_set.add(k)
    return output_set


def ensure_same_keys(data, whole_set):
    status = SUCCESS
    for k, v in data.items():
        if v != whole_set:
            print(f"some keys are missing in {k} but present in other .env files")
            print(whole_set - v)
            status = FAIL
    return status

def look_for(prefix):
    return [prefix, prefix+".prod", prefix+".production",
            prefix+".staging", prefix+".dev", prefix+".sample"]


def main():
    """Console script for check_env_sample."""
    files = [f for f in os.listdir() if f.startswith(".env")]
    files_ending_with_sample = [f for f in files if f.endswith(".sample")]
    statuses = []
    for sample in files_ending_with_sample:
        prefix = sample.replace(".sample", "")
        prefixed_files = [f for f in files if f in look_for(prefix)]
        data = {}
        whole_set = set()
        for f in prefixed_files:
            key_set = extract_set_keys(f)
            data[f] = key_set
            whole_set = whole_set | key_set
        statuses.append(ensure_same_keys(data, whole_set))
    for s in statuses:
        if s == FAIL:
            return FAIL
    return SUCCESS

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cove
