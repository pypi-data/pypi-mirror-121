import os
import pathlib
import platform
import shutil
import ssl
import urllib.request
from tempfile import mkdtemp


def install(version, bin_path):
    if os.path.isfile(bin_path):
        os.remove(bin_path)
    os.makedirs(bin_path.parent, exist_ok=True)

    name = f"esbuild-{target()}"
    url = f"https://registry.npmjs.org/{name}/-/{name}-{version}.tgz"

    downloaded_tar_filepath = download_file(url)

    extract_to_dirpath = downloaded_tar_filepath.parent / "esbuild"
    extract_file(downloaded_tar_filepath, extract_to_dirpath)

    shutil.copy(extract_to_dirpath / "package" / "bin" / "esbuild", bin_path)


def target():
    """
    Returns target for current OS and CPU architecture.

    # Available esbuild targets: https://github.com/evanw/esbuild/tree/master/npm
    """
    return get_target(os_name=platform.system(), arch=platform.machine())


def get_target(os_name, arch):
    """
    Gets target name for provided OS name and CPU architecture.
    """
    os_name = os_name.lower().replace("win32", "windows")
    return {
        "amd64": f"{os_name}-64",
        "x86_64": f"{os_name}-64",
        "aarch64": f"{os_name}-arm64",
        "arm": f"{os_name}-arm64" if os_name == "darwin" else f"{os_name}-arm",
    }[arch]


def download_file(url):
    """
    Downloads a file to a temp directory
    """
    temp_dir = mkdtemp()
    working_dir = pathlib.Path(temp_dir)
    dest_filename = working_dir / os.path.basename(url)

    # Ensures SSL certificate verification doesn't fail
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(url, str(dest_filename))

    return dest_filename


def extract_file(filename, extract_dir):
    return shutil.unpack_archive(filename, extract_dir)
