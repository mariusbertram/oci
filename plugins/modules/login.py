#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: login
short_description: Login to an OCI registry

version_added: "0.1.0"

author:
    - Marius Bertram (@mariusbertram)
'''
EXAMPLES = r'''
- name: login to an OCI registry
  mariusbertram.oci.login:
    hostname: "ghcr.io"
    username: "{{ username }}"
    password: "{{ password }}"
    insecure: False
'''
RETURN = r'''
msg:
  Login Succeeded or Login Failed.

'''
from ansible.module_utils.basic import AnsibleModule
import oras.client

def run_module():
    module_args = dict(
        username=dict(type='str', required=True),
        password=dict(type='list', required=True, no_log=True),
        hostname=dict(type='str', required=True),
        insecure=dict(type='bool', required=False, default=False)
    )

    module = AnsibleModule(
        argument_spec=module_args
    )

    username = module.params['username']
    password = module.params['password']
    hostname = module.params['hostname']

    client = oras.client.OrasClient(tls_verify=module.params['insecure'])

    res = client.login(username=username, password=password, hostname=hostname)

    result = dict(changed=True, msg=res.get("Status"))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
