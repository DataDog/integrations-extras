require 'ci/common'

def neo4j_version
  ENV['FLAVOR_VERSION'] || 'latest'
end

def neo4j_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/data_#{neo4j_version}"
end

container_name = 'dd-test-neo4j'

namespace :ci do
  namespace :neo4j do |flavor|
    task before_install: ['ci:common:before_install'] do
      `docker kill $(docker ps -q --filter name=dd-test-neo4j) || true`
      `docker rm $(docker ps -aq --filter name=dd-test-neo4j) || true`
    end

    task install: ['ci:common:install'] do
      use_venv = in_venv
      install_requirements("--cache-dir #{ENV['PIP_CACHE']}",
                           "#{ENV['VOLATILE_DIR']}/ci.log", use_venv)
      sh %(docker run --name #{container_name} --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data --volume=$HOME/neo4j/logs:/logs neo4j:3.1.1 )
    end

    task before_script: ['ci:common:before_script'] do
      Wait.for 7474
      count = 0
      logs = `docker logs dd-test-neo4j 2>&1`
      puts 'Waiting for Neo4j to come up'
      until count == 60 || logs.include? 'Remote interface available at'
        sleep_for 2
        logs = `docker logs dd-test-neo4j 2>&1`
        count += 1
      end
      if logs.include? 'Remote interface available at'
        puts 'Neo4j is up!'
      end

    end

    task script: ['ci:common:script'] do
      this_provides = [
        'neo4j'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cleanup: ['ci:common:cleanup'] do
      `docker kill $(docker ps -q --filter name=dd-test-neo4j) || true`
      `docker rm $(docker ps -aq --filter name=dd-test-neo4j) || true`
    end

    task :execute do
      exception = nil
      begin
        %w(before_install install before_script).each do |u|
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
