from typing import Generator, Tuple
from logging import getLogger
from subprocess import run


logger = getLogger("get_generator.py")


def generate_pid_errors_file(log_file: str, output_file: str = "pid_errors.log") -> str:
    run(
        f"grep -oP '\[PRODUCT_ERROR\]:\s\w*' {log_file} | awk -F\" \" '{{ print $2 }}' | sort | uniq -u 1> {output_file}",
        shell=True,
    )
    return output_file
