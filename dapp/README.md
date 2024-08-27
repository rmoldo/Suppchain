# blockchain-python

How to start network:\

First node needs to have genesis key\
python3 p2p_main.py --ip localhost --port 10001 --api-port 5000 --key-path keys/genesis.pem\
PUT: http://localhost:5000/transaction // isue a transaction\
GET: http://localhost:5000/transactions // get all the transactions\
GET: http://localhost:5000/blockchain // get the blockchain\


python3 p2p_main.py --ip localhost --port 10002 --api-port 5001\
PUT: http://localhost:5001/transaction // isue a transaction\ 
GET: http://localhost:5001/transactions // get all the transactions\
GET: http://localhost:5001/blockchain // get the blockchain\

python3 p2p_main.py --ip localhost --port 10003 --api-port 5002\
PUT: http://localhost:5002/transaction // isue a transaction\
GET: http://localhost:5002/transactions // get all the transactions\
GET: http://localhost:5002/blockchain // get the blockchain\

etc etc
