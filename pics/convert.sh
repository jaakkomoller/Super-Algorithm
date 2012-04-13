#! /bin/sh
#    pstogif
#
# Call it by putting the .ps file name as first argument but without the
# ".ps" extension.  Ex:  for "Intro_Tbl.ps" use "pstogif Intro_Tbl"
#
gs -r72x72  -sDEVICE=ppmraw -sOutputFile=$1.ppm << endinput
   ($1.ps) run
endinput
 
pnmcrop < $1.ppm | ppmtogif > $1.gif
rm *.ppm
