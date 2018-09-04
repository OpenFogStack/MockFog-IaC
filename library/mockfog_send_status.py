#!/usr/bin/python

from ansible.module_utils.basic import *

import json
import requests

    
def send_data(msg, nm_url):

    headers = { 'Content-type': 'application/json' } # TODO when authorization is implemented
    endpoint_url = "{}{}" . format(nm_url, '/webapi/ansiblelog')
    result = requests.post(endpoint_url, json.dumps(msg), headers=headers)
    
    if result.status_code == 200:
        return False, True, result.status_code, result.json()
    if result.status_code == 428:
        return True, False, result.status_code, result.json()
    else:
        # unkown error
        return True, False, result.status_code, result.json()


def main():

    fields = {
        "nodemanager": {"required": True, "type": "str" },
        "status": {
            "default": "BOOTSTRAPPED",
            "choices": ['BOOTSTRAPPED', 'ERROR']
        },
    }

    module = AnsibleModule(argument_spec=fields)
    status = module.params['status']
    nm_url = module.params['nodemanager']
    
    msg = {}
    msg['status'] = status

    got_error, has_changed, status_code, result = send_data(msg, nm_url )
    
    if not got_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="An error occured", meta=result)




if __name__ == '__main__':
    main()