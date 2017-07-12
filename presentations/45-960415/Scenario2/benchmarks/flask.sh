wrk -t1 -c10 -d20s --latency -s save.lua http://localhost:8082/save > output/flask-save.txt
wrk -t1 -c10 -d20s --latency -s fetch.lua http://localhost:8082/fetch > output/flask-fetch.txt
