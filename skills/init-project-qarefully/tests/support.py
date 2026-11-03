"""Shared fixtures: temp repository builder + script runner."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True  # in-process load_script never leaves scripts/__pycache__
SCRIPTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts")
HAS_GIT = shutil.which("git") is not None


def run(script, *args, cwd=None, env=None):
    """-> (exit code, stdout lines, stderr). Child stdio decoded strictly as UTF-8."""
    done = subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *args], capture_output=True,
                          text=True, encoding="utf-8", errors="strict", cwd=cwd, env=env)
    return done.returncode, done.stdout.splitlines(), done.stderr


def legacy_env():
    """Environment forcing child default stdio encoding (Windows pipe -> cp1252): no UTF-8 mode overrides."""
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONIOENCODING", "PYTHONUTF8")}
    env["PYTHONUTF8"] = "0"
    return env


def load_script(name):
    """-> fresh module object for scripts/<name>.py (in-process tests)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), os.path.join(SCRIPTS, name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RepoCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, "repo")
        os.makedirs(self.root)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, rel, text="x\n", base=None):
        path = os.path.join(base or self.root, *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        return path

    def git(self, *args):
        subprocess.run(["git", "-C", self.root, "-c", "user.name=t", "-c", "user.email=t@t", "-c",
                        "core.autocrlf=false", *args], check=True, capture_output=True)

    def commit_all(self):
        self.git("init", "-q")
        self.git("config", "core.autocrlf", "false")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "init")
