"""Local Compose lifecycle; Python 3.12+, no third-party dependencies."""

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STACKS = {
    "database": ["postgres"],
    "backend": ["postgres", "backend"],
    "all": ["postgres", "backend", "ai"],
}


def run(command: list[str], *, capture: bool = False, timeout: int = 60) -> str:
    result = subprocess.run(
        command, cwd=ROOT, check=True, timeout=timeout,
        text=True, encoding="utf-8", errors="replace", capture_output=capture,
    )
    return result.stdout.strip() if capture else ""


def compose_command(project: str, env_file: Path) -> list[str]:
    # Explicit file/project/profiles prevent ambient COMPOSE_FILE/PROFILES from
    # changing which project down targets. Services are selected separately.
    return [
        "docker", "compose", "--project-directory", str(ROOT),
        "--file", str(ROOT / "compose.yaml"), "--project-name", project,
        "--env-file", str(env_file), "--profile", "backend", "--profile", "ai",
    ]


def initialize(env_file: Path) -> None:
    # Exclusive creation also protects an existing file in a concurrent invocation.
    try:
        with env_file.open("x", encoding="utf-8", newline="\n") as target:
            target.write((ROOT / ".env.example").read_text(encoding="utf-8"))
    except FileExistsError:
        print(f"Kept existing configuration: {env_file}")
    else:
        print(f"Created configuration: {env_file}")


def doctor(command: list[str], services: list[str]) -> None:
    for service, repo in (("backend", "HPC-be"), ("ai", "HPC-ai")):
        if service in services and not (ROOT.parent / repo / "Dockerfile").is_file():
            raise RuntimeError(f"Missing sibling repository: {repo} (see docs/local-testing.md)")
    run(["docker", "compose", "version"])
    if run(["docker", "info", "--format", "{{.OSType}}"], capture=True) != "linux":
        raise RuntimeError("Start Docker Desktop with the Linux container engine.")
    run(command + ["config", "--quiet"])
    print("Docker engine, Compose configuration and required sibling repositories: OK")


def health(command: list[str], services: list[str]) -> None:
    # Read readiness from the selected project's actual containers, not another
    # process that happens to answer on a configured host port.
    for service in services:
        container = run(command + ["ps", "--quiet", service], capture=True)
        if not container or "\n" in container:
            raise RuntimeError(f"Expected one running {service} container; run up/status first.")
        state = json.loads(run(["docker", "inspect", "--format", "{{json .State}}", container], capture=True))
        if not state.get("Running") or ("Health" in state and state["Health"]["Status"] != "healthy"):
            raise RuntimeError(f"{service} is not healthy; run status and inspect Compose logs.")
        if service == "postgres":
            print("postgres: healthy")
            continue
        port, path, expected = (
            (8080, "/actuator/health", {"status": "UP"}) if service == "backend"
            else (8000, "/health", {"status": "ok", "service": "hpc-ai"})
        )
        address = run(command + ["port", service, str(port)], capture=True)
        if not re.fullmatch(r"127\.0\.0\.1:\d+", address):
            raise RuntimeError(f"Unexpected {service} binding; expected one IPv4 loopback port.")
        url = f"http://{address}{path}"
        # Local health checks should not use a developer's HTTP proxy.
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        # The BE image has no Docker HEALTHCHECK. Its HTTP endpoint is the
        # readiness gate; compose --wait alone only observes a running process.
        deadline = time.monotonic() + 90
        while True:
            try:
                with opener.open(url, timeout=5) as response:
                    body = json.load(response)
                if isinstance(body, dict) and all(body.get(key) == value for key, value in expected.items()):
                    break
            except (OSError, ValueError, urllib.error.URLError):
                pass
            if time.monotonic() >= deadline:
                raise RuntimeError(f"{service} did not return the expected health response within 90 seconds.")
            time.sleep(2)
        print(f"{service}: healthy ({url})")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["init", "doctor", "up", "status", "health", "down"])
    parser.add_argument("--stack", choices=STACKS, default="backend", help="services for doctor/up/health (default: backend)")
    parser.add_argument("--project", default="hpc-dev", help="use the same project on every command")
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env", help="relative paths are relative to the workspace repository")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", args.project):
        parser.error("--project must use lowercase letters, digits, hyphens or underscores")
    env_file = args.env_file if args.env_file.is_absolute() else ROOT / args.env_file
    if args.action == "init":
        initialize(env_file)
        return 0
    if not env_file.is_file():
        raise RuntimeError("Missing env file. Run init, then review ports before running up.")
    command = compose_command(args.project, env_file)
    services = STACKS[args.stack]
    print(f"Project: {args.project}; stack: {args.stack}", flush=True)
    if args.action in ("doctor", "up"):
        doctor(command, services)
    if args.action == "up":
        run(command + ["up", "--detach", "--build", "--wait", "--wait-timeout", "180", *services], timeout=1800)
        health(command, services)
    elif args.action == "health":
        health(command, services)
    elif args.action == "status":
        run(command + ["ps", "--all"])
    elif args.action == "down":
        # All known profiles, no --volumes and no --remove-orphans.
        run(command + ["down"], timeout=180)
        print("Stopped this Compose project. Database volumes were preserved.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, subprocess.SubprocessError, urllib.error.URLError) as error:
        # Do not dump captured Compose config or environment values on failure.
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
