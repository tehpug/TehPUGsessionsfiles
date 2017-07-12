wrk -t1 -c10 -d20s --latency -s encode.lua http://localhost:8080/encode > output/japronto-encode.txt
wrk -t1 -c10 -d20s --latency -s decode.lua http://localhost:8080/decode > output/japronto-decode.txt
