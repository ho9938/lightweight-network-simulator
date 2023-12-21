#!/bin/bash

if [ ! -d test/data ] ; then
    mkdir test/data
fi

for idx in {1..100}
do
    # python3 simulator.py $net$idx --direct > ./test/data/$net$idx.log
    for pol in rr fcfs of
    do
        # python3 simulator.py knc_9_$idx'_'$pol --direct > ./test/data/knc_9_$idx'_'$pol.log
        # python3 simulator.py knc_27_$idx'_'$pol --direct > ./test/data/knc_27_$idx'_'$pol.log
        # python3 simulator.py knc_64_$idx'_'$pol --direct > ./test/data/knc_64_$idx'_'$pol.log
        # python3 simulator.py knc_81_$idx'_'$pol --direct > ./test/data/knc_81_$idx'_'$pol.log
        # python3 simulator.py knc_256_$idx'_'$pol --direct > ./test/data/knc_256_$idx'_'$pol.log
        # python3 simulator.py ccc_8_$idx'_'$pol --direct > ./test/data/ccc_8_$idx'_'$pol.log
        # python3 simulator.py ccc_24_$idx'_'$pol --direct > ./test/data/ccc_24_$idx'_'$pol.log
        # python3 simulator.py ccc_64_$idx'_'$pol --direct > ./test/data/ccc_64_$idx'_'$pol.log
        # python3 simulator.py ccc_160_$idx'_'$pol --direct > ./test/data/ccc_160_$idx'_'$pol.log
        python3 simulator.py ccc_384_$idx'_'$pol --direct > ./test/data/ccc_384_$idx'_'$pol.log
        # python3 simulator.py sen_8_$idx'_'$pol --direct > ./test/data/sen_8_$idx'_'$pol.log
        # python3 simulator.py sen_32_$idx'_'$pol --direct > ./test/data/sen_32_$idx'_'$pol.log
        # python3 simulator.py sen_64_$idx'_'$pol --direct > ./test/data/sen_64_$idx'_'$pol.log
        # python3 simulator.py sen_128_$idx'_'$pol --direct > ./test/data/sen_128_$idx'_'$pol.log
        # python3 simulator.py sen_256_$idx'_'$pol --direct > ./test/data/sen_256_$idx'_'$pol.log
    done
    echo testcase $idx complete
done
