class ObservationsController < ApplicationController

  def index
    respond_to do |format|
      format.html
      format.json { render json: Observation.search(params) }
    end
  end
end
