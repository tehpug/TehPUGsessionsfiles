wrk -t1 -c10 -d20s --latency -s encode.lua http://localhost:8082/encode > output/flask-encode.txt
wrk -t1 -c10 -d20s --latency -s decode.lua http://localhost:8082/decode > output/flask-decode.txt
