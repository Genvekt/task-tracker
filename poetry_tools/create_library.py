import platform
import shutil
import subprocess
import sys
from pathlib import Path

import toml

NAMESPACE = "library"


def create_library(library_name):
    poetry_command = f"poetry new {library_name}"

    shell = platform.system() == "Windows"

    process = subprocess.Popen(
        poetry_command.split(),
        stdout=subprocess.PIPE,
        cwd='libraries',
        shell=shell
    )
    output, error = process.communicate()

    if error is None:

        # Edit toml file to include prefix
        toml_file = toml.load(f"libraries/{library_name}/pyproject.toml")
        toml_file['tool']['poetry']['name'] = f"{NAMESPACE}.{library_name}"
        toml_file['tool']['poetry']['authors'] = ["Evgenia Kivotova"]
        toml_file['tool']['poetry']['packages'] = [{'include': NAMESPACE}]

        with open(f"libraries/{library_name}/pyproject.toml", "w") as f:
            toml.dump(toml_file, f)

        # Create diginavis namespace folder
        namespace_dir = Path(f"libraries/{library_name}/{NAMESPACE}")
        namespace_dir.mkdir(exist_ok=True, parents=True)

        library_dir = Path(f"libraries/{library_name}/{library_name}")

        # Move lib files to namespace dir
        shutil.move(str(library_dir), str(namespace_dir))

        print(f"Created libraries/{library_name}")
    else:
        print(
            f"An error occurred while creating libraries/{library_name}: {str(error)}")


if __name__ == "__main__":
    create_library(sys.argv[1])
