#!/bin/bash
 
for idx in {1..100}
do
    # python3 setconf.py knc_9_$idx knc 3 2
    # python3 setconf.py knc_27_$idx knc 3 3
    # python3 setconf.py knc_64_$idx knc 4 3
    # python3 setconf.py knc_81_$idx knc 3 4
    # python3 setconf.py knc_256_$idx knc 4 4
    # python3 setconf.py ccc_8_$idx ccc 2
    # python3 setconf.py ccc_24_$idx ccc 3
    # python3 setconf.py ccc_64_$idx ccc 4
    # python3 setconf.py ccc_160_$idx ccc 5
    python3 setconf.py ccc_384_$idx ccc 6
    # python3 setconf.py sen_8_$idx sen 3
    # python3 setconf.py sen_32_$idx sen 5
    # python3 setconf.py sen_64_$idx sen 6
    # python3 setconf.py sen_128_$idx sen 7
    # python3 setconf.py sen_256_$idx sen 8
done