from pathlib import Path
import shutil
from typing import Dict

import ruamel.yaml
from termcolor import cprint

from kubetwo.config import Settings
from kubetwo.common import Common
from kubetwo.exception import *


class Ansible:

    def __init__(self,
        kubespray_dir_path: Path,
        inventory_path: Path,
        user_name: str,
        ssh_private_key_path: Path
    ):
        self.kubespray_dir_path = kubespray_dir_path
        self.inventory_path = inventory_path
        self.user_name = user_name
        self.ssh_private_key_path = ssh_private_key_path
    
    def run_kubespray(self):
        playbook_dir_path = self.kubespray_dir_path
        command = f"""
            ansible-playbook
            --inventory {str(self.inventory_path)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            --become
            --become-user=root
            cluster.yml
        """
        command = command.replace("\n", " ")
        try:
            cprint("Creating Kubernetes cluster...")
            Common.run_command(command, cwd=str(playbook_dir_path))
            cprint("Finished to create Kubernetes cluster.\n")
        except ProcessException as e:
            raise AnsibleKubesprayException(str(e))

    def run_setup(self):
        playbook_dir_path = Settings.ANSIBLE_TEMPLATE_DIR_PATH
        command = f"""
            ansible-playbook
            --inventory {str(self.inventory_path)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            {Settings.SETUP_PLAYBOOK_NAME}
        """
        command = command.replace("\n", " ")
        try:
            cprint("Setting up Kubernetes cluster...")
            Common.run_command(command, cwd=str(playbook_dir_path))
            cprint("Finished to set up Kubernetes cluster.\n")
        except ProcessException as e:
            raise AnsibleSetupException(str(e))

    def run_deploy_sample(self):
        playbook_dir_path = Settings.ANSIBLE_TEMPLATE_DIR_PATH
        command = f"""
            ansible-playbook
            --inventory {str(self.inventory_path)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            --extra-vars kubernetes_sample_dir={Settings.KUBERNETES_SAMPLE_DIR_PATH}
            {Settings.DEPLOY_SAMPLE_PLAYBOOK_NAME}
        """
        command = command.replace("\n", " ")
        try:
            cprint("Deploying sample in Kubernetes cluster...")
            Common.run_command(command, cwd=str(playbook_dir_path))
            cprint("Finish to deploy sample in Kubernetes cluster.\n")
        except ProcessException as e:
            raise AnsibleDeploySampleException(str(e))

    def run_fetch_admin_conf(
        self, 
        artifact_dir_path: Path,
        admin_conf_path: Path,
        first_control_plane: Dict
    ):
        playbook_dir_path = Settings.ANSIBLE_TEMPLATE_DIR_PATH
        command = f"""
            ansible-playbook
            --inventory {str(self.inventory_path)}
            --user {self.user_name}
            --private-key {str(self.ssh_private_key_path)}
            --extra-vars dest_path={str(artifact_dir_path)}
            {Settings.FETCH_ADMIN_CONF_NAME}
        """
        command = command.replace("\n", " ")
        try:
            cprint("Fetching admin.conf from control plane...")
            Common.run_command(command, cwd=str(playbook_dir_path))
            self._render_admin_conf(
                artifact_dir_path,
                admin_conf_path,
                first_control_plane,
            )
            cprint("Finished to fetch admin.conf from control plane.\n")
        except ProcessException as e:
            raise AnsibleFetchAdminConfException(str(e))

    def _render_admin_conf(
        self, 
        artifact_dir_path: Path,
        admin_conf_path: Path,
        first_control_plane: Dict
    ):
        yaml = ruamel.yaml.YAML()
        admin_conf_src_path = artifact_dir_path / f"{first_control_plane['name']}/admin.conf"
        with open(admin_conf_src_path, "r") as stream:
            admin_conf = yaml.load(stream)

        clusters = []
        for cluster in admin_conf["clusters"]:
            cluster_info = cluster["cluster"]
            cluster_info.pop("certificate-authority-data", None)
            cluster_info["insecure-skip-tls-verify"] = True
            cluster_info["server"] = f"https://{first_control_plane['public_ip']}:6443"
            cluster["cluster"] = cluster_info
            clusters.append(cluster)
        admin_conf["clusters"] = clusters

        with open(admin_conf_path, "w") as stream:
            yaml.dump(admin_conf, stream=stream)

        shutil.rmtree(str(artifact_dir_path / f"{first_control_plane['name']}"))
