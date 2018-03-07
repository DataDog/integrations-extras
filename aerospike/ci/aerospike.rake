require 'ci/common'

def aerospike_version
  ENV['FLAVOR_VERSION'] || 'latest'
end

def aerospike_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/aerospike_#{aerospike_version}"
end

container_name = 'dd-test-aerospike'
container_port = 3003

namespace :ci do
  namespace :aerospike do |flavor|
    task before_install: ['ci:common:before_install'] do
      sh %(docker kill $(docker ps -q --filter name=#{container_name}) || true)
      sh %(docker rm $(docker ps -aq --filter name=#{container_name}) || true)
    end

    task install: ['ci:common:install'] do
      sh %(docker run -d -p 3000:3000 -p3003:3003 --name #{container_name} aerospike/aerospike-server)
    end

    task before_script: ['ci:common:before_script'] do
      Wait.for container_port
      count = 0
      logs = `docker logs #{container_name} 2>&1`
      puts 'Waiting for Aerospike to come up'
      until count == 20 || logs.include?('service ready: soon there will be cake!')
        sleep_for 2
        logs = `docker logs #{container_name} 2>&1`
        count += 1
      end
      if logs.include? 'service ready: soon there will be cake!'
        puts 'Aerospike is up!'
      end
    end

    task script: ['ci:common:script'] do
      this_provides = [
        'aerospike'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cleanup: ['ci:common:cleanup'] do
      sh %(docker kill $(docker ps -q --filter name=#{container_name}) || true)
      sh %(docker rm $(docker ps -aq --filter name=#{container_name}) || true)
    end

    task :execute do
      exception = nil
      begin
        %w[before_install install before_script].each do |u|
          Rake::Task["#{flavor.scope.path}:#{u}"].invoke
        end
        Rake::Task["#{flavor.scope.path}:script"].invoke
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
