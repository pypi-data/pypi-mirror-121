import json
import os
import shutil
from typing import Dict, List, Tuple

import ruamel.yaml
from termcolor import cprint
from jinja2 import Template

from kubetwo.model import CreateInput
from kubetwo.config import ArtifactSettings, Settings
from kubetwo.terraform import Terraform
from kubetwo.ansible import Ansible
from kubetwo.exception import *


class Create:

    def __init__(self, input: CreateInput):
        self.input = input
        self.artifact = ArtifactSettings(self.input.cluster_name)
        self.terraform = Terraform(self.artifact.RENDERED_TERRAFORM_DIR_PATH)
        self.yaml = ruamel.yaml.YAML()
    
    def run(self):
        self.terraform.show_plan()
        if not self.input.approve:
            self.check_tf_plan()
        self.terraform.apply()

        self.create_inventory_file()
        self.deploy_group_vars()
        default_user_name = self.get_default_user_name()
        ansible = Ansible(
            self.artifact.KUBESPRAY_DIR_PATH,
            self.artifact.RENDERED_INVENTORY_PATH,
            default_user_name,
            self.input.ssh_private_key
        )
        ansible.run_kubespray()
        ansible.run_setup()
        if self.input.deploy_sample:
            ansible.run_deploy_sample()
        ansible.run_fetch_admin_conf(
            artifact_dir_path = self.artifact.ARTIFACT_DIR_PATH,
            admin_conf_path = self.artifact.ADMIN_CONF_PATH,
            first_control_plane = self.get_node_info()[0][0]
        )
        self.create_node_info()

    def check_tf_plan(self):
        cprint(f"Resources will be created on AWS.", "yellow")
        cprint("Do you proceed?\n", "yellow")
        try:
            choice = input("Enter a value [y/N]: ")
            print()
            if choice.lower() in ['y', 'yes']:
                return
        except KeyboardInterrupt:
            print()

        raise CheckDeniedException("[ERROR] Suspended to create AWS resources.")
    
    def get_node_info(self) -> Tuple[List[Dict], List[Dict]]:
        """Load node information on AWS from terraform.tfstate.
           Each item format is {"name": str, "private_ip": str, "public_ip": str}."""
        if not os.path.exists(str(self.artifact.RENDERED_TFSTATE_PATH)):
            raise TerraformStateNotFound(f"""
                [ERROR] terraform.tfstate doesn't exist in {self.artifact.RENDERED_TERRAFORM_DIR_PATH}
                It's necessary to execute kubetwo init command first""")

        with open(self.artifact.RENDERED_TFSTATE_PATH, "r") as file:
            tfstate_data = json.load(file)

        control_plane_private_ip_list = tfstate_data["outputs"]["control_plane_private_ip"]["value"]
        control_plane_public_ip_list = tfstate_data["outputs"]["control_plane_public_ip"]["value"]
        worker_node_private_ip_list = tfstate_data["outputs"]["worker_node_private_ip"]["value"]
        worker_node_public_ip_list = tfstate_data["outputs"]["worker_node_public_ip"]["value"]

        control_plane_list = []
        for i, (private_ip, public_ip) in enumerate(zip(control_plane_private_ip_list, control_plane_public_ip_list)):
            name = f"control-plane{i}"
            control_plane_list.append({"name": name, "private_ip": private_ip, "public_ip": public_ip})

        worker_node_list = []
        for i, (private_ip, public_ip) in enumerate(zip(worker_node_private_ip_list, worker_node_public_ip_list)):
            name = f"worker-node{i}"
            worker_node_list.append({"name": name, "private_ip": private_ip, "public_ip": public_ip})

        return control_plane_list, worker_node_list
    
    def create_inventory_file(self):
        cprint("Rendering inventory file for Ansible...")
        control_plane_list, worker_node_list = self.get_node_info()

        if len(control_plane_list) % 2 == 0:
            etcd_count = len(control_plane_list) - 1
        else:
            etcd_count = len(control_plane_list)

        with open(Settings.INVENTORY_FILE_PATH, "r") as stream:
            inventory = self.yaml.load(stream)

        for node in control_plane_list + worker_node_list:
            inventory["all"]["hosts"][node["name"]] = {
                "ansible_ssh_host": node["public_ip"],
                "ip": node["private_ip"],
                "access_ip": node["private_ip"]
            }

        for control_plane in control_plane_list:
            inventory["all"]["children"]["kube_control_plane"]["hosts"][control_plane["name"]] = None

        for worker_node in worker_node_list:
            inventory["all"]["children"]["kube_node"]["hosts"][worker_node["name"]] = None

        for control_plane in control_plane_list[:etcd_count]:
            inventory["all"]["children"]["etcd"]["hosts"][control_plane["name"]] = None

        with open(self.artifact.RENDERED_INVENTORY_PATH, "w") as stream:
            self.yaml.dump(inventory, stream=stream)

        cprint(f"Completed to render inventory file ({self.artifact.RENDERED_INVENTORY_PATH}).\n")

    def deploy_group_vars(self):
        src = str(self.artifact.KUBESPRAY_GROUP_VARS_DIR_PATH)
        dest = str(self.artifact.RENDERED_KUBESPRAY_GROUP_VARS_DIR_PATH)
        shutil.copytree(src, dest)

        for path in self.artifact.RENDERED_ANSIBLE_DIR_PATH.glob('**/*.yml'):
            if path.name == "inventory.yml":
                continue
            with open(path, "r") as stream:
                group_vars = self.yaml.load(stream)
            
            if path.name == "k8s-cluster.yml":
                group_vars["cluster_name"] = self.input.cluster_name
            
            if path.name == "addons.yml":
                group_vars["helm_enabled"] = True

            with open(path, "w") as stream:
                self.yaml.dump(group_vars, stream=stream)

    def get_default_user_name(self) -> str:
        with open(self.artifact.RENDERED_TFSTATE_PATH, "r") as f:
            tfstate_data = json.load(f)

        ami_name = tfstate_data["outputs"]["ami_name"]["value"]
        ami_description = tfstate_data["outputs"]["ami_description"]["value"]
        ami_location = tfstate_data["outputs"]["ami_location"]["value"]

        with open(Settings.DISTRO_INFO_FILE_PATH, "r") as file:
            distro_list = json.load(file)

        default_user_name = "ec2-user"
        for distro in distro_list:
            if  (
                distro["ami_name_keyword"] in ami_name or
                distro["ami_description_keyword"] in ami_description or
                distro["ami_location_keyword"] in ami_location
                ):
                distro_name = distro["distro_name"]
                cprint(f"{distro_name} is detected.")
                default_user_name = distro["user_name"]
                break
                
        cprint(f"User \"{default_user_name}\" will be used for EC2 default user.\n")
        return default_user_name

    def create_node_info(self):
        control_plane_list, worker_node_list = self.get_node_info()
        user_name = self.get_default_user_name()
        params = {
            "control_plane_list": control_plane_list,
            "worker_node_list": worker_node_list,
            "user_name": user_name,
            "ssh_private_key": str(self.input.ssh_private_key),
            "deploy_sample": self.input.deploy_sample
        }
        with open(Settings.NODE_INFO_FILE_PATH, "r") as file:
            template = Template(file.read())

        node_info = template.render(params)

        with open(self.artifact.RENDERED_NODE_INFO_PATH, "w") as file:
            file.write(node_info)

        cprint(node_info, "cyan")
        