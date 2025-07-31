import yaml
import sys
from typing import Any, Dict

def load_config(path: str) -> Dict[str, Any]:
    try:
        with open(path, 'r') as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as ye:
                print(f"Error: Invalid YAML syntax in '{path}':\n  {ye}", file=sys.stderr)
                sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Configuration file '{path}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError as pe:
        print(f"Error: Permission denied reading '{path}': {pe}", file=sys.stderr)
        sys.exit(1)
    except OSError as oe:
        print(f"Error: I/O error opening '{path}': {oe}", file=sys.stderr)
        sys.exit(1)

    if data is None:
        print(f"Warning: '{path}' is empty. No data loaded.", file=sys.stderr)
        return {}
    if not isinstance(data, dict):
        print(f"Error: Unexpected YAML root type in '{path}': expected mapping, got {type(data).__name__}", file=sys.stderr)
        sys.exit(1)

    return data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python config_reader.py <config.yaml>", file=sys.stderr)
        sys.exit(1)

    cfg = load_config(sys.argv[1])
    print("✅ Configuration loaded successfully:")
    print(yaml.dump(cfg, default_flow_style=False))
    for key, val in cfg.items():
        print(f"  {key}: {val}")
