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
      # sample docker usage
      # sh %(docker create -p XXX:YYY --name storm source/storm:storm_version)
      # sh %(docker start storm)
    end

    task before_script: ['ci:common:before_script']

    task script: ['ci:common:script'] do
      this_provides = [
        'storm'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cleanup: ['ci:common:cleanup']
    # sample cleanup task
    # task cleanup: ['ci:common:cleanup'] do
    #   sh %(docker stop storm)
    #   sh %(docker rm storm)
    # end

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
