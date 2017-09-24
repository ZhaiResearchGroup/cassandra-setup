# cassandra-setup

To setup DB: 
1. brew install cassandra (or your OS's equivalent)
2. Clone repo onto machine.
3. pip install -r requirements.txt
4. run python email-parse.py enron_dataset/
5. run cassandra -f, wait until the terminal has a message saying listening and waiting for connections. It will take a few seconds.
6. run python cassandra_setup.py --> This creates the database and parses enron into it

To use API:
1. run python cassandra_interface.py to start the server to listen for requests
2. /thread/single receives a single parameter, an int thread_id for the thread to be retrieved. If no thread is specified, a random one is chosen.
3. /thread/quantity receives a single parameter, an int quantity, specifying the number of threads to be retrieved.
4. /thread/all returns all threads
