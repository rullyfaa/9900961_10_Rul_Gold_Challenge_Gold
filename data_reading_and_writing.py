import sqlite3

conn = sqlite3.connect(
    '/Users/pro2015/Desktop/chapter 3 binar/data/challenge gold/gold.db', check_same_thread=False)


def create_table():
    conn.execute(
        """CREATE TABLE IF NO EXISTS cleaning_tweet (id int PRIMARY KEY, cleaning_new_tweet char(1000)) """)
    conn.commit()


def insert_to_table(value_1, value_2):
    value_1 = value_1.encode('latin1')
    value_2 = value_2.encode('latin1')
    query = "INSERT INTO cleaning_tweet (Tweet, cleaning_new_tweet) VALUES (?,?)"
    cursors = conn.execute(query, (value_1, value_2))
    conn.commit()


def read_table(target_index=None, table_name=None):
    if target_index == None:
        results = conn.execute(f'select cleaning_new_tweet FROM {table_name};')
        results = [results for results in results]
        return results
    else:
        results = conn.execute(
            f'select cleaning_new_tweet FROM {table_name}; WHERE id = {target_index}')
        results = [results for results in results]
        return results[0]
