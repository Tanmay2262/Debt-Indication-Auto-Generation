import psycopg2
import json

def connect_db():
    DB_CONFIG = {"dbname": "User_Information",
                 "user": "postgres",
                 "password": "Pzangoba1!",
                 "host": "localhost",
                 "port": "5432"}
    return psycopg2.connect(**DB_CONFIG)

def save_user_data(username,github_token, azure_token, scheduler_time, rule, jira_base_url, function_code=None):

    data = {
        "github_username": username,
        "github_token": github_token,
        "azure_token": azure_token,
        "scheduler_time": scheduler_time,
        "rule": rule,
        "function_code": function_code,
        "jira_base_url": jira_base_url
    }

    try:
        conn = connect_db()
        cursor = conn.cursor()

        json_data = json.dumps(data)

        cursor.execute(
            "INSERT INTO info_table (data) VALUES (%s)",
            [json_data]
        )

        conn.commit()

        print("JSON data inserted successfully!")

    except Exception as e:
        print("An error occurred:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_function_code(rule):
    """
    Fetch the function_code for a specific rule from the database.

    :param rule: The rule for which to fetch the function_code.
    :return: The function_code as a string, or None if not found.
    """
    conn = connect_db()
    cursor = conn.cursor()

    function_code_retrieval = "SELECT data->>'function_code' FROM info_table WHERE data->>'rule' = %s AND data->>'function_code' IS NOT NULL"

    cursor.execute(function_code_retrieval,(rule,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return result[0]
    else:
        return None
