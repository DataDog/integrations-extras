"""Utility functions for the Rundeck integration."""


def rename_metric(original_name, prefix):
    """Rename the original metric name from /metrics/metrics API"""
    if original_name.startswith(f"{prefix}."):
        parts = original_name[len(prefix) + 1 :].split(".")
    else:
        parts = original_name.split(".")

    final_parts = [convert_case(part) for part in parts]

    return ".".join(final_parts)


def convert_case(part):
    """Convert string from camelCase or PascalCase to snake_case"""
    chars = []
    for i, char in enumerate(part):
        if char.isupper() and i > 0:
            chars.append("_")
        chars.append(char.lower())
    return "".join(chars)


def get_nested_val(data, key_list):
    """Extract nested key value from a dict"""
    current_node = data
    for key in key_list:
        if isinstance(current_node, dict) and key in current_node:
            current_node = current_node[key]
        else:
            return None

    return current_node
