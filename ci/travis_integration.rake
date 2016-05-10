require './ci/common'

def travis_integration_version
  ENV['FLAVOR_VERSION'] || '2.4.12'
end

def travis_integration_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/travis_integration_#{travis_integration_version}"
end

namespace :ci do
  namespace :travis_integration do |flavor|
    task before_install: ['ci:common:before_install']

    task install: ['ci:common:install'] do
      use_venv = in_venv
      install_requirements('travis_integration/requirements.txt',
                           "--cache-dir #{ENV['PIP_CACHE']}",
                           "#{ENV['VOLATILE_DIR']}/ci.log", use_venv)
      # sample docker usage
      sh %(docker create -p 3307:3306 --name mysql -e MYSQL_ROOT_PASSWORD=foo mysql:latest)
      sh %(docker start mysql)
    end

    task before_script: ['ci:common:before_script']

    task script: ['ci:common:script'] do
      this_provides = [
        'travis_integration'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cache: ['ci:common:cache']

    task cleanup: ['ci:common:cleanup']
    # sample cleanup task
    # task cleanup: ['ci:common:cleanup'] do 
    #   sh %(docker stop travis_integration)
    #   sh %(docker rm travis_integration)
    # end

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
