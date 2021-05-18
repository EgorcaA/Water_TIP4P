#!/bin/sh

#SBATCH -p RT_study
#SBATCH --comment=visualisation
#SBATCH -N 1
##SBATCH --exclusive
#SBATCH --ntasks-per-node=8
#SBATCH --time=60

ovitos -nt 8 ovv_vis.py
curl -s -X POST https://api.telegram.org/bot1636627501:AAHijZG6fBOt_3j_e6FdGjRPbQxSllX3yx0/sendMessage -d chat_id=719564532 -d text="we're done with visualisation"

