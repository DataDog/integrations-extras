workers Integer(ENV.fetch('WORKERS', 2))
threads_count = Integer(ENV.fetch('THREADS', 5))
threads threads_count, threads_count

rackup DefaultRackup
port ENV.fetch('PORT', 30001)
environment ENV.fetch('RACK_ENV', 'development')

activate_control_app 'tcp://0.0.0.0:19293', { auth_token: '12345' }
