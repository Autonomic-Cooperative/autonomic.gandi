# autonomic.gandi

[![Build Status](https://drone.autonomic.zone/api/badges/autonomic-cooperative/autonomic.gandi/status.svg)](https://drone.autonomic.zone/autonomic-cooperative/autonomic.gandi)

Ansible libraries for manging Gandi resources.

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
