# main.py
from github_data import get_repo_data
from state_comparison import compare_and_report
from discord_report import send_report_to_discord
from database import load_previous_state, update_database, update_database_with_branches
import config
from github import Github

def main():
    previous_state = load_previous_state()  # Load from database
    print(previous_state["prs"])
    # exit()
    main_branches, main_prs, fork_branches, main_repo = get_repo_data()
    current_state = {
        "branches": [branch.name for branch in main_branches],
        "prs": [pr.number for pr in main_prs]
    }
    # print(current_state)
    # exit(0)
    # Initialize GitHub client and main repository
    # g = Github("")
    # main_repo = g.get_repo(config.MAIN_REPO)

    report = compare_and_report(current_state, previous_state, main_repo)
    print("step1 passed")
    # exit(0)
    send_report_to_discord(report)
    print("step2 passed")
    update_database(current_state)
    branches = {branch.name: branch.commit.sha for branch in main_repo.get_branches()}
    update_database_with_branches(branches)
    print("step3 passed")

if __name__ == "__main__":
    main()
