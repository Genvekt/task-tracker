import json
import sys
import toml
from pathlib import Path

import requests


def is_service_exists(service_name: str) -> bool:
    # Check that service exists in case it was deleted
    service_folder = Path(f"services/{service_name}")
    return service_folder.exists()


def is_library_exists(library_name: str) -> bool:
    # Check that library exists in case it was deleted
    library_folder = Path(f"libraries/{library_name}")
    return library_folder.exists()


def get_changed_services():
    if sys.argv[1] == "master":
        r = requests.get(
            url=f"https://api.github.com/repos/Genvekt/task-tracker/commits/{sys.argv[3]}",
            headers={"authorization": f"Bearer {sys.argv[2]}"}
        )
    else:
        r = requests.get(
            url=f"https://api.github.com/repos/Genvekt/task-tracker/compare/master...{sys.argv[1]}",
            headers={"authorization": f"Bearer {sys.argv[2]}"}
        )
    output = {"service_name": [], "library_name": []}
    if r.status_code == 200:
        files = r.json()['files']
        # Identify changed libraries and services
        changed_services = set()
        changed_libraries = set()
        for file in files:
            elements = file['filename'].split("/")
            # Directly changed libraries
            if elements[0] == 'libraries' and is_library_exists(elements[1]):
                changed_libraries.add(elements[1])
            # Directly changed services
            elif elements[0] == 'services' and is_service_exists(elements[1]):
                changed_services.add(elements[1])

        # Services with changed libraries
        all_services = Path("services").glob("*/")
        for service_dir in all_services:
            toml_file_path = service_dir / "pyproject.toml"
            if toml_file_path.exists():
                poetry_conf = toml.load(toml_file_path)
                dependencies = poetry_conf['tool']['poetry']['dependencies']
                for dependency, dep_params in dependencies.items():
                    if "path" in dep_params and \
                            dependency.startswith("library."):
                        # Get lib name
                        dependency_name = dependency.split(".")[1]
                        if dependency_name in changed_libraries:
                            changed_services.add(service_dir.name)

        for service in changed_services:
            output["service_name"].append(service)

        for library in changed_libraries:
            output["library_name"].append(library)

    print(json.dumps(output))


if __name__ == "__main__":
    get_changed_services()
