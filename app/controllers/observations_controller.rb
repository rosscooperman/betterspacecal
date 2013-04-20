class ObservationsController < ApplicationController

  def index
    @observations = Observation.all
  end
end
