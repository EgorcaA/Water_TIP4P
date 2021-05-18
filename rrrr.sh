for i in $(seq -f 'coords_%g.cfg' 0 1000 400000);
do
	paste coords_0.cfg $i | awk -f rrrr.awk >> sks_rrrr.txt 
done
