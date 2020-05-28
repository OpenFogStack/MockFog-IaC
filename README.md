### *This repository is now read-only, for a new and actively maintained version of MockFog see [MockFog2](https://github.com/MoeweX/MockFog2)*.

# MockFog Infrastructure as Code

This project is part of MockFog which includes the following subprojects:
* [MockFog-Meta](https://github.com/OpenFogStack/MockFog-Meta) Meta repository with a presentation and a demo video
* [MockFog-IaC](https://github.com/OpenFogStack/MockFog-IaC) MockFog Infrastructure as Code artifacts
* [MockFog-NodeManager](https://github.com/OpenFogStack/MockFog-NodeManager) MockFog Node Manager
* [MockFog-Agent](https://github.com/OpenFogStack/MockFog-Agent) MockFog Agent
* [MockFogLight](https://github.com/OpenFogStack/MockFogLight) A lightweight version of MockFog without a visual interface

Fog computing is an emerging computing paradigm that uses processing and storage capabilities located at the edge, in the cloud, and possibly in between. Testing fog applications, however, is hard since runtime infrastructures will typically be in use or may not exist, yet.
MockFog is a tool that can be used to emulate such infrastructures in the cloud. Developers can freely design emulated fog infrastructures, configure their performance characteristics, and inject failures at runtime to evaluate their application in various deployments and failure scenarios.

If you use this software in a publication, please cite it as:

### Text
Jonathan Hasenburg, Martin Grambow, Elias Grünewald, Sascha Huk, David Bermbach. **MockFog: Emulating Fog Computing Infrastructure in the Cloud**. In: Proceedings of the First IEEE International Conference on Fog Computing 2019 (ICFC 2019). IEEE 2019.

### BibTeX
```
@inproceedings{hasenburg_mockfog:_2019,
	title = {{MockFog}: {Emulating} {Fog} {Computing} {Infrastructure} in the {Cloud}},
	booktitle = {Proceedings of the First {IEEE} {International} {Conference} on {Fog} {Computing} 2019 (ICFC 2019)},
	author = {Hasenburg, Jonathan and Grambow, Martin and Grunewald, Elias and Huk, Sascha and Bermbach, David},
	year = {2019},
	publisher = {IEEE}
}
```

A full list of our [publications](https://www.mcc.tu-berlin.de/menue/forschung/publikationen/parameter/en/) and [prototypes](https://www.mcc.tu-berlin.de/menue/forschung/prototypes/parameter/en/) is available on our group website.

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

The repositories and branches that are pulled during the execution of a play are defined at `repositories.yml.

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
