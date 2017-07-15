wrk -t1 -c10 -d20s --latency -s save.lua http://localhost:8081/save > output/sanic-save.txt
wrk -t1 -c10 -d20s --latency -s fetch.lua http://localhost:8081/fetch > output/sanic-fetch.txt
