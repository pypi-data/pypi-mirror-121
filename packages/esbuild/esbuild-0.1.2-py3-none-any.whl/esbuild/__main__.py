import os
import sys

from esbuild import EsBuildLauncher


def main() -> None:
    env = os.environ.copy()
    esbuild = EsBuildLauncher(auto_install=True)
    completed_process = esbuild.run(sys.argv[1:], env=env, live_output=True)
    sys.exit(completed_process.returncode)


if __name__ == "__main__":
    main()
