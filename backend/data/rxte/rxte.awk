/^2.*START$/ { start=$1; id=$4; }
/SOURCE/ { target=$2 }
/TARGET/ {ra=substr($2,4); dec=substr($3,5)}
/^2.*END$/ { end=$1; print start"\t"end"\t"target"\t"ra"\t"dec"\t"id"\t"}
