import sys
import os
from typing import Set


def extract_set_keys(f: str) -> Set[str]:
    output_set = set()
    with open(f, "r") as finput:
        for line in finput:
            k = line.split("=")[0]
            output_set.add(k)
    return output_set


def ensure_same_keys(data, whole_set):
    fail = False
    for k, v in data.items():
        if v != whole_set:
            print(f"some keys are missing in {k} but present in other .env files")
            print(whole_set - v)
            fail = True
    return fail


def main():
    """Console script for check_env_sample."""
    files = [f for f in os.listdir() if f.startswith(".env")]
    data = {}
    whole_set = set()
    for f in files:
        key_set = extract_set_keys(f)
        data[f] = key_set
        whole_set = whole_set | key_set

    return ensure_same_keys(data, whole_set)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cove
