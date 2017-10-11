require 'ci/common'

def neo4j_version
  ENV['FLAVOR_VERSION'] || 'latest'
end

def neo4j_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/data_#{neo4j_version}"
end

def temp_dir
  ENV['VOLATILE_DIR'] + '/neo4j'
end

container_name = 'dd-test-neo4j'

namespace :ci do
  namespace :neo4j do |flavor|
    task before_install: ['ci:common:before_install'] do
      sh %(docker kill #{container_name} || true)
      sh %(docker rm #{container_name} || true)
    end

    task install: ['ci:common:install'] do
      Rake::Task['ci:common:install'].invoke('neo4j')
      volumes = "--volume=#{temp_dir}/data:/data \
      --volume=#{temp_dir}/logs:/logs"
      publish = '--publish=7474:7474 --publish=7687:7687'
      sh %(docker run -d --name #{container_name} #{volumes} #{publish} neo4j:3.2.3)
    end

    task before_script: ['ci:common:before_script'] do
      Wait.for 7474
      count = 0
      logs = `docker logs dd-test-neo4j 2>&1`
      puts 'Waiting for Neo4j to come up'
      until count == 60 || logs.include?('Remote interface available at')
        sleep_for 2
        logs = `docker logs dd-test-neo4j 2>&1`
        count += 1
      end
      logs.include?('Remote interface available at') && puts('Neo4j is up!')
      sh %(curl -H "Content-Type: application/json" \
          -X POST -d '{"password":"dog"}' -u neo4j:neo4j \
          http://localhost:7474/user/neo4j/password)
    end

    task script: ['ci:common:script'] do
      this_provides = [
        'neo4j'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cleanup: ['ci:common:cleanup'] do
      sh %(docker kill #{container_name} || true)
      sh %(docker rm #{container_name} || true)
      sh %(rm -rf #{temp_dir})
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
