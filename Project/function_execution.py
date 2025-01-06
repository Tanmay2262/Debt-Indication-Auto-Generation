from database import connect_db

def execute_function_code(data):
    try:
        if data:
            function_code = data["function_code"].replace("```python", "").replace("```", "").strip()
            print(function_code)

            local_scope = {}
            exec(function_code, local_scope)

            if "function_all" in local_scope:
                result = local_scope['function_all'](
                    github_token=data["github_token"],
                    jira_token=data["jira_token"],
                    github_username=data["github_username"],
                    rule = data["rule"],
                    jira_base_url = data["jira_base_url"]
                )
                print(f"Function result: {result}")
                return result
            else:
                print("No function named 'function_all' found in the code.")
                return None
        else:
            print("No function code found.")
            return None

    except Exception as e:
        print(f"Error while executing function code: {e}")
        return None


def func_exec(rule):
    query = f'''SELECT 
        data->>'github_token' AS github_token,
        data->>'function_code' AS function_code, 
        data->>'jira_token' AS jira_token, 
        data->>'rule' AS rule, 
        data->>'github_username' AS github_username,
        data->>'jira_base_url' AS jira_base_url
    FROM info_table 
    WHERE data->>'function_code' IS NOT NULL AND data->>'rule' = '{rule}'
    '''

    conn = connect_db()  # Add your condition here if needed
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        github_token = result[0]
        jira_token = result[2]
        function_code = result[1]
        github_username = result[4]
        rule = result[3]
        jira_base_url = result[5]

        # Save extracted data into a variable
        extracted_data = {
            "github_token": github_token,
            "jira_token": jira_token,
            "function_code": function_code,
            "github_username": github_username,
            "rule": rule,
            "jira_base_url": jira_base_url
        }

        execute_function_code(extracted_data)

