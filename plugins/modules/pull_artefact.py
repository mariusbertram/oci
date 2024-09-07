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
EXAMPLES = r'''
- name: Pull artefact to /usr/bin
  become: true
  mariusbertram.oci.pull_artefact:
    image: "ghcr.io/mariusbertram/oci_test:test4"
    path: "/usr/bin"
    insecure: False

- name: Pull artefact to tempoath
  mariusbertram.oci.push_artefact:
    target: "ghcr.io/mariusbertram/oci_test:build"

'''
RETURN = r'''
artefacts:
  List of created files

'''
from ansible.module_utils.basic import AnsibleModule
import oras.client
import tempfile


def run_module():
    module_args = dict(
        image=dict(type='str', required=True),
        path=dict(type='str', required=False, default=""),
        insecure=dict(type='bool', required=False, default=False)
    )

    module = AnsibleModule(
        argument_spec=module_args
    )
    image = module.params['image']
    path = module.params['path']

    client = oras.client.OrasClient(tls_verify=module.params['insecure'])

    target_dir = path

    if path == "":
        target_dir = tempfile.mkdtemp()

    artefact = client.pull(target=image, outdir=target_dir)
    result = dict(changed=True, artefacts=artefact)
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
