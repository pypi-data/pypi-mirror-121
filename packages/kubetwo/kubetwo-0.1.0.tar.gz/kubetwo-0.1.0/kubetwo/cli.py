import json
from pathlib import Path
import sys
from typing import List

import fire
from pydantic import ValidationError
from termcolor import cprint

from kubetwo.init import Init
from kubetwo.create import Create
from kubetwo.delete import Delete
from kubetwo.model import CreateInput, DeleteInput, InitInput
from kubetwo.config import Settings
from kubetwo.exception import *
from kubetwo.validator import ValidationFormatter


def main():
    fire.Fire(CLI)


class CLI:

    @classmethod
    def init(
        cls,
        cluster_name: str,
        ssh_public_key: str,
        ami: str = Settings.DEFAULT_AMI,
        instance_type: str = Settings.DEFAULT_INSTANCE_TYPE,
        availability_zone: str = Settings.DEFAULT_AVAILABILITY_ZONE,
        control_plane: int = Settings.DEFAULT_CONTROL_PLANE_NUM,
        worker_node: int = Settings.DEFAULT_WORKER_NODE_NUM,
        open_ports: List[int] = Settings.DEFAULT_OPEN_PORTS,
        approve: bool = False,
        create_mode: bool = False
    ):
        try:
            init_input = InitInput(
                cluster_name = cluster_name,
                ssh_public_key = ssh_public_key,
                ami = ami,
                instance_type = instance_type,
                availability_zone = availability_zone,
                control_plane = control_plane,
                worker_node = worker_node,
                open_ports = open_ports,
                approve = approve,
                create_mode = create_mode,
            )
            init = Init(init_input)
            init.run()
        except ValidationError as e:
            cprint("[ERROR] Input value is not correct.", "red")
            validation_result = json.loads(e.json())
            cprint(ValidationFormatter.format(validation_result), "red")
            sys.exit(1)
        except CheckDeniedException as e:
            cprint(e, "red")
            sys.exit(1)
        except TerraformException as e:
            cprint(e, "red")
            cprint("[ERROR] Terraform execution failed.", "red")
            sys.exit(1)

    @classmethod
    def create(
        cls,
        cluster_name: str,
        ssh_private_key: str,
        deploy_sample: bool = False,
        approve: bool = False,
        create_mode: bool = False
    ):
        try:
            create_input = CreateInput(
                cluster_name = cluster_name,
                ssh_private_key = Path(ssh_private_key).expanduser(),
                deploy_sample = deploy_sample,
                approve = approve,
                create_mode = create_mode
            )
            create = Create(create_input)
            create.run()
        except ValidationError as e:
            cprint("[ERROR] Input value is not correct.", "red")
            validation_result = json.loads(e.json())
            cprint(ValidationFormatter.format(validation_result), "red")
            sys.exit(1)
        except (CheckDeniedException, TerraformStateNotFound) as e:
            cprint(e, "red")
            sys.exit(1)
        except TerraformException as e:
            cprint(e, "red")
            cprint("[ERROR] Terraform execution failed.", "red")
            sys.exit(1)
        except AnsibleException as e:
            cprint(e, "red")
            cprint("[ERROR] Provisioning by Ansible failed.", "red")
            sys.exit(1)

    @classmethod
    def apply(
        cls,
        cluster_name: str,
        ssh_public_key: str,
        ssh_private_key: str,
        ami: str=Settings.DEFAULT_AMI,
        instance_type: str=Settings.DEFAULT_INSTANCE_TYPE,
        availability_zone: str=Settings.DEFAULT_AVAILABILITY_ZONE,
        control_plane: int=Settings.DEFAULT_CONTROL_PLANE_NUM,
        worker_node: int=Settings.DEFAULT_WORKER_NODE_NUM,
        open_ports: List[int] = Settings.DEFAULT_OPEN_PORTS,
        deploy_sample: bool = False,
        approve: bool = False,
    ):
        cls.init(
            cluster_name = cluster_name,
            ssh_public_key = ssh_public_key,
            ami = ami,
            instance_type = instance_type,
            availability_zone = availability_zone,
            control_plane = control_plane,
            worker_node = worker_node,
            open_ports = open_ports,
            approve = approve,
            create_mode = True,
        )
        cls.create(
            cluster_name = cluster_name,
            ssh_private_key = Path(ssh_private_key).expanduser(),
            deploy_sample = deploy_sample,
            approve = approve,
            create_mode = True
        )

    @classmethod
    def delete(
        cls,
        cluster_name: str,
        approve: bool = False
    ):
        try:
            delete_input = DeleteInput(
                cluster_name = cluster_name,
                approve = approve
            )
            delete = Delete(delete_input)
            delete.run()
        except ValidationError as e:
            cprint("[ERROR] Input value is not correct.", "red")
            validation_result = json.loads(e.json())
            cprint(ValidationFormatter.format(validation_result), "red")
            sys.exit(1)
        except CheckDeniedException as e:
            cprint(e, "red")
            sys.exit(1)
        except TerraformException as e:
            cprint(e, "red")
            cprint("[ERROR] Terraform execution failed.", "red")
            sys.exit(1)
