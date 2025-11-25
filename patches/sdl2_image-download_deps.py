#!/usr/bin/env python3
import os
import sys
from droidbuilder.utils.command_executor import run_shell_command
from droidbuilder.cli_logger import logger

# The script is executed with cwd set to package_source_path by patch_resolver.py
package_source_path = os.getcwd()

download_script_path = os.path.join(package_source_path, "external", "download.sh")

logger.info(f"  - Making {download_script_path} executable.")
chmod_result = run_shell_command(
    command=["chmod", "+x", download_script_path],
    description=f"Making {os.path.basename(download_script_path)} executable",
    cwd=package_source_path
)

if chmod_result['returncode'] != 0:
    logger.error(f"  - Failed to make {os.path.basename(download_script_path)} executable. Aborting patch.")
    sys.exit(1)

logger.info(f"  - Executing {download_script_path}.")
run_result = run_shell_command(
    command=[download_script_path],
    description=f"Running {os.path.basename(download_script_path)}",
    cwd=package_source_path
)

if run_result['returncode'] != 0:
    logger.error(f"  - {os.path.basename(download_script_path)} failed (Exit Code: {run_result['returncode']}). Aborting patch.")
    if run_result.get('stdout'):
        logger.error(f"    Stdout:\n{run_result['stdout']}")
    if run_result.get('stderr'):
        logger.error(f"    Stderr:\n{run_result['stderr']}")
    sys.exit(1)

logger.success(f"  - Successfully executed {os.path.basename(download_script_path)}.")