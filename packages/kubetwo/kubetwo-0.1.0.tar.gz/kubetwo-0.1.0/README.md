# kubetwo
kubetwo is a simple CLI tool to create a Kubernetes cluster on AWS EC2 with just one command.

kubetwo will interact with Terraform and Ansible (Kubespray) for provisioning.

# Requirements
To use kubetwo, following tools are necessary.

 - [Python (3.6 and newer)](https://www.python.org/downloads/)
 - [Terraform (1.0.0 and newer)](https://learn.hashicorp.com/tutorials/terraform/install-cli)

# Quick Start
## 1. Prerequisites
First, please install `kubetwo` package using pip or pip3 depending on your environment.

```sh
pip install kubetwo
```

For kubetwo to interact with Terraform and create AWS resources, it's necessary to set environment variables about AWS credentials.

```sh
export AWS_ACCESS_KEY_ID="your_anaccesskey"
export AWS_SECRET_ACCESS_KEY="your_asecretkey"
export AWS_DEFAULT_REGION="your_region"
```

Then, you need to create ssh key to access the EC2. If you've already used ssh key, you can use it. 

```sh
ssh-keygen -t rsa -b 4096 -f ~/.ssh/kubetwo_id_rsa
```

## 2.1 Spin up Kubernetes cluster (kubetwo apply)
By running the following `kubetwo apply` command, kubetwo will spin-up AWS EC2 with Terraform and set Kubernetes cluster on them with Ansible ([Kubespray v2.16.0](https://github.com/kubernetes-sigs/kubespray/tree/release-2.16)).

```sh
kubetwo apply \
--cluster_name="kubetwo-cluster" \
--ssh_public_key="~/.ssh/kubetwo_id_rsa.pub" \
--ssh_private_key="~/.ssh/kubetwo_id_rsa" \
--ami="ami-0df99b3a8349462c6" \
--control_plane=1 \
--worker_node=2 \
--open_ports="[6443, 30080]" \
--availability_zone="ap-northeast-1a" \
--deploy_sample
```

By using `--approve` option, you can automate approval. To know more details about parameters, you can refer to the following section.

Note: Port 6443 will be used for kube-apiserver and port 30080 for sample nginx service.

## 2.2 Spin up Kubernetes cluster (kubetwo init & create)
Instead of using `kubetwo apply` command, you can use `kubetwo init` and `kubetwo create` commands separately.

First, `kubetwo init` command will create the workspace in the current directory and render Terraform manifests and inventory file for Ansible on it. Also, it will download the Kubespray archive from GitHub.

```sh
kubetwo init \
--cluster_name="kubetwo-cluster" \
--ssh_public_key="~/.ssh/kubetwo_id_rsa.pub" \
--ami="ami-0df99b3a8349462c6" \
--control_plane=1 \
--worker_node=2 \
--open_ports="[6443, 30080]" \
--availability_zone="ap-northeast-1a"
```

Then, `kubetwo create` command will spin up EC2 and Kubernetes cluster.

```sh
kubetwo create \
--cluster_name="kubetwo-cluster" \
--ssh_private_key="~/.ssh/kubetwo_id_rsa" \
--deploy_sample
```

## 3. Access to the Kubernetes cluster
After the Kubernetes cluster is created, you can see admin.conf in the workspace.
Setting `KUBECONFIG` will allow you to access the Kubernetes cluster.

```sh
export KUBECONFIG=$(pwd)/kubetwo_cluster/admin.conf
```

Let's check the Kubernetes cluster from your local machine. (If you don't have `kubectl`, please install it)

```sh
kubectl get nodes
```

Also, you can check nginx sample if you add `--deploy_sample` option. URL will be shown when `kubetwo create` is completed.

```sh
curl http://xx.xx.xx.xx:30080
```

## 4. Clean up created resources
You can clean up created resources with `kubetwo delete` command.
It will also delete workspace for kubetwo on your machine.

```sh
kubetwo delete \
--cluster_name="kubetwo-cluster"
```

# Parameters

## kubetwo apply

| Name | Type | Default | Description |
| :---: | :---: | :---: | :--- |
| cluster_name | string | - | Kubernetes cluster name |
| ssh_public_key | string | - | Path of public key for SSH |
| ssh_private_key | string | - | Path of private key for SSH |
| ami | string | ami-0c3fd0f5d33134a76 | Amazon Machine Image of EC2 instance |
| instance_type | string | t3.medium | Instance type of EC2 instance |
| availability_zone | string | us-west-1a | Availability zone of EC2 instance |
| control_plane | int | 1 | Number of control planes |
| worker_node | int | 1 | Number of worker nodes |
| open_ports | array[string] | [6443, 30080] | Ports to open for global (If you use -1, all ports will be open) |
| deploy_sample | boolean | false | If true, kubetwo will deploy nginx sample in cluster |
| approve | boolean | false | If true, kubetwo won't prompt you to approve for execution |

## kubetwo init

| Name | Type | Default | Description |
| :---: | :---: | :---: | :--- |
| cluster_name | string | - | Kubernetes cluster name |
| ssh_public_key | string | - | Path of public key for SSH |
| ami | string | ami-0c3fd0f5d33134a76 | Amazon Machine Image of EC2 instance |
| instance_type | string | t3.medium | Instance type of EC2 instance |
| availability_zone | string | us-west-1a | Availability zone of EC2 instance |
| control_plane | int | 1 | Number of control planes |
| worker_node | int | 1 | Number of worker nodes |
| open_ports | array[string] | [6443, 30080] | Ports to open for global (If you use -1, all ports will be open) |
| approve | boolean | false | If true, kubetwo won't prompt you to approve for execution |

## kubetwo create

| Name | Type | Default | Description |
| :---: | :---: | :---: | :--- |
| cluster_name | string | - | Kubernetes cluster name |
| ssh_private_key | string | - | Path of private key for SSH |
| deploy_sample | boolean | false | If true, kubetwo will deploy nginx sample in cluster |
| approve | boolean | false | If true, kubetwo won't prompt you to approve for execution |

## kubetwo delete

| Name | Type | Default | Description |
| :---: | :---: | :---: | :--- |
| cluster_name | string | - | Kubernetes cluster name |
| approve | boolean | false | If true, kubetwo won't prompt you to approve for execution |
