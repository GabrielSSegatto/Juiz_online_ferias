import os
import subprocess
import tempfile

TIMEOUT = 2.5


def run_java(code: str, input_data: str = "") -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        source_path = os.path.join(tmp, "Main.java")

        with open(source_path, "w", encoding="utf-8") as f:
            f.write(code)

        compile_result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-v", f"{tmp}:/app",
                "juiz-java",
                "javac", "/app/Main.java", "-d", "/app"
            ],
            capture_output=True,
            text=True,
        )

        if compile_result.returncode != 0:
            return {
                "stdout": "",
                "stderr": compile_result.stderr,
                "exit_code": compile_result.returncode,
                "status": "RUNTIME_ERROR"
            }

        try:
            proc = subprocess.run(
                [
                    "docker", "run", "--rm",
                    "-i",
                    "-v", f"{tmp}:/app",
                    "juiz-java",
                    "java", "-cp", "/app", "Main"
                ],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=TIMEOUT,
            )

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