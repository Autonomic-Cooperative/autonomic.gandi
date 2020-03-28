# autonomic.gandi

[![Build Status](https://drone.autonomic.zone/api/badges/autonomic-cooperative/autonomic.gandi/status.svg)](https://drone.autonomic.zone/autonomic-cooperative/autonomic.gandi)

Ansible libraries for manging Gandi resources.

## Requirements

- [Ansible >= 2.9.6](https://pypi.org/project/ansible/)
- [Gandi.cli >= 1.5](https://pypi.org/project/gandi.cli/)

```bash
$ pip install ansible==2.6.9 gandi.cli==1.5
```

These should be present on the localhost where you run Ansible.

## Usage

Include an entry in your `requirements.yml` like so.

```yaml
- src: https://git.autonomic.zone/autonomic-cooperative/autonomic.gandi
  version: 0.0.1
  name: autonomic.gandi
```

See the [releases](https://git.autonomic.zone/autonomic-cooperative/autonomic.gandi/releases) for which is the latest version.

Then make sure to download the role with `ansible-galaxy install -r requirements.yml`.

## Roadmap

- [ ] DNS entries
  - [ ] Create
  - [ ] Update
  - [ ] Delete
