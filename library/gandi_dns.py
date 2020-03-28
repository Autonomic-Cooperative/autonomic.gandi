#!/usr/bin/env python3

import json
import traceback
from subprocess import CalledProcessError, check_output

from ansible.module_utils.basic import (
    AnsibleModule,
    env_fallback,
    missing_required_lib,
)

DOCUMENTATION = """
---
module: gandi_dns
short_description: Manage Gandi DNS entries.
requirements:
  - python >= 3.8
  - dns-lexicon >= 3.3.19
author:
  - Luke Murphy (@decentral1se)
options:
  domain:
    description: The domain name you're working with.
    type: str
    required: true
  ipv4:
    description: The IP v4 address that the domain refers to.
    type: str
    required: true
  rest_api_key:
    description:
      - The Gandi REST API key. It may also be specified by the C(LEXICON_GANDI_AUTH_TOKEN)
        environment variable. See U(https://github.com/AnalogJ/lexicon/blob/ce168132880558415c8c755e65f8e2f9b46cff62/lexicon/providers/gandi.py).
        for more.
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
"""  # noqa

EXAMPLES = """
- name: Create a new Gandi DNS entry
  gandi_dns:
    rest_api_key: "{{ lookup('env', 'LEXICON_GANDI_AUTH_TOKEN') }}"
    domain: foobar.autonomic.zone
    ipv4: 192.168.1.2
    state: present
"""

DNS_LEXICON_IMP_ERR = None
try:
    from lexicon.providers import gandi  # noqa

    HAS_DNS_LEXICON_DEPENDENCY = True
except ImportError:
    DNS_LEXICON_IMP_ERR = traceback.format_exc()
    HAS_DNS_LEXICON_DEPENDENCY = False


def retrieve_domain_info(module):
    """Retrieve all information about a specific domain."""
    try:
        return json.loads(
            check_output(
                [
                    "lexicon",
                    "gandi",
                    "list",
                    module.params["domain"],
                    "A",
                    "--output",
                    "JSON",
                ]
            )
        )
    except CalledProcessError as exception:
        module.fail_json(
            msg="Unable to retrieve domain info. Saw: %s" % str(exception)
        )


def create_domain(module):
    """Create a new DNS entry."""
    try:
        return json.loads(
            check_output(
                [
                    "lexicon",
                    "gandi",
                    "create",
                    module.params["domain"],
                    "A",
                    "--name",
                    module.params["domain"],
                    "--content",
                    module.params["ipv4"],
                    "--output",
                    "JSON",
                ]
            )
        )
    except Exception as exception:
        module.fail_json(
            msg="Unable to create domain entry. Saw: %s" % str(exception)
        )


def delete_domain(module):
    """Delete an existing DNS entry."""
    try:
        return json.loads(
            check_output(
                [
                    "lexicon",
                    "gandi",
                    "delete",
                    module.params["domain"],
                    "A",
                    "--name",
                    module.params["domain"],
                    "--content",
                    module.params["ipv4"],
                    "--output",
                    "JSON",
                ]
            )
        )
    except Exception as exception:
        module.fail_json(
            msg="Unable to delete domain entry. Saw: %s" % str(exception)
        )


def main():
    """Module entrypoint."""
    module = AnsibleModule(
        argument_spec=dict(
            domain=dict(type='str', required=True),
            ipv4=dict(type='str', required=True),
            state=dict(
                type='str', required=True, choices=['present', 'absent']
            ),
            rest_api_key=dict(
                type='str',
                required=True,
                no_log=True,
                fallback=(env_fallback, ['LEXICON_GANDI_AUTH_TOKEN']),
            ),
        ),
        supports_check_mode=False,
        required_together=(['domain', 'ipv4']),
    )

    if not HAS_DNS_LEXICON_DEPENDENCY:
        msg = missing_required_lib('lexicon')
        module.fail_json(msg=msg, exception=DNS_LEXICON_IMP_ERR)

    domains = retrieve_domain_info(module)
    existing_domain = module.params['domain'] in [
        domain['name'] for domain in domains
    ]

    if module.params['state'] == 'present':
        if existing_domain:
            module.exit_json(changed=False)
        create_domain(module)
        module.exit_json(changed=True)

    if module.params['state'] == 'absent':
        if not existing_domain:
            module.exit_json(changed=False)
        delete_domain(module)
        module.exit_json(changed=True)


if __name__ == "__main__":
    main()
