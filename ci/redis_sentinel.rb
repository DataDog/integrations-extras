require './ci/common'

def redis_sentinel_version
  ENV['FLAVOR_VERSION'] || '2.4.12'
end

def redis_sentinel_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/redis_sentinel_#{redis_sentinel_version}"
end

namespace :ci do
  namespace :redis_sentinel do |flavor|
    task before_install: ['ci:common:before_install']

    task install: ['ci:common:install'] do
      sh %(docker create -p 26379:26379 --name redis-sentinel joshula/redis-sentinel --sentinel announce-ip 1.2.3.4 --sentinel announce-port 26379)
      sh %(docker start redis-sentinel)
    end

    task before_script: ['ci:common:before_script']

    task script: ['ci:common:script'] do
      this_provides = [
        'redis_sentinel'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cache: ['ci:common:cache']

    task cleanup: ['ci:common:cleanup'] do
      sh %(docker stop $(docker ps -a -q))
    end

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
