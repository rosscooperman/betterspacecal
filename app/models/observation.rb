require 'open-uri'

class Observation
  include HTTParty
  extend  Mongo

  class << self

    def mongo
      @mongo ||= MongoClient.new('localhost', 27017)['spacecalnyc']
    end

    def mongo_schedules
      @mongo_schedules ||= mongo['schedules']
    end

    def mongo_images
      @mongo_images ||= mongo['target_images']
    end

    def search(params = {})
      begin
        mongo_schedules.find(mongo_params(params)).to_a.tap do |results|
          results.map do |result|
            images = mongo_images.find_one("_id" => result['target'])
            result.merge!(images: images ? images["images"] : [])
          end
        end
      rescue
        File.read(Rails.root.join('test', 'fixtures', 'data.json')).html_safe
      end
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
      { :'$gte' => Time.parse(date).at_midnight }
    end

    def filter_for_end(date)
      { :'$lt' => Time.parse(date).tomorrow.at_midnight }
    end

    def filter_for_target(target)
      target
    end

    def filter_for_source(sources)
      { :'$in' => sources }
    end
  end
end
