import psycopg2
import json

def save_user_data(github_token, jira_token, scheduler_time, rule, function_code=None):

    data = {
        "github_token": github_token,
        "jira_token": jira_token,
        "scheduler_time": scheduler_time,
        "rule": rule,
        "function_code": function_code
    }

    try:
        conn = psycopg2.connect(
            dbname="User_Information",
            user="postgres",
            password="Pzangoba1!",
            host="localhost",
            port="5432"
        )
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
