# Datadog Agent Integrations

Collecting data is cheap; not having it when you need it can be very expensive. So we recommened instrumenting as much of your systems and applications as possible. This integrations repository will help you do that by making it easier to create and share new integrations for Datadog.

# Adding New Integrations

## Requirements

You will need a working [Ruby](https://www.ruby-lang.org) environment. For more information on installing Ruby, please reference [the Ruby installation documentation](https://www.ruby-lang.org/en/documentation/installation/).

You will also need [Wget](https://www.gnu.org/software/wget/). Wget is already installed on most Linux systems and is easy to install on Mac using [Homebrew](http://brew.sh/). *Need Windows instructions link or info*.

## Setup

We've written [a gem](https://rubygems.org/gems/datadog-sdk-testing) and a set of scripts to help you get set up, ease development, and provide testing. To begin:

1. Clone the Github repository
2. Run `gem install bundler`
3. Run `bundle install`

Once the required Ruby gems have been installed by Bundler, you can easily create a [Python](https://www.python.org/) environment:

1. Run `rake setup_env`. This will install a Python virtual environment along with all the components necessary for integration development. This will also create an entry for your new integration in our `.travis.yml` and `circle.yml` continuous integration files to ensure that your tests are run whenever new builds are created.
2. Run `source venv/bin/activate` to activate the installed Python virtual environment. To exit the virtual environment, run `deactivate`. You can learn more about the Python virtual environment on the [Virtualenv documentation](https://virtualenv.pypa.io/en/stable/).

## Building an integration

You can use rake to generate the skeleton for a new integration by running `rake generate:skeleton[my_integration]`, where "my_integration" is the name of your new integration. This will create a new directory, `my_integration`, that contains all the files required for your new integration.

### Integration files

New integrations should contain the following files:

#### `README.md`

Your README file should provide the following sections:

- **Overview** (Required): Let others know what they can expect to do with your integration.
- **Installation** (Required): Provide information about how to install your integration.
- **Configuration** (Required): Detail any steps necessary to configure your integration or the service you are integrating.
- **Validation** (Required): How can users ensure the integration is working as intended?
- **Compatibility** (Required): List the version(s) of the application or service that your integration has been tested and validated against.
- **Metrics** (Required): Include a list of the metrics your integration will provide.
- **Events**: Include a list of events if your integration provides any.
- **Troubleshooting**: Help other users by sharing solutions to common problems they might experience.

#### `check.py`

The file where your check logic should reside.

#### `ci/my_integration.rake`

If your tests require a testing environment, you can use the `install` and `cleanup` tasks to respectively set up and tear down a testing environment.

#### `manifest.json`

This JSON file provides metadata about your integration and should include:

- **`maintainer`**: Provide a valid email address where you can be contacted regarding this integration.
- **`manifest_version`**: The version of this manifest file.
- **`max_agent_version`**: The maximum version of the Datadog agent that is compatible with your integration. We do our best to maintain integration stability within major versions, so you should leave this at the number generated for you. If your integration breaks with a new release of the Datadog agent, please set this number and [submit an issue on the Datadog Agent project](https://github.com/DataDog/dd-agent/blob/master/CONTRIBUTING.md#submitting-issues) (**<<- is that right?**)
- **`min_agent_version`**: The mininmum version of the Datadog agent that is compatible with your integration.
- **`name`**: The name of your integration.
- **`short_description`**: Provide a short description of your integration.
- **`support`**: As a community contributed integration, this should be set to "contrib". Only set this to another value if directed to do so by Datadog staff.
- **`version`**: The current version of your integration.

#### `metadata.csv`

The metadata CSV provides a list of the metrics your integration will provide and basic details that will help inform the Datadog web application as to which graphs and alerts can be provided for the metric.

The CSV should include a header row and the following columns:

- **`metric_name`**: The name of the metric as it should appear in the Datadog web application when creating dashboards or monitors. Often this name is a period delimited combination of the provider, service, and metric (e.g. `aws.ec2.disk_write_ops`) or the application, application feature, and metric (e.g. `apache.net.request_per_s`).
- **`metric_type`**: The type of metric you are reporting. This will influence how the Datadog web application handles and displays your data. Accepted values are: `count`, `guage`, or `rate`.
- **`interval`**: The time interval in seconds that ???
- **`unit_name`**: The label for the unit of measure you are gathering. (e.g. `request`, `byte`, `percent`)
- **`per_unit_name`**: If you are gathering a per unit metric, you may provide an additional unit name here and it will be combined with the `unit_name`. For example, providing a `unit_name` of "request" and a `per_unit_name` of "second" will result in a metric of "requests per second".
- **`description`**: A basic description of the information this metric represents.
- **`orientation`**:
- **`integration`**: The name of your integration. (e.g. "my_integration").
- **`short_name`**: The name of the metric. (e.g. "total resp time", "avg latency")

#### `test_my_integration.py`

We strongly believe in testing code and you should too! Your code tests should be placed in this file.

### Testing your integration

As you build your check and test code, you can use the following to run your tests:

- `rake lint`: Lint your code for potential errors
- `rake ci:run[my_integration]`: Run the tests that you have created in your `test_my_integration.py` file.
- `rake ci:run[default]`: Run the tests you have written in addition to some additional generic tests we have written.

### Teardown and cleanup

When you have finished building your integration, you can run `rake clean_env` to remove the Python virtual environment.

# Reporting Bugs
