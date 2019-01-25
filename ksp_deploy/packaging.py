import os
import shutil
import logging

from ksp_deploy.helpers import ensure_path, clean_path
from ksp_deploy.config import DEPLOY_PATH, BUILD_PATH, TEMP_PATH
from ksp_deploy.dependencies import download_dependency

logger = logging.getLogger('packager.packaging')


def build_nodep_release(version_data, mod_name):
    """
    Builds the release zip with no included dependencies

    Inputs:
        version_data (dict): Contents of the .version file
        mod_name (str): name of the mod
    """
    build_path = os.path.join(DEPLOY_PATH,
        f"{mod_name}_Core_" + "{MAJOR}_{MINOR}_{PATCH}".format(**version_data["VERSION"]))
    shutil.make_archive(build_path, 'zip', os.path.join(BUILD_PATH))
    logger.info(f"Packaged {build_path}")

def build_full_release(version_data, mod_name):
    """
    Builds the release zip with a full set of required dependencies

    Inputs:
        version_data (dict): Contents of the .version file
        mod_name (str): name of the mod
    """
    build_path = os.path.join(DEPLOY_PATH,
        f"{mod_name}_" + "{MAJOR}_{MINOR}_{PATCH}".format(**version_data["VERSION"]))
    shutil.make_archive(build_path, 'zip', os.path.join(BUILD_PATH))
    logger.info(f"Packaged {build_path}")

def build_extras(version_data, build_packages=False):
    """
    Compiles and optionally builds packages for all Extras in the mod

    Inputs:
        version_data (dict): Contents of the .version file
        build_packages (bool): whether to create an individual zipfile for each package
    """
    for root, dirs, files in os.walk("Extras"):
        for name in dirs:
            build_extra(name, version_data, build_packages)

def build_extra(name, version_data, build_package):
    """
    Compiles and optionally builds a single Extras package

    Inputs:
        name (str): name of the extra
        version_data (dict): Contents of the .version file
        build_package (bool): whether to create an individual zipfile for the package
    """
    extra_path = os.path.join(DEPLOY_PATH, f"{name}" + "{MAJOR}_{MINOR}_{PATCH}".format(**version_data["VERSION"]))
    logger.info(f"Packaging Extra {name}")
    ensure_path(os.path.join(BUILD_PATH,"Extras"))
    shutil.copytree(os.path.join("Extras", name), os.path.join(BUILD_PATH,"Extras", name))

    if build_package:
        logger.info(f"Packaging {name}")
        shutil.make_archive(extra_path, "zip", os.path.join(BUILD_PATH, "Extras", name))
        logger.info(f"Packaged {extra_path}")

def collect_dependencies(mod_data):
    """
    Finds and downloads all the mod's dependencies

    Inputs:
        mod_data (dict): the mod data dictionary
    """
    dep_data = mod_data["dependencies"]
    clean_path(TEMP_PATH)
    for name, info in dep_data.items():
        download_dependency(name, info, TEMP_PATH, BUILD_PATH)
    cleanup(mod_data["package"]["included-support-files"])

def cleanup(kept_files):
    """
    Cleans up the trailing files in the main directory for packaging by excluding all expect the
    specified items in the mod's .mod_data.yml
    """
    onlyfiles = [f for f in os.listdir(BUILD_PATH) if os.path.isfile(os.path.join(BUILD_PATH, f))]
    for f in onlyfiles:
        if f not in kept_files:
            os.remove(os.path.join(BUILD_PATH,f))
