import os
from pathlib import Path
import shutil
import tarfile
from typing  import Dict, List

import requests
from termcolor import cprint
from jinja2 import Template

from kubetwo.model import InitInput
from kubetwo.config import ArtifactSettings, Settings
from kubetwo.terraform import Terraform
from kubetwo.exception import *


class Init:

    def __init__(self, input: InitInput):
        self.input = input
        self.artifact = ArtifactSettings(input.cluster_name)
        self.terraform = Terraform(self.artifact.RENDERED_TERRAFORM_DIR_PATH)

    def run(self):
        cprint("Initialize Terraform and Ansible for provisioning.\n")
        params = {
            "cluster_name": self.input.cluster_name.replace('_', '-'),
            "control_plane_count": self.input.control_plane,
            "worker_node_count": self.input.worker_node,
            "ami": self.input.ami,
            "instance_type": self.input.instance_type,
            "availability_zone": self.input.availability_zone,
            "ssh_public_key_name": str(self.input.ssh_public_key.name),
            "ssh_public_key": str(self.input.ssh_public_key),
            "open_ports": self.input.open_ports
        }

        if not self.input.approve:
            self.check_clean_artifact_dir()
        self.clean_artifact_dir()
        self.download_kubespray()
        self.render_and_save_files(params)
        self.terraform.initialize()

        if not self.input.create_mode:
            cprint(f"Next, run the following command:", "cyan")
            cprint(f"kubetwo apply --cluster_name=\"{self.input.cluster_name}\" --ssh_private_key=\"YOUR_PRIVATE_KEY_PATH\"\n", "cyan")

    def check_clean_artifact_dir(self):
        if not os.path.isdir(str(self.artifact.ARTIFACT_DIR_PATH)):
            return

        cprint(f"Directory {str(self.artifact.ARTIFACT_DIR_PATH)} already exists.", "yellow")
        cprint("Do you use this directory to setup kubetwo?\n", "yellow")
        try:
            choice = input("Enter a value [y/N]: ")
            print()
            if choice.lower() in ['y', 'yes']:
                return
        except KeyboardInterrupt:
            print()
        
        raise CheckDeniedException("[ERROR] Please use another cluster_name.")

    def clean_artifact_dir(self):
        if not os.path.isdir(str(self.artifact.ARTIFACT_DIR_PATH)):
            os.makedirs(str(self.artifact.ARTIFACT_DIR_PATH))

        if os.path.isdir(str(self.artifact.RENDERED_ANSIBLE_DIR_PATH)):
            shutil.rmtree(str(self.artifact.RENDERED_ANSIBLE_DIR_PATH))
        os.makedirs(str(self.artifact.RENDERED_ANSIBLE_DIR_PATH))
            
        if not os.path.isdir(str(self.artifact.RENDERED_TERRAFORM_DIR_PATH)):
            os.makedirs(str(self.artifact.RENDERED_TERRAFORM_DIR_PATH))
            
        for tf_file_path in self.artifact.RENDERED_TERRAFORM_DIR_PATH.glob("**/*.tf"):
            os.remove(str(tf_file_path))
        
        if os.path.isfile(str(self.artifact.RENDERED_INVENTORY_PATH)):
            os.remove(str(self.artifact.RENDERED_INVENTORY_PATH))

    def download_kubespray(self):
        cprint("Downloading Kubespray...")
        if os.path.isdir(self.artifact.KUBESPRAY_DIR_PATH):
            return
        
        kubespray_content = requests.get(Settings.KUBESPRAY_ARCHIVE_URL).content

        with open(self.artifact.KUBESPRAY_ARCHIVE_PATH ,mode='wb') as file:
            file.write(kubespray_content)

        with tarfile.open(self.artifact.KUBESPRAY_ARCHIVE_PATH) as tar:
            tar.extractall(self.artifact.ARTIFACT_DIR_PATH)

        os.remove(str(self.artifact.KUBESPRAY_ARCHIVE_PATH))
        cprint("Finished to download Kubespray.\n")

    def get_tf_template_paths(self) -> List[Path]:
        return list(Settings.TERRAFORM_TEMPLATE_DIR_PATH.glob("**/*.tf.j2"))
        
    def render_and_save_files(self, params: Dict):
        cprint("Rendering Terraform manifests...")
        tf_template_paths = self.get_tf_template_paths()
        for path in tf_template_paths:
            with open(path, "r") as file:
                template = Template(file.read())

            rendered_content = template.render(params)
            rendered_file_name = str(path.relative_to(Settings.TERRAFORM_TEMPLATE_DIR_PATH)).replace('.j2', '')
            rendered_file_path = self.artifact.RENDERED_TERRAFORM_DIR_PATH / rendered_file_name

            if rendered_file_path.parent != self.artifact.RENDERED_TERRAFORM_DIR_PATH:
                os.makedirs(str(rendered_file_path.parent), exist_ok=True)

            with open(rendered_file_path, "w") as f:
                f.write(rendered_content)

        cprint(f"Terraform manifests have been successfully rendered in {str(self.artifact.RENDERED_TERRAFORM_DIR_PATH)}\n")
