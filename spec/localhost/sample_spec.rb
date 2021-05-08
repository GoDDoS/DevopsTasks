require 'spec_helper'

describe package('postgresql') do
	it { should be_installed.with_version('12.6') }
end

describe package('python3-pip') do
	it { should be_installed.with_version('20.0.2') }
end

describe package('python3-tk') do
	it { should be_installed.with_version('8.6') }
end

describe package('psycopg2-binary') do
	it {should be_installed.by('pip3').with_version('2.8.6') }
end
