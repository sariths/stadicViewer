rcontrib -I -aa 0.1 -ar 150 -ab 3 -dc 1 -ad 10000 -as 256 -dr 2 -dj 0 -dp 1 -ds 0.2 -dt 0.5 -lr 6 -lw 1e-009 -st 0.15 -e MF:1 -f reinhart.cal -b rbin -bn Nrbins -m sky_glow -faa C:/STADIC/res/intermediateData/Classroom1_South_set1_std.oct < C:/STADIC/data/Classroom1_AutoGen.pts > C:/STADIC/res/intermediateData/Classroom1_South_set1_1k_std.dc

## Create the suns octree here

rcontrib -I -aa 0.1 -ar 150 -dc 1 -ad 10000 -as 256 -dr 2 -dj 0 -dp 1 -ds 0.2 -dt 0.5 -lr 6 -lw 1e-009 -st 0.15 -ab 1 -e MF:1 -f reinhart.cal -b rbin -bn Nrbins -m sky_glow -faa C:/STADIC/res/intermediateData/Classroom1_South_set1_std.oct < C:/STADIC/data/Classroom1_AutoGen.pts > C:/STADIC/res/intermediateData/Classroom1_South_set1_1d_std.dc

rcontrib -I -aa 0.1 -ar 150 -dc 1 -ad 10000 -as 256 -dr 2 -dj 0 -dp 1 -ds 0.2 -dt 0.5 -lr 6 -lw 1e-009 -st 0.15 -ab 0 -e MF:4 -f reinhart.cal -b rbin -bn Nrbins -m solar -faa C:/STADIC/res/intermediateData/Classroom1_South_sun_set1_std.oct < C:/STADIC/data/Classroom1_AutoGen.pts > C:/STADIC/res/intermediateData/Classroom1_South_set1_d_std.dc

gendaymtx -m 4 -d -5 0.533 C:/STADIC/data/StateCollegePennStateSu_USA.wea > C:/STADIC/res/intermediateData/Classroom1_South_set1_d_std.smx

gendaymtx -m 1 -c 1 1 1 C:/STADIC/data/StateCollegePennStateSu_USA.wea > C:/STADIC/res/intermediateData/Classroom1_South_set1_k_std.smx

gendaymtx -m 1 -d C:/STADIC/data/StateCollegePennStateSu_USA.wea > C:/STADIC/res/intermediateData/Classroom1_South_set1_kd_std.smx

dctimestep C:/STADIC/res/intermediateData/Classroom1_South_set1_1k_std.dc C:/STADIC/res/intermediateData/Classroom1_South_set1_k_std.smx | rcollate -ho -oc 1 > C:/STADIC/res/intermediateData/Classroom1_South_set1_sky_std.txt

dctimestep C:/STADIC/res/intermediateData/Classroom1_South_set1_d_std.dc C:/STADIC/res/intermediateData/Classroom1_South_set1_d_std.smx | rcollate -ho -oc 1 > C:/STADIC/res/intermediateData/Classroom1_South_set1_sun_std.txt

dctimestep C:/STADIC/res/intermediateData/Classroom1_South_set1_1d_std.dc C:/STADIC/res/intermediateData/Classroom1_South_set1_kd_std.smx | rcollate -ho -oc 1 > C:/STADIC/res/intermediateData/Classroom1_South_set1_sunPatch_std.txt

rlam C:/STADIC/res/intermediateData/Classroom1_South_set1_sky_std.txt C:/STADIC/res/intermediateData/Classroom1_South_set1_sunPatch_std.txt C:/STADIC/res/intermediateData/Classroom1_South_set1_sun_std.txt | rcalc -e r=$1-$4+$7;g=$2-$5+$8;b=$3-$6+$9 -e ill=179*(.265*r+.670*g+.065*b) -e $1=floor(ill+.5) > C:/STADIC/res/intermediateData/Classroom1_South_set1_ill_std.tmp

rlam C:/STADIC/res/intermediateData/Classroom1_South_set1_sky_std.txt C:/STADIC/res/intermediateData/Classroom1_South_set1_sunPatch_std.txt C:/STADIC/res/intermediateData/Classroom1_South_set1_sun_std.txt | rcalc -e r=$1-$4+$7;g=$2-$5+$8;b=$3-$6+$9 -e ill=179*(.265*r+.670*g+.065*b) -e $1=floor(ill+.5) > C:/STADIC/res/intermediateData/Classroom1_South_set1_ill_std.tmp

