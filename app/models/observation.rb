require 'open-uri'

class Observation
  include HTTParty

  class << self

    def search(params = {})
      File.read(Rails.root.join('public', 'pyserver.json')).html_safe
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
