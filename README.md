# autonomic.gandi

[![Build Status](https://drone.autonomic.zone/api/badges/autonomic-cooperative/autonomic.gandi/status.svg)](https://drone.autonomic.zone/autonomic-cooperative/autonomic.gandi)

Ansible libraries for manging Gandi resources.

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
$ lexicon gandi list autonomic.zone
```

## Usage

Include an entry in your `requirements.yml` like so.

```yaml
- src: https://git.autonomic.zone/autonomic-cooperative/autonomic.gandi
  version: 0.0.1
  name: autonomic.gandi
```

See the [releases](https://git.autonomic.zone/autonomic-cooperative/autonomic.gandi/releases) for which is the latest version.

Then make sure to download the role with `ansible-galaxy install -r requirements.yml`.
