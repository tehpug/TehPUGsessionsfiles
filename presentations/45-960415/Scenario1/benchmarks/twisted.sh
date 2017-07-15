wrk -t1 -c10 -d20s --latency -s encode.lua http://localhost:8083/encode > output/twisted-encode.txt
wrk -t1 -c10 -d20s --latency -s decode.lua http://localhost:8083/decode > output/twisted-decode.txt
