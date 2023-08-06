import os
from pathlib import Path
import subprocess
import sys

from termcolor import cprint

from kubetwo.common import Common
from kubetwo.exception import *


class Terraform:

    def __init__(self, tf_dir_path: Path):
        self.tf_dir_path = tf_dir_path

    def initialize(self):
        command = "terraform init"
        try:
            cprint(f"Initializing Terraform...")
            Common.run_command(command, cwd=str(self.tf_dir_path), stdout=False)
            cprint(f"Terraform successfully initialized.\n")
        except ProcessException as e:
            raise TerraformInitException(str(e))

    def show_plan(self, destroy_mode=False):
        command = "terraform plan -compact-warnings"
        try:
            cprint(f"Creating Terraform plan...")
            if destroy_mode:
                command = f"{command} -destroy"
            Common.run_command(command, cwd=str(self.tf_dir_path))
        except ProcessException as e:
            raise TerraformPlanException(str(e))

    def apply(self):
        command = "terraform apply -auto-approve"
        try:
            cprint(f"Creating resources on AWS...")
            Common.run_command(command, cwd=str(self.tf_dir_path), stdout=False)
            cprint(f"Completed to create resources on AWS.\n")
        except ProcessException as e:
            raise TerraformApplyException(str(e))

    def destroy(self):
        command = "terraform destroy -auto-approve"
        try:
            cprint(f"Deleting resources on AWS...")
            Common.run_command(command, cwd=str(self.tf_dir_path), stdout=False)
            cprint(f"Completed to delete resources on AWS.\n")
        except ProcessException as e:
            raise TerraformDestroyException(str(e))
    