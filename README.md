## Contributing
### Generate your integration skeleton

- `rake generate:skeleton[integration_name]`
- write integraiton
- write tests

## Testing your code
### Setup your environment

Required:
- python 2.6 or 2.7
- bundler

```
# Create a virtual environment and install the dependencies:
cd integrations-extras
bundle install
rake setup_env

# Activate the virtual environment
source venv/bin/activate

# setup git hooks if you wish
rake setup_hooks

# Lint
bundle exec rake lint

# Run the default test
rake ci:run[default]

# Run any flavored test
bundle exec rake ci:run[redis_sentinel]
```



