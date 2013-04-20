class Observation
  include HTTParty

  attr_accessor :source, :target, :ra, :dec, :ra_str, :dec_str, :b, :l, :end, :start

  def initialize(attributes = {})
    attributes.each do |k, v|
      begin
        send(:"#{k}=", v)
      rescue NoMethodError
      end
    end
  end

  def self.all
    json = File.read(Rails.root.join('public', 'pyserver.json'))
    observations = JSON.parse(json)
    observations.map do |observation|
      new(observation)
    end
  end

  def end=(val)
    @end = val.is_a?(String) ? Time.zone.parse(val) : val
  end

  def start=(val)
    @start = val.is_a?(String) ? Time.zone.parse(val) : val
  end
end
