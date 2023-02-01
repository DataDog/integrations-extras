def get_by_path(root: dict, path: str) -> any:
    """Access a nested object in root by item sequence."""

    items = path.split(".")
    for key in items:
        if root is None:
            continue
        root = root.get(key)
    return root
