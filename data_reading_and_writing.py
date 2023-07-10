import sqlite3

conn = sqlite3.connect('gold.db', check_same_thread=False)


def create_table():
    conn.execute("""CREATE TABLE IF NOT EXISTS tweet_cleaning (id INTEGER PRIMARY KEY AUTOINCREMENT, previous_text char(1000), cleaned_text char(1000))""")
    conn.commit()


def insert_to_table(value_1, value_2):
    value_1 = value_1.encode('latin1')
    value_2 = value_2.encode('latin1')
    query = f"INSERT INTO tweet_cleaning (previous_text,cleaned_text) VALUES (?, ?);"
    cursors = conn.execute(query, (value_1, value_2))
    conn.commit()


def read_table(target_index=None, target_keywords=None):
    if target_index == None and target_keywords is None:
        results = conn.execute(
            f'select previous_text, cleaned_text FROM tweet_cleaning;')
        results = [result for result in results]
        return results
    elif target_keywords is not None and target_index is None:
        query = f"select previous_text, cleaned_text FROM tweet_cleaning where previous_text like '%{target_keywords}%';"
        results = conn.execute(query)
        results = [result for result in results]
        return results
    elif target_keywords is None and target_index is not None:
        results = conn.execute(
            f'select previous_text, cleaned_text FROM tweet_cleaning WHERE id = {target_index};')
        results = [result for result in results]
        return results[0]


# def create_table():
#     conn.execute(
#         """CREATE TABLE IF NOT EXISTS cleaning_tweet (id int PRIMARY KEY, cleaning_new_tweet char(1000)) """)
#     conn.commit()


# def insert_to_table(value_1, value_2):
#     value_1 = value_1.encode('latin1')
#     value_2 = value_2.encode('latin1')
#     query = "INSERT INTO cleaning_tweet (id int PRIMARY KEY, cleaning_new_tweet) VALUES (?,?)"
#     cursors = conn.execute(query, (value_1, value_2))
#     conn.commit()


# def read_table(target_index=None, table_name=None):
#     if target_index == None:
#         results = conn.execute(f'select cleaning_new_tweet FROM {table_name};')
#         results = [results for results in results]
#         return results
#     else:
#         results = conn.execute(
#             f'select cleaning_new_tweet FROM {table_name}; WHERE id = {target_index}')
#         results = [results for results in results]
#         return results[0]
