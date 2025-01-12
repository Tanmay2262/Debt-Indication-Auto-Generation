from database import save_user_data
from prompt_generation import generate_function
from function_execution import func_exec
import schedule

def main():
    github_username = input("Enter github username: ")
    github_token = input("Enter Github API Token: ")
    azure_token = input("Enter Azure API Token: ")
    scheduler_time = int(input("Enter Scheduler Time: "))
    rule = input("Enter your rule: ")
    jira_base_url = input("Enter your base url: ")

    save_user_data(username=github_username,github_token=github_token, azure_token=azure_token, scheduler_time=scheduler_time, rule=rule, jira_base_url=jira_base_url)
    generate_function(rule)
    print("Function generated and saved")


    schedule.every(scheduler_time).seconds.do(lambda: func_exec(rule))

    while True:
        schedule.run_pending()




if __name__ == "__main__":
    main()