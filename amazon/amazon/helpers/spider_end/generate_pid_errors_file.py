from logging import getLogger
from subprocess import run


logger = getLogger("get_generator.py")


def generate_pid_errors_file(
    log_file: str = "logs.log", output_file: str = "pid_errors.log"
) -> str:
    """
    Faz a captura das PID (product id da amazon) que podem ter não ter subido corretamente ao banco de dados.
    Funcão utilizada no final do processo.
    Args:
        * log_file: nome do arquivo de logs gerado pelo scrap. Por padrão logs.log
        * output_file: nome do arquivo de saída dos pids únicos com possíveis erros
    """
    run(
        f"grep -oP '\[PRODUCT_ERROR\]:\s\w*' {log_file} | awk -F\" \" '{{ print $2 }}' 1> {output_file}",
        shell=True,
    )
    return output_file
