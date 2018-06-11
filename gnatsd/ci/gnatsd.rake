require 'ci/common'

def gnatsd_version
  ENV['FLAVOR_VERSION'] || 'latest'
end

def gnatsd_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/gnatsd_#{gnatsd_version}"
end

def gnatsd_temp_dir
  ENV['VOLATILE_DIR'] + '/gnatsd'
end

container_name = 'dd-test-gnatsd'

namespace :ci do
  namespace :gnatsd do |flavor|
    task before_install: ['ci:common:before_install'] do
      Rake::Task['ci:gnatsd:cleanup'].invoke
    end

    task :install do
      Rake::Task['ci:common:install'].invoke('gnatsd')
      volumes = "--volume=#{gnatsd_temp_dir}/data:/usr/share/nats/data"
      publish = '--publish=4222:4222 --publish=8222:8222'
      cluster = '-cluster=nats://0.0.0.0:5222'

      # Set up NATS cluster
      sh %(docker run -d --name #{container_name}-serverA --publish=5222:5222 nats:1.1.0 #{cluster})

      sh(%(docker run -d --name #{container_name}-serverB --link #{container_name}-serverA ) +
         %(#{volumes} #{publish} nats:1.0.4 -m 8222 #{cluster} -routes=nats://#{container_name}-serverA:5222))

      # Set up NATS subscribers
      sh %(docker run -d --name #{container_name}-subscriber --link #{container_name}-serverB ruby:2.4.3 bash -l -c "sleep infinity")
      sh %(docker exec #{container_name}-subscriber bash -l -c "gem install nats --version 0.8.4")
      sh %(docker exec -d #{container_name}-subscriber bash -l -c "NATS_CONNECTION_NAME=foo-sub ) +
         %(/usr/local/bundle/bin/nats-sub foo -s http://#{container_name}-serverB:4222")
      sh %(docker exec -d #{container_name}-subscriber bash -l -c "/usr/local/bundle/bin/nats-sub bar -s http://#{container_name}-serverB:4222")

      # Publish a few example events
      sh %(docker exec #{container_name}-subscriber bash -l -c "/usr/local/bundle/bin/nats-pub foo "foo1" -s http://#{container_name}-serverB:4222")
      sh %(docker exec #{container_name}-subscriber bash -l -c "/usr/local/bundle/bin/nats-pub foo "foo2" -s http://#{container_name}-serverB:4222")
      sh %(docker exec #{container_name}-subscriber bash -l -c "/usr/local/bundle/bin/nats-pub bar "bar1" -s http://#{container_name}-serverB:4222")
    end

    task before_script: ['ci:common:before_script']

    task script: ['ci:common:script'] do
      this_provides = [
        'gnatsd'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cleanup: ['ci:common:cleanup'] do
      sh %(docker stop #{container_name}-serverA #{container_name}-serverB #{container_name}-subscriber || true)
      sh %(docker rm #{container_name}-serverA #{container_name}-serverB #{container_name}-subscriber || true)
      sh %(rm -rf #{gnatsd_temp_dir})
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
