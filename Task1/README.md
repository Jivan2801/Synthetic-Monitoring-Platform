
# YAML Reader Script

## What I Did

- Used `yaml.safe_load()` to securely parse YAML files.
- Handled common errors like:
  - File not found
  - Invalid YAML syntax
  - Empty or incorrect YAML structure
- Displayed clear error messages.
- Printed the parsed configuration in a readable format.

## How to Run

1. Make sure `PyYAML` is installed:

```bash
pip install pyyaml
```

2. Run the script:

```bash
python config_reader.py sample_config.yaml
```

Replace `sample_config.yaml` with your actual YAML file name.
