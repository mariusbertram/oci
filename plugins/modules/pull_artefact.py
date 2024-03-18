#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: pull_artefact
short_description: Pulls artefact from an OCI registry

version_added: "0.1.0"

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
        auth_cong=dict(type='str', default=""),
        image=dict(type='str', required=True),
        path=dict(type='str', required=False, default=""),
        insecure=dict(type='bool', required=False, default=False)
    )

    module = AnsibleModule(
        argument_spec=module_args
    )

    username = module.params['username']
    password = module.params['password']
    auth_config = module.params['auth_config']
    image = module.params['image']
    path = module.params['path']

    client = oras.client.OrasClient(tls_verify=module.params['insecure'], )

    if username != "" and auth_config == "":
        client.set_basic_auth(username, password)

    if auth_config != "":
        client.login(config_path=auth_config, username=username, password=password)

    target_dir = path

    if path == "":
        target_dir = tempfile.mkdtemp()

    os.chdir(target_dir)

    artifact = client.pull(target=image)




def main():
    run_module()


if __name__ == '__main__':
    main()
