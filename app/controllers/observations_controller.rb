class ObservationsController < ApplicationController

  def index
    respond_to do |format|
      format.html
      format.json { render json: Observation.search(params) }
    end
  end

  def export
    headers['Content-Disposition'] = "attachment; filename=\"export.txt\""

    observations = Observation.search(params).map do |o|
      id = id.to_s.split('|'); id.shift; id = id.join('')
      "#{o['source']}\t#{id}\t#{o['target']}\t#{o['start'].to_i}\t#{o['end'].to_i}\t#{o['l']}\t#{o['b']}\t#{o['ra']}\t#{o['dec']}\t#{o['ra_str']}\t#{o['dec_str']}"
    end

    header = "satellite_name\tobservation_id\ttarget_name\tutc_start_seconds\tutc_end_seconds\tl\tb\tra\tdec\tra_str\tdec_str"
    render text: header + "\n" + observations.join("\n")
  end
end
