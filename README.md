# cassandra-setup

To setup DB: 
1. brew install cassandra (or your OS's equivalent)
2. Clone repo onto machine.
3. pip install -r requirements.txt
4. run "cassandra -f" in the terminal, wait until terminal has message saying listening for connections to host
5. run python cassandra_setup.py --> This creates the database and parses enron into it

# The python script will crash about 5-6 minutes in depending on how fast your machine is due to a UTF-8 error. This is probably due to the content of one of the emails. Even though it crashes, 5-6 minutes should be enough data for some prelimary work. I will fix this when I have more time.
