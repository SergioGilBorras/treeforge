"""Smoke-test a built wheel in an isolated virtual environment."""
from __future__ import annotations
import glob
from pathlib import Path
import subprocess
import sys
import tempfile
import venv

def main() -> None:
    wheels = glob.glob("dist/treeforge-*.whl")
    if len(wheels) != 1:
        raise SystemExit(f"Expected one TreeForge wheel, found {len(wheels)}")
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        env = root / "venv"
        venv.EnvBuilder(with_pip=True).create(env)
        python = env / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        subprocess.run([str(python), "-m", "pip", "install", "--no-deps",
                        str(Path(wheels[0]).resolve())], check=True)
        code = (
            "from treeforge import TreeForge, TreeConfig; "
            "from pathlib import Path; "
            "t=TreeForge.from_paths(['report.xlsx','data.json','notes.txt','movie.mp4']); "
            "p=Path('smoke.svg'); t.render(p); "
            "s=p.read_text(encoding='utf-8'); "
            "assert all(x in s for x in ('📗','🧩','📃','🎬')); "
            "t.render('smoke.txt'); assert Path('smoke.txt').exists(); "
            "print('Installed wheel smoke test passed')"
        )
        subprocess.run([str(python), "-c", code], cwd=root, check=True)

if __name__ == "__main__":
    main()
