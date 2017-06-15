require 'ci/common'

def snmpwalk_version
  ENV['FLAVOR_VERSION'] || 'latest'
end

def snmpwalk_rootdir
  "#{ENV['INTEGRATIONS_DIR']}/snmpwalk_#{snmpwalk_version}"
end

def resources_path
  base = ENV['TRAVIS_BUILD_DIR'] || ENV['CI_BUILD_DIR']
  base.to_s + '/snmpwalk/ci/resources'
end

namespace :ci do
  namespace :snmpwalk do |flavor|
    task before_install: ['ci:common:before_install']

    task :install do
      Rake::Task['ci:common:install'].invoke('snmpwalk')
      sh %(docker run -d -v #{resources_path}:/etc/snmp/ \
           --name dd-test-snmpwalk -p 11111:161/udp \
            polinux/snmpd -c /etc/snmp/snmpd.conf)
      sleep_for 5
    end

    task before_script: ['ci:common:before_script']

    task script: ['ci:common:script'] do
      this_provides = [
        'snmpwalk'
      ]
      Rake::Task['ci:common:run_tests'].invoke(this_provides)
    end

    task before_cache: ['ci:common:before_cache']

    task cleanup: ['ci:common:cleanup'] do
      sh %(docker stop dd-test-snmpwalk)
      sh %(docker rm dd-test-snmpwalk)
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
