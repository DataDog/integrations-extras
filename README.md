# Datadog Agent Integrations

# Adding New Integrations

## Requirements

You will need a working [Ruby](https://www.ruby-lang.org) environment. For more information on installing Ruby, please reference [the Ruby installation documentation](https://www.ruby-lang.org/en/documentation/installation/).

You will also need [Wget](https://www.gnu.org/software/wget/). Wget is already sinstalled on most Linux systems and is easy to install on Mac using [Homebrew](http://brew.sh/). *Need Windows instructions link or info*.

## Setup

We've written a gem and a set of scripts to help you get set up, ease development, and provide testing. To begin:
1. Clone this Github repository
2. Run `gem install bundler`
3. Run `bundle install`

Once the required Ruby gems have been installed by Bundler, you can easily create a [Python](https://www.python.org/) environment:
1. Run `rake setup_env`. This will install a Python virtual environment along with all the components necessary for integration development.
2. Run `source venv/bin/activate` to activate the installed Python virtual environment. To exit the virtual environment, run `deactivate`. You can learn more about the Python virtual environment on the [Virtualenv documentation](https://virtualenv.pypa.io/en/stable/).

## Building an Integration

You can use rake to generate the skeleton for a new integration by running `rake generate:skeleton[my_integration]`, where "my_integration" is the name of your new integration. This will create a new directory, `my_integration`, that contains all the files required for your new integration:

- `check.py`: The file where your check logic should reside.
- `test_my_integration.py`: We strongly believe in testing code and you should too! Your code tests should be placed in this file.

As you build your check and test code, you can use the following to run your tests:

- `rake lint`: Lint your code for potential errors
- `rake ci:run[my_integration]`: Run the tests that you have created in your `test_my_integration.py` file.
- `rake ci:run[default]`: Run the tests you have written in addition to some additional generic tests we have written.

When you have finished building your integration, you can run `rake clean_env` to remove the Python virtual environment.

# Reporting Bugs

