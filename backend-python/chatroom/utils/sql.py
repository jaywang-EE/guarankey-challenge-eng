import pymysql

def generate_connection():
    return pymysql.connect(
        user='root',
        password='testpass',
        host= 'db',
        database='challenge',
    )


"""
def search_sql(sql, params):
    db = generate_connection()
    with db.cursor() as cur:
        cur.execute(sql, params)
        result = cur.fetchall()
    db.close()
    return result
def insert_sql(sql, params):
    db = generate_connection()
    with db.cursor() as cur:
        cur.execute(sql, params)
        db.commit()
    db.close()
    return
"""

