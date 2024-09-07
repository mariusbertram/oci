#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: push_artefact
short_description: Pushes artefact to an OCI registry

version_added: "0.1.0"

author:
    - Marius Bertram (@mariusbertram)
'''

EXAMPLES = r'''
- name: Push all json Files
  mariusbertram.oci.push_artefact:
    target: "ghcr.io/mariusbertram/oci_test:test4"
    files: "{{ item }}"
    insecure: False
  with_fileglob:
    - "./*.json"
    
- name: Push a single File
  mariusbertram.oci.push_artefact:
    target: "ghcr.io/mariusbertram/oci_test:build"
    files: 
      - "./out/test"
'''
from ansible.module_utils.basic import AnsibleModule
import oras.client

def run_module():
    module_args = dict(
        target=dict(type='str', required=True),
        files=dict(type='list', required=True),
        insecure=dict(type='bool', required=False, default=False)
    )

    module = AnsibleModule(
        argument_spec=module_args
    )

    target = module.params['target']
    files = module.params['files']

    client = oras.client.OrasClient(tls_verify=module.params['insecure'])

    res = client.push(files=files, target=target)

    result = dict(changed=True, msg=res.status_code)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
