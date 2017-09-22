from cassandra.cluster import Cluster
import os
import uuid
import json

def revert_setup(cass_session, keyspace_name):
    """
    Reverts the cassandra setup and drops the keyspace
    """
    revert_query = "DROP KEYSPACE %s" % (keyspace_name)
    cass_session.execute(revert_query)

def insert(cass_session, keyspace_name, table_name, data):
    """
    Inserts data into the cassandra database
    """
    prepared = cass_session.prepare('INSERT INTO %s.%s JSON ?' % (keyspace_name, table_name))
    cass_session.execute(prepared, [json.dumps(data, ensure_ascii=False)])

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

if __name__ == "__main__":
    keyspace_name = "enron_cluster"
    cass_session = Cluster(['127.0.0.1']).connect()

    create_keyspace(cass_session, keyspace_name)

    create_table(
        cass_session,
        keyspace_name,
        'messages',
        "id text PRIMARY KEY, thread int, time text, sender int, recipient list<int>, cc list<int>, bcc list<int>, subject text, message text"
    )

    create_table(
        cass_session,
        keyspace_name,
        'threads',
        'thread_title text, thread_id int PRIMARY KEY'
    )

    create_table(
        cass_session,
        keyspace_name,
        'users',
        'user text, user_id int PRIMARY KEY'
    )

    create_table(
        cass_session,
        keyspace_name,
        'thread_users',
        'thread_id text PRIMARY KEY, users list<int>'
    )

    # populate users table
    with open('users.json', 'rb') as users_file:
        users_json = json.loads(users_file.read())
        for user in users_json:
            user_row = {
                "user": user,
                "user_id": users_json[user]
            }
            insert(cass_session, keyspace_name, 'users', user_row)
        users_file.close()

    # populate threads table
    with open('threads.json', 'rb') as threads_file:
        threads_json = json.loads(threads_file.read())
        for thread in threads_json:
            thread_row = {
                "thread_title": thread,
                "thread_id": threads_json[thread]
            }
            insert(cass_session, keyspace_name, 'threads', thread_row)
        threads_file.close()

    # populate threads-users table
    with open('thread-users.json', 'rb') as threads_users_file:
        threads_users_json = json.loads(threads_users_file.read())
        for thread in threads_users_json:
            thread_users_row = {
                "thread_id": thread,
                "users": threads_users_json[thread]
            }
            insert(cass_session, keyspace_name, 'thread_users', thread_users_row)
        threads_users_file.close()

    # populate messages table
    with open('messages.json', 'rb') as messages_file:
        messages_json = json.loads(messages_file.read())
        for message in messages_json:
            message["id"] = str(uuid.uuid4())
            insert(cass_session, keyspace_name, 'messages', message)
        messages_file.close()