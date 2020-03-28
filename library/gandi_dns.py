#!/usr/bin/python3

DOCUMENTATION = """
---
module: gandi_dns
short_description: Manage Gandi DNS entries
"""

EXAMPLES = """
- name: Create a new Gandi DNS entry
  gandi_dns:
    apirest_key: "{{ apirest_key }}"
    domain: foobar.autonomic.zone
    ipv4: 192.168.1.2
"""

from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(argument_spec={})
    module.exit_json(changed=False, meta={"TO": "DO"})


if __name__ == "__main__":
    main()
