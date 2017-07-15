wrk -t1 -c10 -d20s --latency -s encode.lua http://localhost:8081/encode > output/sanic-encode.txt
wrk -t1 -c10 -d20s --latency -s decode.lua http://localhost:8081/decode > output/sanic-decode.txt
