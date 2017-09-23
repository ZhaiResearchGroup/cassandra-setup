from flask import Flask, request
from random import randint
import json
from cassandra.cluster import Cluster
from cassandra.query import dict_factory

import cassandra_utility as cutil

cassandra_session = Cluster(['127.0.0.1']).connect('enron_cluster')
cassandra_session.row_factory = dict_factory

app = Flask(__name__)

@app.route('/thread/quantity', methods=['POST'])
def get_number_of_threads():
    """Returns the specified number of email threads"""
    quantity = request.values.get("quantity")
     
    num_threads = cutil.count_threads(cassandra_session)[0].count
    thread_ids = [randint(0, num_threads - 1) for i in range(0, int(quantity))]

    threads = {}
    for thread_id in thread_ids:
        query = "SELECT * FROM messages WHERE thread={}".format(thread_id)
        messages = cassandra_session.execute(query)
        threads[thread_id] = [message_row for message_row in messages]

    return json.dumps(threads)

@app.route('/thread/single', methods=['POST'])
def get_thread():
    """Returns the thread specified by the thread id. 
    If there is no thread_id passed in, randomly selects a thread to return.
    """
    thread = request.values.get("thread")

    # generate random thread number if none is provided
    if thread is None:
        num_threads = cutil.count_threads(cassandra_session)[0].count
        thread = randint(0, num_threads - 1)

    query = "SELECT * FROM messages WHERE thread={}".format(thread)
    messages = cassandra_session.execute(query)

    return json.dumps({"rows": [message_row for message_row in messages]})

@app.route('/thread/all', methods=['POST'])
def get_all_threads():
    """Returns all of the threads in the database"""

    threads = {}
    query = "SELECT * from messages;"
    rows = cassandra_session.execute(query)

    for message_row in rows:
        if message_row["thread"] in threads:
            threads[message_row["thread"]].append(message_row)
        else:
            threads[message_row["thread"]] = [message_row] 

    return json.dumps(threads)

if __name__ == "__main__":
    app.run()