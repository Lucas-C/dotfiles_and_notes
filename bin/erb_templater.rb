#!/bin/env ruby

# USAGE: ./erb_templater --key-prefix @ $params.yaml < $template.erb

require 'erubis'
require 'yaml'

prefix = ''
if ARGV[0] == "--key-prefix"
    ARGV.shift
    prefix = ARGV.shift
end

params = YAML.load_file(ARGV[0])
params = Hash[params.map { |h|
    pair = h.to_a[0]
    [prefix+pair[0], pair[1]]
}]

puts Erubis::Eruby.new($stdin.read).result(params)