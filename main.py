# main.py
from github_data import get_repo_data
from state_comparison import compare_and_report
from discord_report import post_to_discord
from database import load_previous_state, update_database, update_database_with_branches
from pr_report import find_open_merged_pr
from find_branch_info import find_branch_info
from branch_report import branch_report
import config
from github import Github

def main():
    previous_state = load_previous_state()  # Load from database
    # print(previous_state["prs"])
    # exit()
    fork_branches, main_repo = get_repo_data()
    # print(main_repo)
    # exit(0)
    main_prs = {pr.number: pr.state for pr in main_repo.get_pulls(state='all')}
    main_branches = [branch.name for branch in main_repo.get_branches()]
    current_state = {"branches": main_branches, "prs": main_prs}
    current_state["prs"] = {int(key): value for key, value in current_state["prs"].items()}
    previous_state["prs"] = {int(key): value for key, value in previous_state["prs"].items()}
    report_prs = find_open_merged_pr(previous_state, current_state, main_repo)
    print("step1 passed")
    post_to_discord(report_prs, config.DISCORD_WEBHOOK_URL)
    # branch_info = find_branch_info()
    # post_to_discord(branch_info)
    exit(0)
    branches_report, merged_branches_without_pr_report = branch_report()
    post_to_discord(branches_report, config.DISCORD_WEBHOOK_URL)
    post_to_discord(merged_branches_without_pr_report, config.DISCORD_WEBHOOK_URL)
    print("step2 passed")
    exit(0)
    update_database(current_state)
    branches = {branch.name: branch.commit.sha for branch in main_repo.get_branches()}
    update_database_with_branches(branches)
    print("step3 passed")

if __name__ == "__main__":
    main()
