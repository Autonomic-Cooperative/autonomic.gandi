#!/usr/bin/python3

import traceback
from subprocess import check_output

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

DOCUMENTATION = """
---
module: gandi_dns
short_description: Manage Gandi DNS entries.
requirements:
  - python >= 3.8
  - gandi.cli >= 1.5
author:
  - Luke Murphy (@decentral1se)
options:
  apirest_key:
    description:
      - The Gandi REST API key. It may also be specified by the
        C(API_REST_KEY) environment variable. See the
        U(https://github.com/Gandi/gandi.cli/blob/master/gandicli.man.rst#environment)
    type: str
    required: true
  domain:
    description: The domain name you're working with.
    type: str
    required: true
  ipv4:
    description: The IP v4 address that the domain refers to.
    type: str
    required: true
  state:
    description:
      - The desired instance state.
    type: str
    choices:
        - present
        - absent
    required: true
"""

EXAMPLES = """
- name: Create a new Gandi DNS entry
  gandi_dns:
    apirest_key: "{{ apirest_key }}"
    domain: foobar.autonomic.zone
    ipv4: 192.168.1.2
    state: present
"""

RETURN = """
TODO
"""

GANDI_CLI_IMP_ERR = None
try:
    from gandi import cli  # noqa

    HAS_GANDI_DEPENDENCY = True
except ImportError:
    GANDI_IMP_ERR = traceback.format_exc()
    HAS_GANDI_DEPENDENCY = False


def retrieve_domain(domain):
    """Retrieve information about an existing domain."""
    pass


def main():
    """Module entrypoint."""
    module = AnsibleModule(argument_spec={})

    if not HAS_GANDI_DEPENDENCY:
        msg = missing_required_lib('gandi.cli')
        module.fail_json(msg=msg, exception=GANDI_IMP_ERR)

    if module.params['state'] == 'present':
        domain = retrieve_domain(module.params['domain'])

    if module.params['state'] == 'absent':
        pass


if __name__ == "__main__":
    main()
