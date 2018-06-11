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

module GnatsdDocker
  def volumes
    "--volume=#{gnatsd_streaming_temp_dir}/data:/usr/share/nats/data"
  end

  def publish
    '--publish=4222:4222 --publish=8222:8222'
  end

  def store_mount
    '-store file -dir /usr/share/nats/data'
  end

  def primary_routes
    "-cluster nats://#{container_name}-primary:5222 -routes nats://#{container_name}-secondary:5222 -ft_group failover"
  end

  def secondary_routes
    "-cluster nats://#{container_name}-secondary:5222 -routes nats://#{container_name}-primary:5222 -ft_group failover"
  end

  def primary
    "nats-streaming:0.9.2 #{store_mount} #{primary_routes} -m 8222"
  end

  def secondary
    "nats-streaming:0.9.2 #{store_mount} #{secondary_routes} -m 8223"
  end

  def container_name
    'dd-test-gnatsd-streaming'
  end
end

container_name = 'dd-test-gnatsd-streaming'

namespace :ci do
  namespace :gnatsd_streaming do |flavor|
    task before_install: ['ci:common:before_install'] do
      Rake::Task['ci:gnatsd_streaming:cleanup'].invoke
      self.extend(GnatsdDocker)

      sh %(docker network create nats)

      # Set up NATS Streaming
      sh %(docker run -d --name #{container_name}-primary #{publish} --network nats #{volumes} #{primary})
      # these have to come up in order so sleep for a second to make sure that
      # the primary is always the active server
      sleep 1
      sh %(docker run -d --name #{container_name}-secondary #{volumes} --publish=8223:8223 #{secondary})

      # Set up Streaming channels
      benchmark = "/go/src/github.com/nats-io/go-nats-streaming/examples/stan-bench/main.go -s nats://#{container_name}-primary:4222 -n 10"
      sh %(docker run -d --name #{container_name}-channels --network nats golang:1.10.0 bash -l -c "sleep infinity")
      sh %(docker exec #{container_name}-channels go get -v github.com/nats-io/go-nats-streaming)
      sh %(docker exec #{container_name}-channels go run #{benchmark} test.channel1)
      sh %(docker exec #{container_name}-channels go run #{benchmark} test.channel2)
      sh %(docker exec #{container_name}-channels go run #{benchmark} test.channel3)
    end

    task :install do
      Rake::Task['ci:common:install'].invoke('gnatsd_streaming')
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
      sh %(docker stop #{container_name}-primary #{container_name}-secondary #{container_name}-channels || true)
      sh %(docker rm #{container_name}-primary #{container_name}-secondary #{container_name}-channels || true)
      sh %(docker network rm nats || true)
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
