class Observation
  include HTTParty

  attr_accessor :target

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
end
