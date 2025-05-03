def successLogger(cursor, operations):
    cursor.execute(operations)
    return cursor.fetchall()
