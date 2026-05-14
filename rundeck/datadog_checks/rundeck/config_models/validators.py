# Here you can include additional config validators or transformers


def initialize_instance(values, **kwargs):
    api_version = values.get("api_version")
    if api_version is not None and api_version < 30:
        raise ValueError(f"Minimum API version is 30, got {api_version}")
    return values
