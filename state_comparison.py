# state_comparison.py
import config
import sqlite3
from github import Github
def fetch_previous_branch_state(db_name='branch_state.db'):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Fetch all branch states
    cursor.execute('SELECT branch_name, commit_hash FROM branch_state')
    rows = cursor.fetchall()

    # Convert the fetched data into a dictionary
    previous_branch_state = {branch_name: commit_hash for branch_name, commit_hash in rows}

    # Close the connection
    conn.close()

    return previous_branch_state


def compare_and_report(current_state, previous_state, main_repo):
    # report = []
    print("I'm in comparing")
    default_branch = main_repo.default_branch
    # Determine the last PR number from the previous state
    last_pr_number = max(previous_state['prs'], default=0)
    print(last_pr_number)
    # exit(0)
    # Compare branches with new PRs
    # Step 1: Collect unique branch names associated with new PRs
    new_branch_names = set()

    for pr in current_state['prs']:
        if pr > last_pr_number:  # Only consider new PRs
            pr_details = main_repo.get_pull(pr)
            
            # Add head and base branches to the set
            new_branch_names.add(pr_details.head.ref)
            new_branch_names.add(pr_details.base.ref)

    # Step 2: Generate a report for each unique branch
    branch_report = []

    for branch_name in new_branch_names:
        # Find new PRs associated with this branch
        associated_prs = [
            pr for pr in current_state['prs'] if (
                pr > last_pr_number and  # Only consider new PRs
                (main_repo.get_pull(pr).head.ref == branch_name or 
                main_repo.get_pull(pr).base.ref == branch_name)
            )
        ]
    
        # Collect all new commits for this branch
        branch_commits = []
        for pr in associated_prs:
            pr_details = main_repo.get_pull(pr)
            commits = pr_details.get_commits()
            for commit in commits:
                branch_commits.append(f"- {commit.commit.message} ({commit.html_url})")

        # Create a report entry for the branch
        branch_report.append(
            f"Branch: {branch_name}\n"
            f"Associated PRs:\n" +
            "\n".join([
                f"  PR #{pr}: {main_repo.get_pull(pr).title} ({main_repo.get_pull(pr).html_url})"
                for pr in associated_prs
            ]) + "\n"
            "Commits:\n" + "\n".join(branch_commits) + "\n"
            "-----------------------------------\n"
        )

    print("passed succcessfully")

    # Print the branch report
    for report_item in branch_report:
        print(report_item)

    # exit(0)
    # print(branch_report)
    print(type(branch_report))
    print("\n\n\n")
    # exit(0)
    # Compare branches without PRs
    # Step 1: Get all branches in the main repository
    all_branches = [branch.name for branch in main_repo.get_branches()]

    print(all_branches)
    # exit(0)
    # Step 2: Filter out branches associated with PRs
    non_pr_branches = set(all_branches) - new_branch_names
    print(non_pr_branches)
    # Assume you have a dictionary `previous_branch_state` that stores the last known commit hash for each branch
    # Example: previous_branch_state = {'branch_name': 'commit_hash'}
    previous_branch_state = fetch_previous_branch_state()
    # Step 3: Compare commits and generate report
    for branch_name in non_pr_branches:
        print(branch_name)
        # Fetch the latest commit for this branch
        latest_commit = main_repo.get_branch(branch_name).commit

        # Get the previous commit hash for this branch
        previous_commit_hash = previous_branch_state.get(branch_name, None)

        # If there is a previous commit hash, find all new commits
        if previous_commit_hash:
            # Compare the range from the previous commit to the latest commit
            comparison = main_repo.compare(previous_commit_hash, latest_commit.sha)
            new_commits = comparison.commits
        else:
        # If there is no previous commit hash, fetch all commits in the branch
        # This assumes the branch is new, so we take all commits from the initial commit
            print("im here")

            comparison = main_repo.compare(default_branch, branch_name)
            new_commits = comparison.commits
            # Create a list of commit messages and URLs

        commit_list = [f"- {commit.commit.message} ({commit.html_url})" for commit in new_commits]
        if len(commit_list) == 0:
            continue
        # Create a report entry for the branch
        branch_report.append(
            f"Branch: {branch_name}\n"
            "Commits:\n" + "\n".join(commit_list) + "\n"
            "-----------------------------------\n"
        )

    # Print the updated branch report
    for report_item in branch_report:
        print(report_item)

    # print(report)
    return branch_report