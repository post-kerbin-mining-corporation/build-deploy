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
from ksp_deploy.config import BUILD_PATH, DEPLOY_PATH, TEMP_PATH, TEMP_CHANGELOG_NAME, TEMP_VERSION_NAME


def package(core_release, extras_release, complete_release):
    """
    Compiles and packages the set of release packages according to information from
    the .version file and the .build_data.yml file
    """
    # Collect build information
    build_data = get_build_data()
    version_data = get_version_file_info(build_data["mod-name"])

    logger.info(f"Building {build_data['mod-name']} version {get_version(version_data)}\n=================")

    # Clean/recreate the build, deploy and temp paths
    clean_path(os.path.join(BUILD_PATH))
    clean_path(os.path.join(DEPLOY_PATH))
    clean_path(os.path.join(TEMP_PATH))

    # Copy main mod content
    logger.info(f"Compiling core mod content")
    shutil.copytree(os.path.join("GameData", build_data["mod-name"]), os.path.join(BUILD_PATH, "GameData", build_data["mod-name"]))
    shutil.copy("changelog.txt", os.path.join(BUILD_PATH, "changelog.txt"))
    shutil.copy("readme.txt", os.path.join(BUILD_PATH,  "readme.txt"))

    if core_release:
        logger.info(f"Packaging BASIC release package")
        build_nodep_release(version_data, build_data['mod-name'])

    if os.path.exists("Extras"):
      logger.info(f"Packaging EXTRAS release packages")
      build_extras(version_data, extras_release)

    logger.info(f"Packaging complete release package")
    logger.info(f"Collecting dependencies")
    collect_dependencies(build_data)

    if complete_release:
        logger.info(f"Packaging COMPLETE release package")
        build_full_release(version_data, build_data['mod-name'])

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

    args = parser.parse_args()

    logger = set_logging("packager")

    package(args.basic, args.extras, args.complete)
