import os
import subprocess
import tempfile
import logging

TIMEOUT = 5.0
BASE_RUNNER_DIR = "/tmp/juiz_runners"
os.makedirs(BASE_RUNNER_DIR, exist_ok=True)

def run_python(code: str, input_data: str = "") -> dict:
    with tempfile.TemporaryDirectory(dir=BASE_RUNNER_DIR) as tmp:
        path = os.path.join(tmp, "main.py")

        with open(path, "w") as f:
            f.write(code)

        try:
            proc = subprocess.run(
                [
                    "docker", "run", "--rm",
                    "-i",
                    "-v", f"{tmp}:/app",
                    "juiz-python",
                    "python3", "/app/main.py"
                ],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=TIMEOUT
            )

            if proc.returncode != 0:
                logging.error(f"Erro no Docker Runner: {proc.stderr}")
                print(f"ERRO DOCKER STDERR: {proc.stderr}")

            return {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "exit_code": proc.returncode,
                "status": "OK" if proc.returncode == 0 else "RUNTIME_ERROR"
            }

        except Exception as e:
            logging.error(f"Exceção Crítica no subprocess: {e}")
            return {
                "stdout": "",
                "stderr": str(e),
                "exit_code": -1,
                "status": "RUNTIME_ERROR"
            }

        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": "Time Limit Exceeded",
                "exit_code": -1,
                "status": "TLE"
            }
