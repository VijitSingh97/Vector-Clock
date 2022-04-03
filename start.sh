# kill anything running before
./stop.sh 2> /dev/null

python3 main.py 0 &
echo $! > server_8080.pid
python3 main.py 1 &
echo $! > server_8081.pid
python3 main.py 2 &
echo $! > server_8082.pid