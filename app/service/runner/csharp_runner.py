import os
import subprocess
import tempfile

TIMEOUT = 2.5
BASE_RUNNER_DIR = "/tmp/juiz_runners"

def run_csharp(code: str, input_data: str = "") -> dict:
    os.makedirs(BASE_RUNNER_DIR, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=BASE_RUNNER_DIR) as tmp:
        source_path = os.path.join(tmp, "Program.cs")
        project_path = os.path.join(tmp, "Main.csproj")

        with open(source_path, "w", encoding="utf-8") as f:
            f.write(code)

        project_contents = (
            '<Project Sdk="Microsoft.NET.Sdk">\n'
            '  <PropertyGroup>\n'
            '    <OutputType>Exe</OutputType>\n'
            '    <TargetFramework>net8.0</TargetFramework>\n'
            '    <ImplicitUsings>enable</ImplicitUsings>\n'
            '    <Nullable>enable</Nullable>\n'
            '  </PropertyGroup>\n'
            '</Project>\n'
        )

        with open(project_path, "w", encoding="utf-8") as f:
            f.write(project_contents)

        compile_result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-v", f"{tmp}:/app",
                "juiz-csharp",
                "dotnet", "build", "/app/Main.csproj", "-c", "Release", "--nologo"
            ],
            capture_output=True,
            text=True,
        )

        if compile_result.returncode != 0:
            return {
                "stdout": "",
                "stderr": (compile_result.stdout or "") + (compile_result.stderr or ""),
                "exit_code": compile_result.returncode,
                "status": "RUNTIME_ERROR"
            }

        try:
            proc = subprocess.run(
                [
                    "docker", "run", "--rm",
                    "-i",
                    "-v", f"{tmp}:/app",
                    "juiz-csharp",
                    "dotnet", "/app/bin/Release/net8.0/Main.dll"
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
