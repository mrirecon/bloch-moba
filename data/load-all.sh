#!/bin/bash

set -B

# Fig 04b
# Download datasets for single-shot inversion recovery
# following https://github.com/mrirecon/sms-t1-mapping

./load.sh 3969809 phantom-ss .
tar -xzvf phantom-ss.tgz


ZENODO_RECORD=7654462

# Fig 04cd, s04
for i in data_06_b1map data_06_irflash data_06_irbssfp_short
do

	./load-cfl.sh ${ZENODO_RECORD} ${i} .
done


# Fig 05b
for i in data_05b_b1map data_05b_kspace; do

	./load-cfl.sh ${ZENODO_RECORD} ${i} .
done


# s03
for i in  data_s03_b1map data_s03_irflash data_s03_irbssfp_2_5ms data_s03_irbssfp_2_1ms \
	data_s03_irbssfp_1_6ms data_s03_irbssfp_1_2ms data_s03_irbssfp_0_6ms data_s03_irbssfp_0_4ms
do

	./load-cfl.sh ${ZENODO_RECORD} ${i} .
done
