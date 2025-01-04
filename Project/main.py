from database import save_user_data
from prompt_generation import generate_function

def main():
    github_token = input("Enter Github API Token: ")
    jira_token = input("Enter Jira API Token: ")
    scheduler_time = int(input("Enter Scheduler Time: "))
    rule = input("Enter your rule: ")

    save_user_data(github_token, jira_token, scheduler_time, rule)

    function_code = generate_function(rule)


if __name__ == "__main__":
    main()