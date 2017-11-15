require 'ci/common'

def logstash_version
  ENV['FLAVOR_VERSION'] || '5.6'
end

def logstash_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/logstash_#{logstash_version}"
end

container_name = 'dd-logstash'
container_port = 9600

namespace :ci do
  namespace :logstash do |flavor|
    task before_install: ['ci:common:before_install'] do
      sh %(docker kill #{container_name} 2>/dev/null || true)
      sh %(docker rm #{container_name} 2>/dev/null || true)
    end

    task :install do
      Rake::Task['ci:common:install'].invoke('logstash')
      # sample docker usage
      # sh %(docker create -p XXX:YYY --name logstash source/logstash:logstash_version)
      # sh %(docker start logstash)
      docker_image = 'logstash:' + logstash_version
      cmd = "logstash -e 'input { stdin { } } filter { json { source => 'message' } } output { stdout { } }' --http.host 0.0.0.0"
      sh %(docker run -d --name #{container_name} -p #{container_port}:#{container_port} #{docker_image} #{cmd})
    end

    task before_script: ['ci:common:before_script'] do
      Wait.for 'http://localhost:9600', 20
    end

    task script: ['ci:common:script'] do
      this_provides = [
        'logstash'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cleanup: ['ci:common:cleanup'] do
      sh %(docker kill #{container_name} 2>/dev/null || true)
      sh %(docker rm #{container_name} 2>/dev/null || true)
    end

    task :execute do
      exception = nil
      begin
        %w[before_install install before_script].each do |u|
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
