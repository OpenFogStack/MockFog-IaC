#!/bin/bash


install_ansible()
{
    if [ ! -d .venv ]; then
        virtualenv .venv
        source .venv/bin/activate
        pip3 install -r requirements.txt
    else
        echo ".venv already exists"
        source .venv/bin/activate
    fi
}

read -r -p "Which cloud are you using?
  1. OpenStack
  2. AWS EC2
: " reply

install_ansible

case "$reply" in
  1) ansible-playbook nm_openstack.yml --tags bootstrap;;
  2) ansible-playbook nm_aws.yml --tags bootstrap;;
  *) echo; echo "Invalid provider selected."; exit 1;;
esac
