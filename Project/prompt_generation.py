import psycopg2
import google.generativeai as genai
import json

DB_CONFIG={"dbname":"User_Information",
            "user":"postgres",
            "password":"Pzangoba1!",
            "host":"localhost",
            "port":"5432"}

def get_user_data(rule):
    """Fetch user data from the database."""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    query = "SELECT data->>'rule' AS rule, data->>'azure_token' AS azure_token, data->>'github_token' AS github_token, data->>'function_code' AS function_code, data->>'scheduler_time' AS scheduler_time, data->>'jira_base_url' AS jira_base_url FROM info_table WHERE data->>'rule' = %s;"
    cursor.execute(query, (rule,))

    result = cursor.fetchone()

    if result:
        user_data = {
            "rule": result[0],
            "azure_token": result[1],
            "github_token": result[2],
            "function_code": result[3],
            "github_username": result[4],
            "jira_base_url": result[5]
        }
    else:
        user_data = None

    return user_data

def generate_function(rule):
    user_data = get_user_data(rule)
    if not user_data:
        raise Exception("No user data found in the database.")

    rule = user_data["rule"]
    azure_token = user_data["azure_token"]
    github_token = user_data["github_token"]
    github_username = user_data["github_username"]
    jira_base_url = user_data["jira_base_url"]
    prompt = f"""
        Write a Python function that implements the following rule: "{rule}".
        The function should accept the following parameters:
        - github token: {github_token}
        - azure token: {azure_token}
        - github username: {github_username}
        - rule: {rule}
        - jira_base_url: {jira_base_url}
        Assign these tokens in the function defination as default parameters and the name of the parameters should be as above only.
        But the github username can be optional and only when needed
        Ensure the function is written in Python and returns the required results as per the rule entered.
        Take the azure board name from the rule as it is and no need to assume any other name other than the one given in the rule.
        To access github and azure you can use the token that has been passed.
        Use Github/ Azure REST API instead of library.
        Importanat to note, Only provide the function and no other text including any comments in the code. the function name has to be function_all
        """

    genai.configure(api_key="AIzaSyAIXY2ayF-Z2eNEgXMO4UY8WDHvaxfSYsE")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    # print(response.text)
    update_function_in_db(rule,response.text)

def update_function_in_db(rule, function_code):
    function_code_json = json.dumps(function_code)

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    update_query = """
                UPDATE info_table
                SET data = jsonb_set(data, '{function_code}', %s::jsonb, true)
                WHERE data->>'rule' = %s;
            """

    cursor.execute(update_query, (function_code_json, rule))
    conn.commit()
    print(f"Updated function_code for rule: {function_code_json}")
    cursor.close()
    conn.close()


