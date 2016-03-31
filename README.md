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

# Lint
bundle exec rake lint

# Run the default test
rake ci:run[default]

# Run a flavored test
bundle exec rake ci:run[redis_sentinel]
```

### Generate your tests

- `rake gen:test integration_name`
- Add your flavor to the `circle.yml` file, so you can run your tests on CircleCI.


