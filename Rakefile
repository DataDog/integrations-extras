#!/usr/bin/env rake
# encoding: utf-8
# 3p
require 'rake/clean'
require 'rubocop/rake_task'

# Flavored Travis CI jobs
require './ci/default'
Rake.add_rakelib 'ci/'

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
  ENV['SDK_TESTING'] = 'true'
end

desc 'Setup a development environment for the SDK'
task 'setup_env' do
  `mkdir -p venv`
  `wget -q -O venv/virtualenv.py https://raw.github.com/pypa/virtualenv/1.11.6/virtualenv.py`
  `python venv/virtualenv.py  --no-site-packages --no-pip --no-setuptools venv/`
  `wget -q -O venv/ez_setup.py https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py`
  `venv/bin/python venv/ez_setup.py`
  `wget -q -O venv/get-pip.py https://bootstrap.pypa.io/get-pip.py`
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

desc 'Setup git hooks'
task 'setup_hooks' do
  pwd = File.dirname(__FILE__)
  sh "ln -sf #{pwd}/ci/hooks/pre-commit.py #{pwd}/.git/hooks/pre-commit"
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

desc 'Find requirements conflicts'
task 'requirements' => ['ci:default:requirements'] do
end

namespace :generate do
  desc 'Setup a development environment for the SDK'
  task :skeleton, :option do |_, args|
    puts "generating skeleton files for #{args[:option]}"
    capitalized = args[:option].capitalize
    sh 'mkdir -p ./ci'
    sh "mkdir -p ./#{args[:option]}"
    sh "wget -q -O ./ci/#{args[:option]}.rake https://raw.githubusercontent.com/DataDog/integrations-extras/jaime/skeleton/skeleton/ci/skeleton.rake"
    sh "wget -q -O ./#{args[:option]}/manifest.json \
    https://raw.githubusercontent.com/DataDog/integrations-extras/jaime/skeleton/skeleton/manifest.json"
    sh "wget -q -O ./#{args[:option]}/check.py https://raw.githubusercontent.com/DataDog/integrations-extras/jaime/skeleton/skeleton/check.py"
    sh "wget -q -O ./#{args[:option]}/test_#{args[:option]}.py \
    https://raw.githubusercontent.com/DataDog/integrations-extras/jaime/skeleton/skeleton/test_skeleton.py"
    sh "wget -q -O ./#{args[:option]}/metadata.csv https://raw.githubusercontent.com/DataDog/integrations-extras/jaime/skeleton/skeleton/metadata.csv"
    sh "wget -q -O ./#{args[:option]}/requirements.txt \
    https://raw.githubusercontent.com/DataDog/integrations-extras/jaime/skeleton/skeleton/requirements.txt"
    sh "wget -q -O ./#{args[:option]}/README.md https://raw.githubusercontent.com/DataDog/integrations-extras/jaime/skeleton/skeleton/README.md"
    sh "find ./#{args[:option]} -type f -exec sed -i '' \"s/skeleton/#{args[:option]}/g\" {} \\;"
    sh "find ./#{args[:option]} -type f -exec sed -i '' \"s/Skeleton/#{capitalized}/g\" {} \\;"
    sh "sed -i '' \"s/skeleton/#{args[:option]}/g\" ./ci/#{args[:option]}.rake"
    sh "sed -i '' \"s/Skeleton/#{capitalized}/g\" ./ci/#{args[:option]}.rake"
    sh "git add ./ci/#{args[:option]}.rake"
    sh "git add ./#{args[:option]}/*"

    new_file = './circle.yml.new'
    File.open(new_file, 'w') do |fo|
      File.foreach('./circle.yml') do |line|
        fo.puts "        - rake ci:run[#{args[:option]}]" if line =~ /bundle\ exec\ rake\ requirements/
        fo.puts line
      end
    end
    File.delete('./circle.yml')
    File.rename(new_file, './circle.yml')

    new_file = './.travis.yml.new'
    File.open(new_file, 'w') do |fo|
      File.foreach('./.travis.yml') do |line|
        fo.puts "  - rake ci:run[#{args[:option]}]" if line =~ /bundle\ exec\ rake\ requirements/
        fo.puts line
      end
    end
    File.delete('./.travis.yml')
    File.rename(new_file, './.travis.yml')
  end
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
