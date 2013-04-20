require 'open-uri'

class Observation
  include HTTParty
  extend  Mongo

  class << self

    def mongo
      @mongo ||= MongoClient.new('localhost', 27017)['spacecalnyc']['schedules']
    end

    def search(params = {})
      mongo.find.to_a
    end

    def query_string(params = {})
      params.map do |k, v|
        begin
          "#{k}=" + send(:"filterable_#{k}", v)
        rescue NoMethodError
        end
      end.compact.join('&')
    end

    def filterable_start(date)
      filterable_date(date)
    end

    def filterable_end(date)
      filterable_date(date)
    end

    def filterable_date(date)
      URI::encode(date.to_s)
    end
  end
end
