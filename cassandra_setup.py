from cassandra.cluster import Cluster
import email_parse
import os
import uuid
import json

def revert_setup(cass_session, keyspace_name):
    """
    Reverts the cassandra setup and drops the keyspace
    """
    revert_query = "DROP KEYSPACE %s" % (keyspace_name)
    cass_session.execute(revert_query)

def insert(cass_session, keyspace_name, table_name, email):
    """
    Inserts an email into the cassandra database
    """
    prepared = cass_session.prepare('INSERT INTO %s.%s JSON ?' % (keyspace_name, table_name))
    cass_session.execute(prepared, [json.dumps(email, ensure_ascii=False)])

def create_table(cass_session, keyspace_name, table_name, columns_string):
    """
    Creates the email table in Cassandra within the designated keyspace
    """
    create_table_query = "CREATE TABLE %s.%s (%s);" % (keyspace_name, table_name, columns_string)
    cass_session.execute(create_table_query)

def create_keyspace(cass_session, keyspace_name):
    """
    Creates a keyspace in Cassandra with one node replication
    """
    create_keyspace_query = "CREATE KEYSPACE IF NOT EXISTS %s WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1 };" % (keyspace_name)
    cass_session.execute(create_keyspace_query)

def cassandra_setup(keyspace_name, initial_table_name, initial_table_columns):
    """
    Initiates the cassandra set up process
    """
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()

    create_keyspace(session, keyspace_name)
    create_table(session, keyspace_name, initial_table_name, initial_table_columns)

    enron_data = get_enron_data(enron_path)

    for email in enron_data:
        email["id"] = str(uuid.uuid4())
        insert(session, keyspace_name, initial_table_name, email)

def get_enron_data(starting_filepath):
    """
    Gets the enron email threads from the data set files
    """
    data = email_parse.parse_email(starting_filepath)
    return data

if __name__ == "__main__":
    keyspace_name = "enron_cluster"
    initial_table_name = "emails"
    initial_table_columns = "id UUID PRIMARY KEY, thread_id int, date text, sender text, recipients list<text>, cc list<text>, bcc list<text>, subject text, message text"
    enron_path = "enron_dataset"

    cassandra_setup(keyspace_name, initial_table_name, initial_table_columns)
