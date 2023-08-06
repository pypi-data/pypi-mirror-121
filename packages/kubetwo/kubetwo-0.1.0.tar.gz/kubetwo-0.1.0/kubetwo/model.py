from pathlib import Path
from typing import List

from pydantic import BaseModel, conint, constr, root_validator, validator

from kubetwo.config import Settings
from kubetwo.validator import Validator


class InitInput(BaseModel):

    cluster_name: constr(max_length=64)
    ssh_public_key: Path
    ami: str = Settings.DEFAULT_AMI
    instance_type: str = Settings.DEFAULT_INSTANCE_TYPE
    availability_zone: str = Settings.DEFAULT_AVAILABILITY_ZONE
    control_plane: conint(ge=1) = Settings.DEFAULT_CONTROL_PLANE_NUM
    worker_node: conint(ge=1) = Settings.DEFAULT_WORKER_NODE_NUM
    open_ports: List[conint(ge=-1, le=65535)] = Settings.DEFAULT_OPEN_PORTS
    approve: bool = False
    create_mode: bool = False

    _check_credentials = root_validator(allow_reuse=True)(Validator.check_credentials)

    _ssh_public_key_str_to_path = \
        validator("ssh_public_key", pre=True, allow_reuse=True)(Validator.str_to_path)

    _ssh_public_key_exists = \
        validator("ssh_public_key", allow_reuse=True)(Validator.file_exists)

class CreateInput(BaseModel):

    cluster_name: constr(max_length=64)
    ssh_private_key: Path
    deploy_sample: bool = False
    approve: bool = False
    create_mode: bool = False


    _check_credentials = root_validator(allow_reuse=True)(Validator.check_credentials)

    _check_artifact_dir_exists = root_validator(allow_reuse=True)(Validator.check_artifact_dir_exists)
    
    _check_artifact_dir_exists = root_validator(allow_reuse=True)(Validator.check_artifact_dir_exists)

    _ssh_private_key_str_to_path = \
        validator("ssh_private_key", pre=True, allow_reuse=True)(Validator.str_to_path)

    _ssh_private_key_exists = \
        validator("ssh_private_key", allow_reuse=True)(Validator.file_exists)


class DeleteInput(BaseModel):

    cluster_name: constr(max_length=64)
    approve: bool = False

    _check_credentials = root_validator(allow_reuse=True)(Validator.check_credentials)

    _check_artifact_dir_exists = root_validator(allow_reuse=True)(Validator.check_artifact_dir_exists)

    _check_tfstate_exists = root_validator(allow_reuse=True)(Validator.check_tfstate_exists)

    _check_artifact_dir_exists = root_validator(allow_reuse=True)(Validator.check_artifact_dir_exists)
