require 'open-uri'

class Observation
  include HTTParty
  extend  Mongo

  class << self

    def mongo
      @mongo ||= MongoClient.new('localhost', 27017)['spacecalnyc']['schedules']
    end

    def search(params = {})
      mongo.find(mongo_params(params)).to_a
    end

    def mongo_params(params = {})
      params.inject({}) do |memo, (k, v)|
        begin
          memo[k] = send(:"filter_for_#{k}", v) unless v.blank?
        rescue NoMethodError
        end
        memo
      end
    end

    def filter_for_start(date)
      { '$gte' => Time.parse(date) }
    end

    def filter_for_end(date)
      { '$lte' => Time.parse(date) }
    end

    def filter_for_target(target)
      target
    end

    def filter_for_source(sources)
      { '$in' => sources }
    end
  end
end
