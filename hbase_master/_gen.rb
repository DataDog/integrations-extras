#! /usr/bin/ruby
#  Description
# --------------
# This helper script read configuration file '_metrics.yml' and generate
#  - _metadata.csv
#  - _conf.yaml.example
# by extracting description from actual hbase web console
#
#  How to use
# --------------
# 1. start hbase cluster in pseudo distributed mode: `docker-compose -f ci/resources/docker-compose-hbase.yaml up -d`
# 2. run this script `./_gen.rb`
# 3. you will see two files '_metadata.csv', '_conf.yaml.example'

require 'yaml'
require 'json'
require 'csv'
require 'erb'

METRICS_FILENAME='_metrics.yml'
OUT_CONFIG_FILENAME='_conf.yaml.example'
OUT_METADATA_FILENAME='_metadata.csv'
ORIENTATION = "0"

MANIFEST = JSON.load(File.new('manifest.json',"r"))
jmx_dump = JSON.load(`curl -s http://localhost:60010/jmx?description=true`)["beans"]
metrics = YAML.load(File.new(METRICS_FILENAME, "r"))

# metrics data decorators
# complete required fields or optional fields from dumped attribut from hbase
def decorate_descrption(metric, dumped_attribute)
  if Hash === dumped_attribute && dumped_attribute.has_key?("description")
    metric["description"] = dumped_attribute["description"]
  else
    metric["description"] = ""
  end
end

def decorate_unit(metric)
  if !metric.has_key?("unit_name") then
    if metric["alias"].include?("size") || metric["description"].include?("in bytes") then
      metric["unit_name"] = "byte"
    elsif (metric["alias"].include?("percent") || metric["description"].include?("percent")) && !metric["alias"].include?("percentile")
      metric["unit_name"] = "percent"
    elsif metric["alias"].include?("time") || metric["description"].include?("time")
      metric["unit_name"] = "millisecond"
    else
      metric["unit_name"] = ""
    end
  end
end

def decorate_required_fields(metric)
  metric["integration"] = MANIFEST["name"]
  metric["metric_name"] = metric["alias"]
  # operation will be fixed value
  metric["orientation"] = ORIENTATION
  # default metric_type is gauge
  if !metric.has_key?("metric_type")
    metric["metric_type"] = "gauge"
  end
end

def decorate_optional_fields(metric, attribute)
  decorate_descrption(metric,attribute)
  decorate_unit(metric)
end

metadata_keys = %w{metric_name metric_type interval unit_name per_unit_name description orientation integration short_name}
metadata_header = CSV::Row.new(metadata_keys,[],true)
metadata = CSV::Table.new([metadata_header])
metrics.each do |m|
  decorate_required_fields(m)
  mbean = jmx_dump.find{|o| o["name"] == m["bean"]}
  if mbean.has_key?(m["attribute"])
    decorate_optional_fields(m, mbean[m["attribute"]])
  else
    decorate_optional_fields(m, "")
  end

  r = CSV::Row.new([],[],false)
  metadata_keys.each do |k|
    if m.has_key?(k)
      r << { k => m[k] }
    else
      r << { k => "" }
    end
  end
  metadata << r
end

File.open(OUT_METADATA_FILENAME, 'w').puts metadata.to_csv

conf_template = ERB.new(<<-HEREDOC
instances:
  - host: localhost
    port: 10101 # This is the JMX port on which HBase Master exposes its metrics (usually 10101)
    tags:
      hbase: master
      # env: stage
      # newTag: test
    # user: username
    # password: password
    # process_name_regex: .*process_name.* # Instead of specifying a host and port or jmx_url, the agent can connect using the attach api.
    #                                      # This requires the JDK to be installed and the path to tools.jar to be set below.
    # tools_jar_path: /usr/lib/jvm/java-7-openjdk-amd64/lib/tools.jar # To be set when process_name_regex is set
    # name: hbase_master
    # # java_bin_path: /path/to/java # Optional, should be set if the agent cannot find your java executable
    # # java_options: "-Xmx200m -Xms50m" # Optional, Java JVM options
    # # trust_store_path: /path/to/trustStore.jks # Optional, should be set if ssl is enabled
    # # trust_store_password: password

init_config:
  is_jmx: true

  # Metrics collected by this check. You should not have to modify this.
  conf:<% bean_metrics.each do |bean_name, metrics| %>
    - include:
        domain: Hadoop
        bean:
         - <%= bean_name %>
        attribute:<% metrics.each do |m| %><%if m.has_key?("description") && m["description"] != "" %>
          # <%= m["description"] %><% end %>
          <%= m["attribute"] %>:
            metric_type: <%= m["metric_type"] %>
            alias: <%= m["alias"] %><%if m.has_key?("values") %>
            values: <%= m["values"] %><% end %><% end %>
<% end %>
HEREDOC
)

bean_metrics=metrics.group_by {|m| m["bean"] }
conf_rendered=conf_template.result(binding)
File.open(OUT_CONFIG_FILENAME, 'w').puts conf_rendered
