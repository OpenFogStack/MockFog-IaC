# MockFog Infrastructure as Code

## Requirements

- OS: Tested on Ubuntu 16.04
- virtualenv
- pip
- python 2.7

## Installation

-  `git clone git@github.com:OpenFogStack/MockFog-IaC.git`

-  `virtualenv .venv`

-  `source .venv/bin/activate`

-  `pip install -r requirements.txt`

  

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
   
