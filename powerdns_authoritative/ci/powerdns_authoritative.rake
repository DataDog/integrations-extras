require 'ci/common'

def powerdns_authoritative_version
  ENV['FLAVOR_VERSION'] || 'latest'
end

def powerdns_authoritative_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/powerdns_authoritative_#{powerdns_authoritative_version}"
end

namespace :ci do
  namespace :powerdns_authoritative do |flavor|
    task before_install: ['ci:common:before_install']

    task install: ['ci:common:install'] do
      use_venv = in_venv
      install_requirements('powerdns_authoritative/requirements.txt',
                           "--cache-dir #{ENV['PIP_CACHE']}",
                           "#{ENV['VOLATILE_DIR']}/ci.log", use_venv)
      # sample docker usage
      # sh %(docker create -p XXX:YYY --name powerdns_authoritative source/powerdns_authoritative:powerdns_authoritative_version)
      # sh %(docker start powerdns_authoritative)
    end

    task before_script: ['ci:common:before_script']

    task script: ['ci:common:script'] do
      this_provides = [
        'powerdns_authoritative'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cleanup: ['ci:common:cleanup']
    # sample cleanup task
    # task cleanup: ['ci:common:cleanup'] do
    #   sh %(docker stop powerdns_authoritative)
    #   sh %(docker rm powerdns_authoritative)
    # end

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
