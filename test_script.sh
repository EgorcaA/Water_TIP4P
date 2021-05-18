#!/bin/bash
mkdir test
cd test
for boxlength in 600  700 800 1000 1200 1500 ; do
mkdir box_$boxlength
cp ../sent.sh ../gauss_en.py  ../rr*  ../in.water ../write_lammps.py ../start_lammps.sh ./box_$boxlength
cd box_$boxlength
touch config.txt
echo box_length $boxlength > config.txt
python write_lammps.py
sbatch start_lammps.sh
cd ..
#sed -i "s/all create 3.0/all create $tempe/g" in.melt
#srun -N 1 -p RT --ntasks-per-node=8 -J lammps_agapov --comment="lammps $tempe"  ../lmp_mpi -in in.melt
#echo $tempe $(awk -f ../awk.sh log.lammps) >> ../Temp.txt
#touch rdf.txt
#tail -n 50 tmp.rdf > rdf.txt
#echo "$tempe" $(cat rdf.txt) >>../RDF.txt
#cd ..


done 
#gnuplot gnuplot.sh
#curl -s -X POST https://api.telegram.org/bot1636627501:AAHijZG6fBOt_3j_e6FdGjRPbQxSllX3yx0/sendMessage -d chat_id=719564532 -d text="we're done"
