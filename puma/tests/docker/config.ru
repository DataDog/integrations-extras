require 'sinatra/base'

class MyApp < Sinatra::Base
  get "/" do
    "datadog-puma test server — see http://localhost:19293/stats?token=12345"
  end
end

run MyApp
