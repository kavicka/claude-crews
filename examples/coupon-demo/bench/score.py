"""Score a finished attempt: its own tests, typecheck, the hidden tests and the probe.

    python3 bench/score.py <work dir>
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
HIDDEN = HERE.parent / "hidden" / "acceptance.test.ts"


def vitest_json(work: Path, *args: str) -> dict:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
        out = Path(fh.name)
    subprocess.run(["npx", "vitest", "run", *args, "--reporter=json", f"--outputFile={out}"],
                   cwd=work, capture_output=True, text=True, timeout=600)
    try:
        return json.loads(out.read_text() or "{}")
    except (json.JSONDecodeError, FileNotFoundError):
        return {}
    finally:
        out.unlink(missing_ok=True)


def score(work: Path) -> dict:
    work = Path(work)
    own = vitest_json(work)
    typecheck = subprocess.run(["npx", "tsc", "--noEmit"], cwd=work, capture_output=True, text=True, timeout=600)

    shutil.copy(HIDDEN, work / "src" / "acceptance.test.ts")
    shutil.copy(HERE / "probe.test.ts", work / "src" / "zz-probe.test.ts")
    try:
        hidden = vitest_json(work, "src/acceptance.test.ts")
        results = [a for f in hidden.get("testResults", []) for a in f.get("assertionResults", [])]
        failed = [re.match(r"(\w\d)", a["title"]).group(1) for a in results if a["status"] != "passed"]

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
            probe_out = Path(fh.name)
        subprocess.run(["npx", "vitest", "run", "src/zz-probe.test.ts"], cwd=work, capture_output=True,
                       text=True, timeout=600, env={**os.environ, "PROBE_OUT": str(probe_out)})
        try:
            probe = json.loads(probe_out.read_text() or "{}")
        except (json.JSONDecodeError, FileNotFoundError):
            probe = {"error": "probe did not run"}
        probe_out.unlink(missing_ok=True)
    finally:
        for name in ("acceptance.test.ts", "zz-probe.test.ts"):
            (work / "src" / name).unlink(missing_ok=True)

    return {
        "own_tests_passed": own.get("numPassedTests", 0),
        "own_tests_total": own.get("numTotalTests", 0),
        "typecheck_ok": typecheck.returncode == 0,
        "hidden_passed": sum(a["status"] == "passed" for a in results),
        "hidden_total": len(results),
        "hidden_failed": failed,
        "probe": probe,
    }


if __name__ == "__main__":
    print(json.dumps(score(Path(sys.argv[1])), indent=2))
