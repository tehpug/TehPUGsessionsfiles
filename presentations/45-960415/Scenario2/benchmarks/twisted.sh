wrk -t1 -c10 -d20s --latency -s save.lua http://localhost:8083/save > output/twisted-save.txt
wrk -t1 -c10 -d20s --latency -s fetch.lua http://localhost:8083/fetch > output/twisted-fetch.txt
