
def count_threads(cassandra_session):
    """Returns the number of threads in the database"""
    query = "select count(*) from enron_cluster.threads;"
    return cassandra_session.execute(query)
    
