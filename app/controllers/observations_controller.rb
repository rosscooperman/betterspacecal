class ObservationsController < ApplicationController

  def index
    respond_to do |format|
      format.html
      format.json { render json: Observation.all }
    end
  end
end
