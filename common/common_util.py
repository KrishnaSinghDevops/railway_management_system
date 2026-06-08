import re
from django.db import connections


def get_connection(db_name='default'):
    return connections[db_name]


def select_query(sql_query, params=None, db_name='default'):
    

    results = []

    try:
        sql_query = re.sub(r'[\u00A0\u200B\u200C\u200D\uFEFF]', ' ', sql_query)

        connection = get_connection(db_name)

        with connection.cursor() as cursor:
            cursor.execute(sql_query, params or [])

            columns = [col[0] for col in cursor.description]

            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))

    except Exception as e:
        print("SELECT QUERY ERROR :", e)

    return results


def execute_query(sql_query, params=None, db_name='default'):
    """
    Execute INSERT, UPDATE, DELETE query.

    Returns:
        status, message
    """

    try:
        sql_query = re.sub(r'[\u00A0\u200B\u200C\u200D\uFEFF]', ' ', sql_query)

        connection = get_connection(db_name)

        with connection.cursor() as cursor:
            cursor.execute(sql_query, params or [])

        connection.commit()

        return True, "Query executed successfully"

    except Exception as e:
        return False, str(e)


def global_data(request):
    return {
        'username': request.session.get('USERNAME', '')
    }
