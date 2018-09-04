#!/usr/bin/python

from ansible.module_utils.basic import *
import json
import requests
import boto3

def parse_openstack(data):
    has_changed = False
    nodes = data['nodes']
    nm_url = data['nodemanager']
    node_ips = {}
    for node in nodes:
        tmp = {}
        for net in node['server']['addresses']:
            tmp[net] = {
                "addr": node['server']['addresses'][net][0]['addr'],
                "mac": node['server']['addresses'][net][0]['OS-EXT-IPS-MAC:mac_addr']
            }
        
        tmp['public_addr'] =  node['openstack']['public_v4']
        node_ips[node['item']['name']] = tmp
	
    with open('/opt/MFog-IaC/created/agentIPs.json', 'w') as f:
        json.dump(node_ips, f)
	
    got_error, has_changed, result = send_data(node_ips, nm_url)
    return (got_error, has_changed, result, node_ips)
    

def ec2_get_subnet_name(aws_access_key, aws_secret_key, aws_region, subnet_id):
    ec2 = boto3.resource(
        'ec2',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
        )
    subnet = ec2.Subnet(subnet_id)
    for tags in subnet.tags:
        if tags["Key"] == 'Name':
            subnet_name = tags["Value"]
    return subnet_name


def parse_aws(data):
    aws_access_key = data['aws_access_key']
    aws_secret_key = data['aws_secret_key']
    aws_region = data['region']
    aws_region = data["region"]
    has_changed = False,
    nodes = data['nodes']
    nm_url = data['nodemanager']
    node_ips = {}
    # probably not the most efficient way
    for node in nodes:
        tmp = {}
        for net in node['network_interfaces']:
            subnet_name = ec2_get_subnet_name(aws_access_key,
                                              aws_secret_key,
                                              aws_region,
                                              net['subnet_id']
                                              )
            tmp[subnet_name] = { 
                "addr": net["private_ip_address"],
                "mac": net["mac_address"]
            }
        tmp['public_addr'] = node["public_ip_address"]
        node_ips[node['tags']['Name']] = tmp

    got_error, has_changed, result = send_data(node_ips, nm_url)
    return (got_error, has_changed, result, node_ips)




def send_data(nodes, nm_url):

    headers = { 'Content-type': 'application/json' } # TODO when authorization is implemented
    endpoint_url = "{}{}" . format(nm_url, '/webapi/parseDhcp')
    result = requests.post(endpoint_url, json.dumps(nodes), headers=headers)
    
    if result.status_code == 200:
        return False, True, result.status_code
    if result.status_code == 400:
        return True, False, result.status_code
    else:
        # unkown error
        #e = {"status": result.status_code, "response": result.json()}
        e = {"status": result.status_code }
        return True, False, e


def main():

    fields = {
        "cloud": {
            "default": "openstack",
            "choices": ['openstack', 'aws'],
            "type": 'str'
        },
        "nodes": {"required": True, "type": "list" },
        "nodemanager": {"required": True, "type": "str" },
        "aws_access_key": {"required": False, "type": "str" },
        "aws_secret_key": {"required": False, "type": "str" },
        "region": {"required": False, "type": "str" },
    }

    choice_map = {
        "openstack": parse_openstack,
        "aws": parse_aws,
    }

    module = AnsibleModule(argument_spec=fields)
    got_error, has_changed, results, nodes = choice_map.get(module.params['cloud'])(module.params)
    
    if not got_error:
        module.exit_json(changed=has_changed, meta=results, nodes=nodes)
    else:
        module.fail_json(msg="An error occured", meta=results)




if __name__ == '__main__':
    main()