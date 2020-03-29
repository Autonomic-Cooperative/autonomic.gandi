# autonomic.gandi

[![Build Status](https://drone.autonomic.zone/api/badges/autonomic-cooperative/autonomic.gandi/status.svg)](https://drone.autonomic.zone/autonomic-cooperative/autonomic.gandi)

Ansible libraries for managing Gandi resources.

## Example

```yaml
---
- hosts: localhost
  gather_facts: false
  connection: local
  tasks:
    - name: Create foobar.autonomic.zone
      gandi_dns:
        gandi_rest_token: abc...
        domain: foobar.autonomic.zone
        ipv4: 94.130.105.60
        state: present
```

## Features

- [x] Create a new DNS entry
- [x] Delete an existing DNS entry
- [ ] Update an existing DNS entry

## Requirements

- [Ansible >= 2.9.6](https://pypi.org/project/ansible/)
- [dns-lexicon >= 3.3.19](https://pypi.org/project/dns-lexicon/) (if using `gandi_dns` module)

```bash
$ pip install ansible==2.6.9 "dns-lexicon[gandi]==3.3.19"
```

These should be present on the localhost where you run Ansible.

## Gandi DNS Setup

If you want to use the `gandi_dns` module you need to prepare the environment.

```bash
export PROVIDER="gandi"
export LEXICON_GANDI_AUTH_TOKEN="${pass show users/decentral1se/gandi/api_key)"
export LEXICON_GANDI_API_PROTOCOL="rest"
```

You can test that everything is working by running the following.

```bash
$ lexicon gandi list autonomic.zone A
```

The `gandi_dns` module will provide the `PROVIDER` and
`LEXICON_GANDI_API_PROTOCOL` environment variables internally so you only need
to pass `LEXICON_GANDI_AUTH_TOKEN` as the `gandi_rest_token` argument to the
task or expose it in the environment and it will be picked up.

## Usage

Include an entry in your `requirements.yml` like so.

```yaml
- src: https://git.autonomic.zone/autonomic-cooperative/autonomic.gandi/archive/0.0.3.tar.gz
  name: autonomic.gandi
```

See the [releases](https://git.autonomic.zone/autonomic-cooperative/autonomic.gandi/releases) for which is the latest version.

Then make sure to download the role with `ansible-galaxy install -r requirements.yml`.
