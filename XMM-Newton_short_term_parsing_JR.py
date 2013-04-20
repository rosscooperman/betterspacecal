text=urlopen("http://xmm2.esac.esa.int/external/xmm_sched/short_term_schedule.php").read()

from astropysics.coords import ICRSCoordinates, GalacticCoordinates

# this takes two strings in, one for the right ascension, and one for the declination
# this can be passed in with a range of formats. If it fails then it throws a 
def parseCoords(ra_str,dec_str):
  eq_coords = ICRSCoordinates(ra_str,dec_str)
	gal_coords = eq_coords.convert(GalacticCoordinates)
	return {"ra_float":eq_coords.ra.degrees, "dec_float":eq_coords.dec.degrees,\
			 "l_float":gal_coords.l.degrees, "b_float":gal_coords.b.degrees,\
			 "ra_str":eq_coords.ra.getHmsStr(), "dec_str":eq_coords.dec.getDmsStr()}

def getContent(line):
	end=line.split("<TD>")[1]
	val=end.split("</TD>")[0]
	return val.strip()

lines=text.split("\n")
for i in range(len(lines)):
	if 	'<TR ALIGN=CENTER >' in lines[i]:
		# in block of data.
		revn_ln=lines[i+1]
		tel_id_ln=lines[i+2]					# The id of the observation
		target_name=getContent(lines[i+3])		# The name of the target
		ra_str=getContent(lines[i+4])
		dec_str=getContent(lines[i+5])
		pa_st_ln=lines[i+6]
		start_string=getContent(lines[i+7])		# string designating the date time - need to parse this to a datetime
		end_string=getContent(lines[i+8])		# string designating the date time - need to parse this to a datetime
		
		coords=parseCoords(ra_str,dec_str)
	else:
		continue

