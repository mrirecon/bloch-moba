#!/bin/bash

set -euo pipefail
set -x

# Set default to IR bSSFP
MODEL="irbssfp"

# Folder for temporary stuff
[ -d tmp ] && rm -r tmp
mkdir tmp

# Folder for results
RESULTS=${MODEL}
[ -d ${RESULTS} ] && rm -r ${RESULTS}
mkdir ${RESULTS}


TR=0.004
TE=0.002
TRF=0.00001
PREP=0.00002
DINV=0
FA=45
REP=1000
BWTP=4
T1=1.25
T2=0.045
ODE_TOL=1E-6


# Simulation with SA

bart sim --ODE --seq IR-BSSFP,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${PREP},Trf=${TRF},FA=${FA},BWTP=${BWTP},isp=${DINV} --other ode-tol=${ODE_TOL} -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/_s tmp/_sens


# extract desired parameter sensitivities
bart slice 4 0 tmp/_sens ${RESULTS}/sens_R1
bart slice 4 2 tmp/_sens ${RESULTS}/sens_R2
bart slice 4 3 tmp/_sens ${RESULTS}/sens_B1


# Difference Quotient

H=(1.0025 1.005 1.01 1.03 1.1)

for h in "${H[@]}"
do
        echo ${h}
        # R1

        ## Simulation without and with small distortion
        bart sim --ODE --seq IR-BSSFP,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${PREP},Trf=${TRF},FA=${FA},BWTP=${BWTP},isp=${DINV} --other ode-tol=${ODE_TOL} -1 $(echo ${T1} ${h} | awk '{printf "%f\n",$1*$2}'):$(echo ${T1} ${h} | awk '{printf "%f\n",$1*$2}'):1 -2 ${T2}:${T2}:1 tmp/_s2

        ## Estimate difference quotient
        bart saxpy -- -1 tmp/_s{2,} tmp/_diff  # f(x1)-f(x2)

        DIFF=$(echo ${T1} ${h} | awk '{printf "%f\n", $1*(1-$2)}') # x1-x2

        # Devide by x1-x2 to estimate difference quotient
        bart scale -- $(echo ${DIFF} | awk '{printf "%f\n",1/$1}') tmp/_diff tmp/_grad

        bart scale -- $(echo ${T1} | awk '{printf "%f\n",-($1*$1)}') tmp/_grad tmp/grad_R1_$(printf ${h} | sed -e 's/\./_/')

        # R2

        ## Simulation without and with small distortion
        bart sim --ODE --seq IR-BSSFP,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${PREP},Trf=${TRF},FA=${FA},BWTP=${BWTP},isp=${DINV} --other ode-tol=${ODE_TOL} -1 ${T1}:${T1}:1 -2 $(echo ${T2} ${h} | awk '{printf "%f\n",$1*$2}'):$(echo ${T2} ${h} | awk '{printf "%f\n",$1*$2}'):1 tmp/_s2

        ## Estimate difference quotient
        bart saxpy -- -1 tmp/_s{2,} tmp/_diff  # f(x1)-f(x2)

        DIFF=$(echo ${T2} ${h} | awk '{printf "%f\n", $1*(1-$2)}') # x1-x2

        # Devide by x1-x2 to estimate difference quotient
        bart scale -- $(echo ${DIFF} | awk '{printf "%f\n",1/$1}') tmp/_diff tmp/_grad

        # Scale to compensate for T2 <-> R2 differences
        bart scale -- $(echo ${T2} | awk '{printf "%f\n",-($1*$1)}') tmp/_grad tmp/grad_R2_$(printf ${h} | sed -e 's/\./_/')


        # B1

        ## Simulation without and with small distortion
        bart sim --ODE --seq IR-BSSFP,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${PREP},Trf=${TRF},FA=$(echo ${FA} ${h} | awk '{printf "%f\n",$1*$2}'),BWTP=${BWTP},isp=${DINV} --other ode-tol=${ODE_TOL} -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/_s2

        ## Estimate difference quotient
        bart saxpy -- -1 tmp/_s{2,} tmp/_diff  # f(x1)-f(x2)

        DIFF=$(echo ${FA} ${h} | awk '{printf "%f\n", $1*(1-$2)}') # x1-x2

        bart scale -- $(echo 1 ${DIFF} | awk '{printf "%f\n",$1/$2}') tmp/_diff tmp/_grad

        # Scale to convert dFA -> dB1
        bart scale -- $(echo 1 ${FA} | awk '{printf "%f\n",1/($1/$2)}') tmp/_grad tmp/grad_B1_$(printf ${h} | sed -e 's/\./_/')

done

bart join 6 $(ls tmp/grad_R1_*.cfl | sed -e 's/\.cfl//') ${RESULTS}/grad_R1
bart join 6 $(ls tmp/grad_R2_*.cfl | sed -e 's/\.cfl//') ${RESULTS}/grad_R2
bart join 6 $(ls tmp/grad_B1_*.cfl | sed -e 's/\.cfl//') ${RESULTS}/grad_B1

rm ${RESULTS}/h.txt || :
touch ${RESULTS}/h.txt
echo "${H[@]}" >> ${RESULTS}/h.txt

# Remove temporary stuff
[ -d tmp ] && rm -r tmp