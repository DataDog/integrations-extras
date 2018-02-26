require 'ci/common'

def gnatsd_streaming_version
  ENV['FLAVOR_VERSION'] || 'latest'
end

def gnatsd_streaming_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/gnatsd_streaming_#{gnatsd_streaming_version}"
end

def gnatsd_streaming_temp_dir
  ENV['VOLATILE_DIR'] + '/gnatsd_streaming'
end

container_name = 'dd-test-gnatsd-streaming'

namespace :ci do
  namespace :gnatsd_streaming do |flavor|
    task before_install: ['ci:common:before_install'] do
      Rake::Task['ci:gnatsd_streaming:cleanup'].invoke
    end

    task :install do
      Rake::Task['ci:common:install'].invoke('gnatsd_streaming')
      volumes = "--volume=#{gnatsd_streaming_temp_dir}/data:/usr/share/nats/data"
      publish = '--publish=4222:4222 --publish=8222:8222'

      # Set up NATS Streaming
      sh %(docker run -d --name #{container_name}-server #{publish} #{volumes} nats-streaming:0.7.0)

      # Set up Streaming channels
      benchmark = "/go/src/github.com/nats-io/go-nats-streaming/examples/stan-bench/main.go -s nats://#{container_name}-server:4222 -n 10"
      sh %(docker run -d --name #{container_name}-channels --link #{container_name}-server golang:1.10.0 bash -l -c "sleep infinity")
      sh %(docker exec #{container_name}-channels go get -v github.com/nats-io/go-nats-streaming)
      sh %(docker exec #{container_name}-channels go run #{benchmark} test.channel1)
      sh %(docker exec #{container_name}-channels go run #{benchmark} test.channel2)
      sh %(docker exec #{container_name}-channels go run #{benchmark} test.channel3)
    end

    task before_script: ['ci:common:before_script']

    task script: ['ci:common:script'] do
      this_provides = [
        'gnatsd_streaming'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cleanup: ['ci:common:cleanup'] do
      sh %(docker stop #{container_name}-server #{container_name}-channels || true)
      sh %(docker rm #{container_name}-server #{container_name}-channels || true)
      sh %(rm -rf #{gnatsd_streaming_temp_dir})
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
      rescue StandardError => e
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
