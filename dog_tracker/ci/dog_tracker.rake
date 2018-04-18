require 'ci/common'

def dog_tracker_version
  ENV['FLAVOR_VERSION'] || 'latest'
end

def dog_tracker_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/dog_tracker_#{dog_tracker_version}"
end

namespace :ci do
  namespace :dog_tracker do |flavor|
    task before_install: ['ci:common:before_install']

    task before_script: ['ci:common:before_script']

    task :install do
      Rake::Task['ci:common:install'].invoke('dog_tracker')
    end

    task script: ['ci:common:script'] do
      this_provides = [
        'dog_tracker'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

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
