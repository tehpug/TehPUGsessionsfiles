wrk -t1 -c10 -d20s --latency -s save.lua http://localhost:8080/save > output/japronto-save.txt
wrk -t1 -c10 -d20s --latency -s fetch.lua http://localhost:8080/fetch > output/japronto-fetch.txt
