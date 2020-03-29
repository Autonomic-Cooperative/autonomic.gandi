#!/usr/bin/env python3

import json
import os
import traceback
from subprocess import CalledProcessError, check_output

from ansible.module_utils.basic import AnsibleModule, env_fallback

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
  gandi_rest_token:
    description:
      - The Gandi REST API key. It may also be specified by the C(LEXICON_GANDI_AUTH_TOKEN)
        environment variable. See U(https://github.com/AnalogJ/lexicon/blob/ce168132880558415c8c755e65f8e2f9b46cff62/lexicon/providers/gandi.py).
        for more.
    type: str
    required: false
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


def error_msg(domain):
    """Better error message since check_output output is not helpful."""
    return (
        "Unable to retrieve domain info. Did you export "
        "the LEXICON_GANDI_AUTH_TOKEN environment variable? "
        "Does running the following command work? lexicon "
        "gandi list {domain} A"
    ).format(domain=domain)


def get_env():
    """Build environment for running command-line commands."""
    env = os.environ.copy()
    env["PROVIDER"] = "gandi"
    env["LEXICON_GANDI_API_PROTOCOL"] = "rest"
    return env


def retrieve_domain_info(module):
    """Retrieve all information about a specific domain."""
    domain = module.params["domain"]
    env = get_env()

    try:
        return json.loads(
            check_output(
                ["lexicon", "gandi", "list", domain, "A", "--output", "JSON"],
                env=env,
            )
        )
    except CalledProcessError:
        module.fail_json(msg=error_msg(domain))


def create_domain(module):
    """Create a new DNS entry."""
    domain = module.params["domain"]
    ipv4 = module.params["ipv4"]
    env = get_env()

    try:
        return json.loads(
            check_output(
                [
                    "lexicon",
                    "gandi",
                    "create",
                    domain,
                    "A",
                    "--name",
                    domain,
                    "--content",
                    ipv4,
                    "--output",
                    "JSON",
                ],
                env=env,
            )
        )
    except Exception:
        module.fail_json(msg=error_msg(domain))


def delete_domain(module):
    """Delete an existing DNS entry."""
    domain = module.params["domain"]
    ipv4 = module.params["ipv4"]
    env = get_env()

    try:
        return json.loads(
            check_output(
                [
                    "lexicon",
                    "gandi",
                    "delete",
                    domain,
                    "A",
                    "--name",
                    domain,
                    "--content",
                    ipv4,
                    "--output",
                    "JSON",
                ],
                env=env,
            )
        )
    except Exception:
        module.fail_json(msg=error_msg(domain))


def main():
    """Module entrypoint."""
    module = AnsibleModule(
        argument_spec=dict(
            domain=dict(type="str", required=True),
            ipv4=dict(type="str", required=True),
            state=dict(
                type="str", required=True, choices=["present", "absent"]
            ),
            gandi_rest_token=dict(
                type="str",
                required=False,
                no_log=True,
                fallback=(env_fallback, ["LEXICON_GANDI_AUTH_TOKEN"]),
            ),
        ),
        supports_check_mode=False,
        required_together=(["domain", "ipv4"]),
    )

    if not HAS_DNS_LEXICON_DEPENDENCY:
        msg = (
            "Missing dns-lexicon, please run apt "
            "install -y python3-lexicon or install it "
            " using the Ansible `apt` module."
        )
        module.fail_json(msg=msg, exception=DNS_LEXICON_IMP_ERR)

    domains = retrieve_domain_info(module)
    existing_domain = module.params["domain"] in [
        domain["name"] for domain in domains
    ]

    if module.params["state"] == "present":
        if existing_domain:
            module.exit_json(changed=False)
        create_domain(module)
        module.exit_json(changed=True)

    if module.params["state"] == "absent":
        if not existing_domain:
            module.exit_json(changed=False)
        delete_domain(module)
        module.exit_json(changed=True)


if __name__ == "__main__":
    main()
