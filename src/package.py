# Packaging script entrypoint
import os
import shutil
import zipfile
import zlib
import sys
from argparse import ArgumentParser
import logging

from ksp_deploy.logging import set_logging
from ksp_deploy.helpers import clean_path, get_build_data, get_version_file_info, get_version
from ksp_deploy.packaging import collect_dependencies, build_extras, build_nodep_release, build_full_release
from ksp_deploy.config import BUILD_PATH, DEPLOY_PATH, TEMP_PATH, BUILD_DATA_NAME


def package(core_release, extras_release, complete_release, mod_data_file):
    """
    Compiles and packages the set of release packages according to information from
    the .version file and the .build_data.yml file
    Inputs:
        core_release (bool): whether to build a no-dependency release zip
        extras_release (bool): whether to build a release zip for each extra file
        complete_release (bool): whether to build a yes dependency release zip
        mod_data_file (str): path to mod data yaml (defaults to the one in ksp_deploy.config.py)
    """
    # Collect build information
    if mod_data_file == "":
        mod_data_file = BUILD_DATA_NAME
    build_data = get_build_data(mod_data_file)
    version_data = get_version_file_info(os.path.join(os.path.dirname(mod_data_file), "GameData", build_data['mod-name']), build_data['mod-name'])

    logger.info(f"Building {build_data['mod-name']} version {get_version(version_data)}\n=================")

    build_mod_path = os.path.join(BUILD_PATH, build_data['mod-name'])
    deploy_mod_path = os.path.join(DEPLOY_PATH, build_data['mod-name'])
    # Clean/recreate the build, deploy and temp paths
    clean_path(os.path.join(build_mod_path))
    clean_path(os.path.join(deploy_mod_path))
    clean_path(os.path.join(TEMP_PATH))

    # Copy main mod content
    logger.info(f"Compiling core mod content")


    for gamedata_item in build_data['package']['included-gamedata']:
        shutil.copytree(os.path.join(os.path.dirname(mod_data_file), "GameData"), os.path.join(build_mod_path, "GameData", gamedata_item))

    for support_item in build_data['package']['included-support']:
        shutil.copy(os.path.join(os.path.dirname(mod_data_file), support_item), os.path.join(build_mod_path, support_item))

    if core_release:
        logger.info(f"Packaging BASIC release package")
        build_nodep_release(version_data, build_data, build_mod_path, deploy_mod_path)

    if os.path.exists("Extras"):
      logger.info(f"Packaging EXTRAS release packages")
      build_extras(version_data, extras_release, build_mod_path, deploy_mod_path)

    logger.info(f"Packaging complete release package")
    logger.info(f"Collecting dependencies")
    collect_dependencies(build_data, build_mod_path)

    if complete_release:
        logger.info(f"Packaging COMPLETE release package")
        build_full_release(version_data, build_data, build_mod_path, deploy_mod_path)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-c", "--complete",
                        action="store_true",  default=True,
                        help="write complete package")
    parser.add_argument("-e", "--extras",
                        action="store_true", default=False,
                        help="write extras package")
    parser.add_argument("-b", "--basic",
                        action="store_true", default=False,
                        help="write basic no dependency package")
    parser.add_argument("-f", "--file", default="",
                        help="custom package data file path")

    args = parser.parse_args()

    logger = set_logging("packager")

    package(args.basic, args.extras, args.complete, args.file)
