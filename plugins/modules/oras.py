#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: oras
short_description: Pulls and Push an image from an OCI registry

version_added: "1.0.0"

author:
    - Marius Bertram (@mariusbertram)
'''

from ansible.module_utils.basic import AnsibleModule
import oras.client
import os
import tempfile


def run_module():
    module_args = dict(
        username=dict(type='str', default=""),
        password=dict(type='str', default="", no_log=True),
        image=dict(type='str', required=True),
        path=dict(type='str', required=False, default=""),
        insecure=dict(type='bool', required=False, default=False)
    )

    module = AnsibleModule(
        argument_spec=module_args
    )

    username = module.params['username']
    password = module.params['password']
    image = module.params['image']
    path = module.params['path']

    client = oras.client.OrasClient(tls_verify=module.params['insecure'])

    if username != "":
        client.set_basic_auth(username, password)

    target_dir = path

    if path == "":
        target_dir = tempfile.mkdtemp()

    os.chdir(target_dir)

    artifact = client.pull(target=image)

    return module.exit_json(changed=True, resource=artifact)


def main():
    run_module()


if __name__ == '__main__':
    main()
