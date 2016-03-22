require 'rake'

require './ci/common'

namespace :ci do
  namespace :default do |flavor|
    task before_install: ['ci:common:before_install']

    task :coverage do
      ci_dir = File.dirname(__FILE__)
      sdk_dir = File.join(ci_dir, '..')

      integrations = []
      untested = []
      testable = []
      pyfiles = Dir.glob(File.join(sdk_dir, '**/test_*.py')).reject do |path|
        !%r{#{sdk_dir}/embedded/.*$}.match(path).nil? || !%r{#{sdk_dir}\/venv\/.*$}.match(path).nil?
      end
      pyfiles.each do |check|
        integration_name = /test_((\w|_)+).py$/.match(check)[1]
        integrations.push(integration_name)
        if File.exist?(check)
          testable.push(check)
        else
          untested.push(check)
        end
      end
      total_checks = (untested + testable).length
      unless untested.empty?
        puts "Untested checks (#{untested.length}/#{total_checks})".red
        puts '-----------------------'.red
        untested.each { |check_name| puts check_name.red }
        puts ''
      end
    end

    task install: ['ci:common:install']

    task lint: ['rubocop'] do
      sh %(flake8)
    end

    task script: ['ci:common:script', :coverage, :lint] do
      Rake::Task['ci:common:run_tests'].invoke(['default'])
    end

    task cleanup: ['ci:common:cleanup']

    task :execute do
      exception = nil
      begin
        %w(before_install install script).each do |t|
          Rake::Task["#{flavor.scope.path}:#{t}"].invoke
        end
      rescue => e
        exception = e
        puts "Failed task: #{e.class} #{e.message}".red
      end
      if ENV['SKIP_CLEANUP']
        puts 'Skipping cleanup, disposable environments are great'.yellow
      else
        puts 'Cleaning up'
        Rake::Task["#{flavor.scope.path}:cleanup"].invoke
      end
      raise exception if exception
    end
  end
end
