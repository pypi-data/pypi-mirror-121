import os
import pathlib
import shlex
import subprocess
from typing import Union

from esbuild.installation import install

from .exceptions import EsbuildBinNotFound

ESBUILD_VERSION = "0.12.28"


class EsBuildLauncher:
    def __init__(
        self,
        auto_install: bool = False,
        bin_path: str = None,
        cwd: str = None,
    ):
        self.auto_install = auto_install
        self.cwd = cwd
        self.bin_path = bin_path or get_bin_path_root() / "esbuild"

    def run(
        self,
        cli_args: Union[list, str],
        cwd: pathlib.Path = None,
        env: dict = None,
        live_output=False,
    ):
        if self.auto_install and not self.bin_path.exists():
            self.install(ESBUILD_VERSION)

        if isinstance(cli_args, str):
            cli_args = shlex.split(cli_args)

        opts = {
            "cwd": cwd or self.cwd or os.getcwd(),
            "env": env or {},
        }
        if live_output is False:
            opts.update(
                {
                    "capture_output": True,
                    "check": True,
                }
            )

        try:
            output = subprocess.run([str(self.bin_path)] + cli_args, **opts)
            if live_output:
                return output
            return output.stdout.decode().strip()
        except FileNotFoundError as err:
            raise EsbuildBinNotFound(err)

    def install(self, version=ESBUILD_VERSION):
        return install(version, self.bin_path)


def get_bin_path_root():
    return pathlib.Path(__file__).parent.resolve() / "bin"
