# NVML Datadog check

## Development

### Regenerate API protobuf code

```shell
$ python3 -m venv .venv
$ . .venv/bin/activate
(venv) $ python3 -m pip install -r requirements.txt
(venv) $ python3 -m grpc_tools.protoc --python_out=. --proto_path=. api.proto
(venv) $ deactivate
$
```

