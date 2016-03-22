#!/usr/bin/env rake
# encoding: utf-8
# 3p
require 'rake/clean'
require 'rubocop/rake_task'

# Flavored Travis CI jobs
require './ci/default'
require './ci/redis_sentinel'

CLOBBER.include '**/*.pyc'

# CI-like environment for local use
unless ENV['CI']
  rakefile_dir = File.dirname(__FILE__)
  ENV['TRAVIS_BUILD_DIR'] = rakefile_dir
  ENV['INTEGRATIONS_DIR'] = File.join(rakefile_dir, 'embedded')
  ENV['PIP_CACHE'] = File.join(rakefile_dir, '.cache/pip')
  ENV['VOLATILE_DIR'] = '/tmp/integration-sdk-testing'
  ENV['CONCURRENCY'] = ENV['CONCURRENCY'] || '2'
  ENV['NOSE_FILTER'] = 'not windows'
  ENV['RUN_VENV'] = 'true'
end

desc 'Setup a development environment for the SDK'
task 'setup_env' do
  `mkdir -p venv`
  `wget -O venv/virtualenv.py https://raw.github.com/pypa/virtualenv/1.11.6/virtualenv.py`
  `python venv/virtualenv.py  --no-site-packages --no-pip --no-setuptools venv/`
  `wget -O venv/ez_setup.py https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py`
  `venv/bin/python venv/ez_setup.py`
  `wget -O venv/get-pip.py https://bootstrap.pypa.io/get-pip.py`
  `venv/bin/python venv/get-pip.py`
  `venv/bin/pip install -r requirements.txt` if File.exist?('requirements.txt')
  `venv/bin/pip install -r requirements-test.txt` if File.exist?('requirements-test.txt')
  # These deps are not really needed, so we ignore failures
  ENV['PIP_COMMAND'] = 'venv/bin/pip'
  `./utils/pip-allow-failures.sh requirements-opt.txt` if File.exist?('requirements-opt.txt')
  `git clone https://github.com/DataDog/dd-agent.git ./embedded/dd-agent`
  `cd ./embedded/dd-agent ; git fetch && git checkout jaime/sdktesting ; cd -`
  `echo "$PWD/embedded/dd-agent/" > venv/lib/python2.7/site-packages/datadog-agent.pth`
end

namespace :test do
  desc 'cProfile tests, then run pstats'
  task 'profile:pstats' => ['test:profile'] do
    sh 'python -m pstats stats.dat'
  end

  desc 'Display test coverage for checks'
  task 'coverage' => 'ci:default:coverage'
end

RuboCop::RakeTask.new(:rubocop) do |t|
  t.patterns = ['ci/**/*.rb', 'Gemfile', 'Rakefile']
end

desc 'Lint the code through pylint'
task 'lint' => ['ci:default:lint'] do
end

namespace :ci do
  desc 'Run integration tests'
  task :run, :flavor do |_, args|
    puts 'Assuming you are running these tests locally' unless ENV['TRAVIS']
    flavor = args[:flavor] || ENV['TRAVIS_FLAVOR'] || 'default'
    flavors = flavor.split(',')
    flavors.each { |f| Rake::Task["ci:#{f}:execute"].invoke }
  end
end

task default: ['lint', 'ci:run']
