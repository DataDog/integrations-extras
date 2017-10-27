require 'ci/common'

def storm_version
  ENV['FLAVOR_VERSION'] || 'latest'
end

def storm_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/storm_#{storm_version}"
end

namespace :ci do
  namespace :storm do |flavor|
    task before_install: ['ci:common:before_install']

    task install: ['ci:common:install'] do
      # Build the storm jar for the sample topology
      sh %(docker build -t topology-maker $(pwd)/storm/ci/.)
      sh %(docker run -d --name topology-build --rm -v $(pwd):/artifacts topology-maker)
      sh %(docker cp topology-build:/topology.jar $(pwd))
      sh %(docker stop topology-build)
      sh %(docker rmi -f topology-maker)
      # Start the storm cluster
      sh %(docker run -d --restart always --name storm-zookeeper zookeeper:3.4)
      sh %(docker run -d --restart always -p 6627:6627 --name storm-nimbus --link storm-zookeeper:zookeeper
        storm:1.1 storm nimbus)
      sh %(docker run -d --restart always --name storm-supervisor --link storm-zookeeper:zookeeper
        --link storm-nimbus:nimbus storm:1.1 storm supervisor)
      sh %(docker run -d -p 9005:8080 --restart always --name storm-ui --link storm-nimbus:nimbus storm:1.1 storm ui)
      # Wait for storm to start...
      sh %(sleep 60)
      # Deploy the basic WordCountTopology we created earlier.
      sh %(docker run --link storm-nimbus:nimbus -it --rm -v $(pwd)/topology.jar:/topology.jar storm:1.1 storm jar
        /topology.jar org.apache.storm.starter.WordCountTopology topology)
    end

    task before_script: ['ci:common:before_script']

    task script: ['ci:common:script'] do
      this_provides = [
        'storm'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cleanup: ['ci:common:cleanup'] do
      sh %(rm $(pwd)/topology.jar)
      sh %(docker stop storm-ui)
      sh %(docker rm storm-ui)
      sh %(docker stop storm-supervisor)
      sh %(docker rm storm-supervisor)
      sh %(docker stop storm-nimbus)
      sh %(docker rm storm-nimbus)
      sh %(docker stop storm-zookeeper)
      sh %(docker rm storm-zookeeper)
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
