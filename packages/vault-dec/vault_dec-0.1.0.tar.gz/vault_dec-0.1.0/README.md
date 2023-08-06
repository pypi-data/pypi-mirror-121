# vault_dec
[![GitHub Actions](https://github.com/alekseyl1992/vault_dec/workflows/release/badge.svg)](https://github.com/alekseyl1992/vault_dec/actions?query=workflow%3Arelease)
[![PyPI](https://img.shields.io/pypi/v/vault_dec.svg)](https://pypi.org/project/vault_dec)

Decrypts arbitrary text files (configs, k8s resource specs) by substituting values from HashiCorp Vault.

## Installation
```bash
pip install vault_dec
```

## Usage example
### Config (input file)
```yaml
apiVersion: v1
kind: Secret
type: Opaque
metadata:
  name: dev-basic-auth
stringData:
  auth: 'vault:dev-basic-auth'
```

### Command to run
```bash
    - python -m vault_dec
      --addr=<your_vault_address>
      --token=<your_vault_token>
      --prefix=/secret/apps
      .kube/your_chart/templates/secrets.yaml
```
