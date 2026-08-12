import os
import subprocess
import tempfile
import logging

TIMEOUT = 2.5
BASE_RUNNER_DIR = "/tmp/juiz_runners"
os.makedirs(BASE_RUNNER_DIR, exist_ok=True)

def run_c(code: str, input_data: str = "") -> dict:
    with tempfile.TemporaryDirectory(dir=BASE_RUNNER_DIR) as tmp:
        path = os.path.join(tmp, "main.c")
        binary = os.path.join(tmp, "main")

        with open(path, "w") as f:
            f.write(code)

        # Passo 1: Compilação
        compile = subprocess.run(
            [
                "docker", "run", "--rm",
                "-v", f"{tmp}:/app",
                "juiz-c",
                "gcc", "/app/main.c", "-O2", "-o", "/app/main"
            ],
            capture_output=True,
            text=True
        )

        if compile.returncode != 0:
            logging.error(f"Erro na compilação (C): {compile.stderr}")
            return {
                "stdout": "",
                "stderr": compile.stderr,
                "exit_code": compile.returncode,
                "status": "RUNTIME_ERROR"
            }

        # Passo 2: Execução
        try:
            proc = subprocess.run(
                [
                    "docker", "run", "--rm",
                    "-i",
                    "-v", f"{tmp}:/app",
                    "juiz-c",
                    "/app/main"
                ],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=TIMEOUT
            )

            if proc.returncode != 0:
                logging.error(f"Erro no Docker Runner (C): {proc.stderr}")

            return {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "exit_code": proc.returncode,
                "status": "OK" if proc.returncode == 0 else "RUNTIME_ERROR"
            }

        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": "Time Limit Exceeded",
                "exit_code": -1,
                "status": "TLE"
            }
            
        except Exception as e:
            logging.error(f"Exceção Crítica no subprocess (C): {e}")
            return {
                "stdout": "",
                "stderr": str(e),
                "exit_code": -1,
                "status": "RUNTIME_ERROR"
            }
