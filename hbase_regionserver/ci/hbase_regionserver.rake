require 'ci/common'

def hbase_regionserver_version
  ENV['FLAVOR_VERSION'] || 'latest'
end

def hbase_regionserver_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/hbase_regionserver_#{hbase_regionserver_version}"
end

namespace :ci do
  namespace :hbase_regionserver do |flavor|
    task before_install: ['ci:common:before_install']

    task :install do
      Rake::Task['ci:common:install'].invoke('hbase_regionserver')
      sh %(docker-compose -f \
           #{ENV['TRAVIS_BUILD_DIR']}/hbase_regionserver/ci/resources/docker-compose-hbase.yaml up -d)
      Wait.for 10_101
      Wait.for 10_102
      wait_on_docker_logs('resources_hbase_1', '30', 'HBase Master', 'http://localhost:60010', 'HBase Region Server', 'http://localhost:60030')
    end

    task before_script: ['ci:common:before_script']

    task script: ['ci:common:script'] do
      this_provides = [
        'hbase_regionserver'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cleanup: ['ci:common:cleanup'] do
      sh %(docker-compose -f \
           #{ENV['TRAVIS_BUILD_DIR']}/hbase_regionserver/ci/resources/docker-compose-hbase.yaml down -v)
    end

    task :execute do
      exception = nil
      begin
        %w(before_install install before_script).each do |u|
          Rake::Task["#{flavor.scope.path}:#{u}"].invoke
        end
        if !ENV['SKIP_TEST']
          Rake::Task["#{flavor.scope.path}:script"].invoke
        else
          puts 'Skipping tests'.yellow
        end
        Rake::Task["#{flavor.scope.path}:before_cache"].invoke
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
