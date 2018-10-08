# MockFog Infrastructure as Code

## Requirements

- OS: Tested on Ubuntu 16.04
- virtualenv
- pip
- python 2.7

## Installation

- Create a `nm_aws.yml` file based on the `nm_aws_template.yml`, feel free to add you aws security credentials as this file is irgnored by git.
- Execute `install_nodemanager.sh`
- Enter the ip of the created nodemanger in your browser

## Plays

Two plays exist, one for the setup/tear down of the nodemanager and one for the setup/tear down of the agents.

The nodemanager play is started by either executing `./install_nodemanager.sh` or by running the `nm_aws.yml` playbook.

The agent play is started by running the `aws.yml` playbook.

The repositories and branches that are pulled during the execution of a play are defined at `repositories.yml` (also git ignored), if it does not exist, `repositories_default.yml` will be used.

## Configuration

### Openstack

1. Download OpenRC file with Cloud credentials



You can find it in the OpenStack Dashboard at Compute - Access and Security - API Access



2. Set OpenStack Environment Variables
`source MockFog-openrc.sh`

3. Create SSH Key if not already availabe
`ssh-keygen -t rsa -b 4096`

4. Add SSH Public Key to OpenStack Cloud
   via OpenStack Dashboard or CLI

5. Add name of OpenStack SSH Key to example vars file
i.e. `os_ssh_key_name: <ssh_key_name>`

## Bootstrap testbed

### OpenStack

-  `ansible-playbook openstack.yml --tags "bootstrap"`
   to deploy MockFog testbed in OpenStack



## Destroy testbed

### OpenStack

-  `ansible-playbook openstack.yml --tags "destroy"`
   to destroy MockFog testbed in OpenStack
