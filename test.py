

# import os
# from github import Github
# import requests
# import json
# from datetime import datetime
# import config
# import sqlite3
# # from detecting import chanking_report
# from discord_report import send_report_to_discord
# import re

# def wrap_urls_with_angle_brackets(text):
#     # Regular expression to match URLs
#     url_pattern = r'(https?://\S+)'
    
#     # Split the text by the newline character
#     parts = text.split('\n')
    
#     # Wrap URLs in each part
#     wrapped_parts = []
#     for part in parts:
#         wrapped_part = re.sub(url_pattern, r'<\1>', part.strip())
#         wrapped_parts.append(wrapped_part)
    
#     # Join the parts back with newline
#     return '\n'.join(wrapped_parts)

# def chunk_report(report):
#     # Discord message limit
#     DISCORD_MESSAGE_LIMIT = 2000

#     # Wrap URLs in the entire report
#     report = wrap_urls_with_angle_brackets(report)

#     # Split the report into chunks
#     chunks = []
#     lines = report.split('\n')
#     current_chunk = ""

#     for line in lines:
#         # Check if adding the line would exceed the limit
#         if len(current_chunk) + len(line) + 1 > DISCORD_MESSAGE_LIMIT:
#             # If it would, save the current chunk and start a new one
#             chunks.append(current_chunk)
#             current_chunk = line
#         else:
#             # Otherwise, add the line to the current chunk
#             if current_chunk:
#                 current_chunk += "\n" + line
#             else:
#                 current_chunk = line

#     # Don't forget to add the last chunk
#     if current_chunk:
#         chunks.append(current_chunk)
    
#     return chunks

# # GitHub API token
# GITHUB_TOKEN = config.git_access_token

# # Discord webhook URL
# DISCORD_WEBHOOK_URL = "your_discord_webhook_url_here"

# # Initialize GitHub client
# g = Github(GITHUB_TOKEN)

# def fetch_current_repo_state(repo_family):
#     current_state = []
#     for repo_full_name in repo_family:
#         repo = g.get_repo(repo_full_name)
#         branches = repo.get_branches()
#         for branch in branches:
#             current_state.append({
#                 "repo_owner": repo.owner.login,
#                 "repo_name": repo.name,
#                 "branch_name": branch.name,
#                 "commit_hash": branch.commit.sha
#             })
#     return current_state

# def load_previous_state(db_name='branch_state.db'):
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
    
#     cursor.execute('''
#         SELECT repo_owner, repo_name, branch_name, commit_hash
#         FROM branch_state
#     ''')
    
#     previous_state = []
#     for row in cursor.fetchall():
#         previous_state.append({
#             "repo_owner": row[0],
#             "repo_name": row[1],
#             "branch_name": row[2],
#             "commit_hash": row[3]
#         })
    
#     conn.close()
#     return previous_state

# def save_current_state(current_state):
#     with open("previous_state.json", "w") as f:
#         json.dump(current_state, f)

# def convert_commits(paginated_commits):
#     return [{"name": commit.commit.message.split('\n')[0], "link": commit.html_url} for commit in paginated_commits]

# def compare_states(current_state, previous_state):
#     new_branches = []
#     updated_branches = []
#     deleted_branches = []
#     rebased_branches = []  # New list for rebased branches
#     current_branch_keys = {(b['repo_owner'], b['repo_name'], b['branch_name']) for b in current_state}
#     for current_branch in current_state:
#         repo_full_name = f"{current_branch['repo_owner']}/{current_branch['repo_name']}"
#         repo = g.get_repo(repo_full_name)
        
#         previous_branch = next((b for b in previous_state 
#                                 if b["repo_owner"] == current_branch["repo_owner"] 
#                                 and b["repo_name"] == current_branch["repo_name"] 
#                                 and b["branch_name"] == current_branch["branch_name"]), None)
        
#         if previous_branch is None:
#             # New branch
#             default_branch = repo.default_branch
#             comparison = repo.compare(default_branch, current_branch["branch_name"])
#             if comparison.commits:
#                 new_branches.append({
#                     "repo_owner": current_branch["repo_owner"],
#                     "repo_name": current_branch["repo_name"],
#                     "branch_name": current_branch["branch_name"],
#                     "commit_hash": current_branch["commit_hash"],
#                     "commits": convert_commits(comparison.commits)
#                 })
#         elif current_branch["commit_hash"] != previous_branch["commit_hash"]:
#             # Existing branch with new commits
#             comparison = repo.compare(previous_branch["commit_hash"], current_branch["commit_hash"])
#             if comparison.commits:
#                 updated_branches.append({
#                     "repo_owner": current_branch["repo_owner"],
#                     "repo_name": current_branch["repo_name"],
#                     "branch_name": current_branch["branch_name"],
#                     "current_commit_hash": current_branch["commit_hash"],
#                     "previous_commit_hash": previous_branch["commit_hash"],
#                     "commits": convert_commits(comparison.commits)
#                 })
                
#                 # Check for rebased branches
#                 if is_rebased(comparison):
#                     rebased_branches.append({
#                         "repo_owner": current_branch["repo_owner"],
#                         "repo_name": current_branch["repo_name"],
#                         "branch_name": current_branch["branch_name"],
#                         "commits": convert_commits(comparison.commits)
#                     })
#     for previous_branch in previous_state:
#         if (previous_branch['repo_owner'], previous_branch['repo_name'], previous_branch['branch_name']) not in current_branch_keys:
#             deleted_branches.append(previous_branch)
    
#     return new_branches, updated_branches, deleted_branches, rebased_branches

# def is_rebased(comparison):
#     # Logic to determine if the branch is rebased
#     # This is a placeholder function. You need to implement the actual logic
#     # to detect if the branch has been rebased.
#     # For simplicity, let's assume a branch is rebased if all commits have different hashes.
#     return all(commit.sha != comparison.base_commit.sha for commit in comparison.commits)

# def fetch_commits(repo_full_name, branch_name, since_commit=None):
#     repo = g.get_repo(repo_full_name)
#     commits = []
#     for commit in repo.get_commits(sha=branch_name):
#         if since_commit and commit.sha == since_commit:
#             break
#         commits.append({
#             "name": commit.commit.message.split('\n')[0],  # Get first line of commit message
#             "link": commit.html_url
#         })
#     return commits

# def generate_report(new_branches, updated_branches, deleted_branches, rebased_branches):
#     report = "**Git Repository Update Report**\n\n"

#     if new_branches:
#         report += "**New branches:**\n"
#         for branch in new_branches:
#             repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
#             branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
#             report += f"\n{branch_url}\n"
#             report += "Commits:\n"
            
#             for commit in branch["commits"]:
#                 report += f"    {commit['name']} ({commit['link']} )\n"
    
#     if updated_branches:
#         report += "\n**Updated branches:**\n"
#         for branch in updated_branches:
#             repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
#             branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
#             report += f"\n{branch_url}\n"
#             report += "New commits:\n"
            
#             for commit in branch["commits"]:
#                 report += f"    {commit['name']} ({commit['link']} )\n"
    
#     if deleted_branches:
#         report += "\n**Deleted branches:**\n"
#         for branch in deleted_branches:
#             repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
#             branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
#             report += f"\n{branch_url}\n"
    
#     if rebased_branches:
#         report += "\n**Rebased branches:**\n"
#         for branch in rebased_branches:
#             repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
#             branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
#             report += f"\nBranch URL: {branch_url}\n"
#             report += "Commits :\n"
            
#             for commit in branch["commits"]:
#                 # Assuming you have a way to map old commits to new ones,
#                 # this is a placeholder to show the format.
#                 # Replace `old_commit` and `new_commit` with actual commit data.
#                 # old_commit = commit['name']  # Placeholder for the old commit name
#                 new_commit = commit['name']  # Placeholder for the new commit name
#                 report += f"    {new_commit} ({commit['link']} )\n"
    
#     return report


# def post_to_discord(report, webhook_url):
#     # Split the report into chunks of 2000 characters or less
#     chunks = [report[i:i+2000] for i in range(0, len(report), 2000)]
    
#     for chunk in chunks:
#         payload = {
#             "content": chunk
#         }
#         response = requests.post(webhook_url, json=payload)
#         if response.status_code != 204:
#             print(f"Failed to post to Discord. Status code: {response.status_code}")

# def update_database(current_state, db_name='branch_state.db'):
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
    
#     # Create the table if it doesn't exist
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS branch_state (
#             repo_owner TEXT,
#             repo_name TEXT,
#             branch_name TEXT,
#             commit_hash TEXT,
#             PRIMARY KEY (repo_owner, repo_name, branch_name)
#         )
#     ''')
    
#     # Insert or update each branch state
#     for branch in current_state:
#         cursor.execute('''
#             INSERT INTO branch_state (repo_owner, repo_name, branch_name, commit_hash)
#             VALUES (?, ?, ?, ?)
#             ON CONFLICT(repo_owner, repo_name, branch_name)
#             DO UPDATE SET commit_hash=excluded.commit_hash
#         ''', (branch['repo_owner'], branch['repo_name'], branch['branch_name'], branch['commit_hash']))
    
#     conn.commit()
#     conn.close()


# def main():
#     main_repo = config.MAIN_REPO
#     forks = config.FORKS
#     repo_family = [main_repo] + forks
#     current_state = fetch_current_repo_state(repo_family)
#     previous_state = load_previous_state()
#     new_branches, updated_branches, deleted_branches, rebased_branches = compare_states(current_state, previous_state)  # Added rebased_branches
#     print(len(deleted_branches))
#     print (new_branches)
#     print("\n\n")
#     print(updated_branches)
#     # exit(0)
#     if new_branches or updated_branches or deleted_branches or rebased_branches:  # Check for rebased_branches
#         report = generate_report(new_branches, updated_branches, deleted_branches, rebased_branches)  # Added rebased_branches
#         print(report)
#         report = chunk_report(report)
#         print(report)
#         send_report_to_discord(report)
#     # update_database(current_state)
#         # post_to_discord(report, DISCORD_WEBHOOK_URL)

# # Uncomment to run the main function
# if __name__ == "__main__":
#     main()


# import os
# from github import Github
# import requests
# import json
# from datetime import datetime
# import config
# import sqlite3
# # from detecting import chanking_report
# from discord_report import send_report_to_discord
# import re

# def wrap_urls_with_angle_brackets(text):
#     url_pattern = r'(https?://\S+)'
#     parts = text.split('\n')
#     wrapped_parts = []
#     for part in parts:
#         wrapped_part = re.sub(url_pattern, r'<\1>', part.strip())
#         wrapped_parts.append(wrapped_part)
#     return '\n'.join(wrapped_parts)

# def chunk_report(report):
#     DISCORD_MESSAGE_LIMIT = 2000
#     report = wrap_urls_with_angle_brackets(report)
#     chunks = []
#     lines = report.split('\n')
#     current_chunk = ""

#     for line in lines:
#         if len(current_chunk) + len(line) + 1 > DISCORD_MESSAGE_LIMIT:
#             chunks.append(current_chunk)
#             current_chunk = line
#         else:
#             if current_chunk:
#                 current_chunk += "\n" + line
#             else:
#                 current_chunk = line

#     if current_chunk:
#         chunks.append(current_chunk)
    
#     return chunks

# GITHUB_TOKEN = config.git_access_token
# DISCORD_WEBHOOK_URL = "your_discord_webhook_url_here"
# g = Github(GITHUB_TOKEN)

# def fetch_current_repo_state(repo_family):
#     current_state = []
#     for repo_full_name in repo_family:
#         repo = g.get_repo(repo_full_name)
#         branches = repo.get_branches()
#         for branch in branches:
#             current_state.append({
#                 "repo_owner": repo.owner.login,
#                 "repo_name": repo.name,
#                 "branch_name": branch.name,
#                 "commit_hash": branch.commit.sha
#             })
#     return current_state

# def load_previous_state(db_name='branch_state.db'):
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#     cursor.execute('''
#         SELECT repo_owner, repo_name, branch_name, commit_hash
#         FROM branch_state
#     ''')
#     previous_state = []
#     for row in cursor.fetchall():
#         previous_state.append({
#             "repo_owner": row[0],
#             "repo_name": row[1],
#             "branch_name": row[2],
#             "commit_hash": row[3]
#         })
#     conn.close()
#     return previous_state

# def save_current_state(current_state):
#     with open("previous_state.json", "w") as f:
#         json.dump(current_state, f)

# def convert_commits(paginated_commits):
#     return [{"name": commit.commit.message.split('\n')[0], "link": commit.html_url} for commit in paginated_commits]

# def compare_states(current_state, previous_state):
#     new_branches = []
#     updated_branches = []
#     deleted_branches = []
#     rebased_branches = []
#     current_branch_keys = {(b['repo_owner'], b['repo_name'], b['branch_name']) for b in current_state}
#     for current_branch in current_state:
#         repo_full_name = f"{current_branch['repo_owner']}/{current_branch['repo_name']}"
#         repo = g.get_repo(repo_full_name)
        
#         previous_branch = next((b for b in previous_state 
#                                 if b["repo_owner"] == current_branch["repo_owner"] 
#                                 and b["repo_name"] == current_branch["repo_name"] 
#                                 and b["branch_name"] == current_branch["branch_name"]), None)
        
#         if previous_branch is None:
#             default_branch = repo.default_branch
#             comparison = repo.compare(default_branch, current_branch["branch_name"])
#             if comparison.commits:
#                 new_branches.append({
#                     "repo_owner": current_branch["repo_owner"],
#                     "repo_name": current_branch["repo_name"],
#                     "branch_name": current_branch["branch_name"],
#                     "commit_hash": current_branch["commit_hash"],
#                     "commits": convert_commits(comparison.commits)
#                 })
#         elif current_branch["commit_hash"] != previous_branch["commit_hash"]:
#             comparison = repo.compare(previous_branch["commit_hash"], current_branch["commit_hash"])
#             if comparison.commits:
#                 updated_branches.append({
#                     "repo_owner": current_branch["repo_owner"],
#                     "repo_name": current_branch["repo_name"],
#                     "branch_name": current_branch["branch_name"],
#                     "current_commit_hash": current_branch["commit_hash"],
#                     "previous_commit_hash": previous_branch["commit_hash"],
#                     "commits": convert_commits(comparison.commits)
#                 })
                
#                 if is_rebased(comparison):
#                     rebased_branches.append({
#                         "repo_owner": current_branch["repo_owner"],
#                         "repo_name": current_branch["repo_name"],
#                         "branch_name": current_branch["branch_name"],
#                         "commits": convert_commits(comparison.commits)
#                     })
#     for previous_branch in previous_state:
#         if (previous_branch['repo_owner'], previous_branch['repo_name'], previous_branch['branch_name']) not in current_branch_keys:
#             deleted_branches.append(previous_branch)
    
#     return new_branches, updated_branches, deleted_branches, rebased_branches

# def is_rebased(comparison):
#     return all(commit.sha != comparison.base_commit.sha for commit in comparison.commits)

# def fetch_commits(repo_full_name, branch_name, since_commit=None):
#     repo = g.get_repo(repo_full_name)
#     commits = []
#     for commit in repo.get_commits(sha=branch_name):
#         if since_commit and commit.sha == since_commit:
#             break
#         commits.append({
#             "name": commit.commit.message.split('\n')[0],
#             "link": commit.html_url
#         })
#     return commits

# def generate_report(new_branches, updated_branches, deleted_branches, rebased_branches):
#     report = "**Git Repository Update Report**\n\n"

#     if new_branches:
#         report += "**New branches:**\n"
#         for branch in new_branches:
#             repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
#             branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
#             report += f"\n{branch_url}\n"
#             report += "Commits:\n"
            
#             for commit in branch["commits"]:
#                 report += f"    {commit['name']} ({commit['link']} )\n"
    
#     if updated_branches:
#         report += "\n**Updated branches:**\n"
#         for branch in updated_branches:
#             repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
#             branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
#             report += f"\n{branch_url}\n"
#             report += "New commits:\n"
            
#             for commit in branch["commits"]:
#                 report += f"    {commit['name']} ({commit['link']} )\n"
    
#     if deleted_branches:
#         report += "\n**Deleted branches:**\n"
#         for branch in deleted_branches:
#             repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
#             branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
#             report += f"\n{branch_url}\n"
    
#     if rebased_branches:
#         report += "\n**Rebased branches:**\n"
#         for branch in rebased_branches:
#             repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
#             branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
#             report += f"\nBranch URL: {branch_url}\n"
#             report += "Commits :\n"
            
#             for commit in branch["commits"]:
#                 new_commit = commit['name']
#                 report += f"    {new_commit} ({commit['link']} )\n"
    
#     return report

# def find_merged_branches_without_pr(current_state, previous_state):
#     merged_without_pr = []
#     for current_branch in current_state:
#         repo_full_name = f"{current_branch['repo_owner']}/{current_branch['repo_name']}"
#         repo = g.get_repo(repo_full_name)

#         # Check if the branch has been merged into the default branch
#         default_branch = repo.default_branch
#         comparison = repo.compare(default_branch, current_branch["branch_name"])

#         # If there are commits in the comparison, it indicates a merge
#         if comparison.commits:
#             # Check if there is no associated pull request
#             pulls = repo.get_pulls(state='closed', base=default_branch)
#             pr_found = any(pr.head.ref == current_branch["branch_name"] for pr in pulls)
#             if not pr_found:
#                 merged_without_pr.append(current_branch["branch_name"])
    
#     return merged_without_pr

# def post_to_discord(report, webhook_url):
#     chunks = [report[i:i+2000] for i in range(0, len(report), 2000)]
    
#     for chunk in chunks:
#         payload = {
#             "content": chunk
#         }
#         response = requests.post(webhook_url, json=payload)
#         if response.status_code != 204:
#             print(f"Failed to post to Discord. Status code: {response.status_code}")

# def update_database(current_state, db_name='branch_state.db'):
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS branch_state (
#             repo_owner TEXT,
#             repo_name TEXT,
#             branch_name TEXT,
#             commit_hash TEXT,
#             PRIMARY KEY (repo_owner, repo_name, branch_name)
#         )
#     ''')
#     for branch in current_state:
#         cursor.execute('''
#             INSERT INTO branch_state (repo_owner, repo_name, branch_name, commit_hash)
#             VALUES (?, ?, ?, ?)
#             ON CONFLICT(repo_owner, repo_name, branch_name)
#             DO UPDATE SET commit_hash=excluded.commit_hash
#         ''', (branch['repo_owner'], branch['repo_name'], branch['branch_name'], branch['commit_hash']))
    
#     conn.commit()
#     conn.close()

# def main():
#     main_repo = config.MAIN_REPO
#     forks = config.FORKS
#     repo_family = [main_repo] + forks
#     current_state = fetch_current_repo_state(repo_family)
#     previous_state = load_previous_state()
#     new_branches, updated_branches, deleted_branches, rebased_branches = compare_states(current_state, previous_state)
    
#     merged_without_pr = find_merged_branches_without_pr(current_state, previous_state)
#     if merged_without_pr:
#         print("Merged branches without PR:", merged_without_pr)
    
#     if new_branches or updated_branches or deleted_branches or rebased_branches:
#         report = generate_report(new_branches, updated_branches, deleted_branches, rebased_branches)
#         report = chunk_report(report)
#         send_report_to_discord(report)

# if __name__ == "__main__":
#     main()



# import os
# from github import Github
# import requests
# import json
# from datetime import datetime
# import config
# import sqlite3
# from discord_report import send_report_to_discord
# import re

# def wrap_urls_with_angle_brackets(text):
#     url_pattern = r'(https?://\S+)'
#     parts = text.split('\n')
#     wrapped_parts = []
#     for part in parts:
#         wrapped_part = re.sub(url_pattern, r'<\1>', part.strip())
#         wrapped_parts.append(wrapped_part)
#     return '\n'.join(wrapped_parts)

# def chunk_report(report):
#     DISCORD_MESSAGE_LIMIT = 2000
#     report = wrap_urls_with_angle_brackets(report)
#     chunks = []
#     lines = report.split('\n')
#     current_chunk = ""

#     for line in lines:
#         if len(current_chunk) + len(line) + 1 > DISCORD_MESSAGE_LIMIT:
#             chunks.append(current_chunk)
#             current_chunk = line
#         else:
#             if current_chunk:
#                 current_chunk += "\n" + line
#             else:
#                 current_chunk = line

#     if current_chunk:
#         chunks.append(current_chunk)
    
#     return chunks

# GITHUB_TOKEN = config.git_access_token
# DISCORD_WEBHOOK_URL = "your_discord_webhook_url_here"
# g = Github(GITHUB_TOKEN)

# def fetch_current_repo_state(repo_family):
#     current_state = []
#     for repo_full_name in repo_family:
#         repo = g.get_repo(repo_full_name)
#         branches = repo.get_branches()
#         for branch in branches:
#             current_state.append({
#                 "repo_owner": repo.owner.login,
#                 "repo_name": repo.name,
#                 "branch_name": branch.name,
#                 "commit_hash": branch.commit.sha
#             })
#     return current_state

# def load_previous_state(db_name='branch_state.db'):
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
#     cursor.execute('''
#         SELECT repo_owner, repo_name, branch_name, commit_hash
#         FROM branch_state
#     ''')
#     previous_state = []
#     for row in cursor.fetchall():
#         previous_state.append({
#             "repo_owner": row[0],
#             "repo_name": row[1],
#             "branch_name": row[2],
#             "commit_hash": row[3]
#         })
#     conn.close()
#     return previous_state

# def save_current_state(current_state):
#     with open("previous_state.json", "w") as f:
#         json.dump(current_state, f)

# def convert_commits(paginated_commits):
#     return [{"name": commit.commit.message.split('\n')[0], "link": commit.html_url} for commit in paginated_commits]

# def compare_states(current_state, previous_state):
#     new_branches = []
#     updated_branches = []
#     deleted_branches = []
#     rebased_branches = []
#     current_branch_keys = {(b['repo_owner'], b['repo_name'], b['branch_name']) for b in current_state}
    
#     for current_branch in current_state:
#         repo_full_name = f"{current_branch['repo_owner']}/{current_branch['repo_name']}"
#         repo = g.get_repo(repo_full_name)
        
#         previous_branch = next((b for b in previous_state 
#                                 if b["repo_owner"] == current_branch["repo_owner"] 
#                                 and b["repo_name"] == current_branch["repo_name"] 
#                                 and b["branch_name"] == current_branch["branch_name"]), None)
        
#         if previous_branch is None:
#             default_branch = repo.default_branch
#             comparison = repo.compare(default_branch, current_branch["branch_name"])
#             if comparison.commits:
#                 new_branches.append({
#                     "repo_owner": current_branch["repo_owner"],
#                     "repo_name": current_branch["repo_name"],
#                     "branch_name": current_branch["branch_name"],
#                     "commit_hash": current_branch["commit_hash"],
#                     "commits": convert_commits(comparison.commits)
#                 })
#         elif current_branch["commit_hash"] != previous_branch["commit_hash"]:
#             comparison = repo.compare(previous_branch["commit_hash"], current_branch["commit_hash"])
#             if comparison.commits:
#                 updated_branches.append({
#                     "repo_owner": current_branch["repo_owner"],
#                     "repo_name": current_branch["repo_name"],
#                     "branch_name": current_branch["branch_name"],
#                     "current_commit_hash": current_branch["commit_hash"],
#                     "previous_commit_hash": previous_branch["commit_hash"],
#                     "commits": convert_commits(comparison.commits)
#                 })
                
#                 if is_rebased(comparison):
#                     rebased_branches.append({
#                         "repo_owner": current_branch["repo_owner"],
#                         "repo_name": current_branch["repo_name"],
#                         "branch_name": current_branch["branch_name"],
#                         "commits": convert_commits(comparison.commits)
#                     })
    
#     for previous_branch in previous_state:
#         if (previous_branch['repo_owner'], previous_branch['repo_name'], previous_branch['branch_name']) not in current_branch_keys:
#             deleted_branches.append(previous_branch)
    
#     return new_branches, updated_branches, deleted_branches, rebased_branches

# def is_rebased(comparison):
#     # Example: Use git to check commit history
#     # This example assumes you have access to the local repository
#     import subprocess

#     try:
#         # Fetch the commit history for the branch
#         commits = subprocess.check_output(
#             ["git", "rev-list", "--ancestry-path", "branch_name"],
#             universal_newlines=True
#         ).splitlines()

#         # Analyze the commit history to determine if a rebase has occurred
#         # This is a placeholder logic, adjust as needed
#         for commit in commits:
#             # Check if commit has multiple parents, indicating a merge
#             parents = subprocess.check_output(
#                 ["git", "rev-list", "--parents", "-n", "1", commit],
#                 universal_newlines=True
#             ).split()

#             if len(parents) > 2:
#                 # More than one parent indicates a merge commit
#                 return False

#         # If no merge commits are found, assume it might be rebased
#         return True

#     except subprocess.CalledProcessError as e:
#         print(f"Error checking commit history: {e}")
#         return False

# def find_merged_commits_without_pr(main_repo, current_state, previous_state):
#     merged_without_pr = []

#     # Get the repo object for the main repository
#     repo = g.get_repo(main_repo)
#     main_branch_name = repo.default_branch

#     # Filter the current and previous states to only include the main repo's main branch
#     current_main_branch = next((b for b in current_state if b["repo_owner"] == main_repo.split('/')[0] and 
#                                 b["repo_name"] == main_repo.split('/')[1] and 
#                                 b["branch_name"] == main_branch_name), None)

#     previous_main_branch = next((b for b in previous_state if b["repo_owner"] == main_repo.split('/')[0] and 
#                                  b["repo_name"] == main_repo.split('/')[1] and 
#                                  b["branch_name"] == main_branch_name), None)

#     # Fetch all new commits in the main branch
#     previous_commit_hash = previous_main_branch["commit_hash"] if previous_main_branch else None
#     new_commits = fetch_commits(main_repo, main_branch_name, previous_commit_hash)
#     # print(new_commits)
#     # Fetch all new pull requests targeting the main branch
#     pulls = repo.get_pulls(state='closed', base=main_branch_name)
#     # print(pulls)
#     # Collect all PR commit SHAs
#     pr_commit_shas = set()
#     for pr in pulls:
#         pr_commits = pr.get_commits()
#         pr_commit_shas.update(commit.sha for commit in pr_commits)
#     # print(pr_commit_shas)
#     # Identify commits not associated with any PR
#     for commit in new_commits:
#         # print(commit)
#         # print(type(commit))
#         # Adjust the key name based on the actual structure
#         commit_sha = commit.get("sha") # Example adjustment
#         # print(commit_sha)
#         if commit_sha and commit_sha not in pr_commit_shas:
#             merged_without_pr.append(commit)

#     return merged_without_pr


# def fetch_commits(repo_full_name, branch_name, since_commit=None):
#     repo = g.get_repo(repo_full_name)
#     commits = []
#     for commit in repo.get_commits(sha=branch_name):
#         if since_commit and commit.sha == since_commit:
#             break
#         commits.append({
#             "name": commit.commit.message.split('\n')[0],
#             "link": commit.html_url,
#             "sha" : commit.sha
#         })
#     return commits

# def generate_report(new_branches, updated_branches, deleted_branches, rebased_branches):
#     report = "**Git Repository Update Report**\n\n"

#     if new_branches:
#         report += "**New branches:**\n"
#         for branch in new_branches:
#             if len(branch["commits"]) == 0:
#                 continue
#             repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
#             branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
#             report += f"\n{branch_url}\n"
#             report += "Commits:\n"
            
#             for commit in branch["commits"]:
#                 report += f"    {commit['name']} ({commit['link']} )\n"
    
#     if updated_branches:
#         report += "\n**Updated branches:**\n"
#         for branch in updated_branches:
#             repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
#             branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
#             report += f"\n{branch_url}\n"
#             report += "New commits:\n"
            
#             for commit in branch["commits"]:
#                 report += f"    {commit['name']} ({commit['link']} )\n"
    
#     if deleted_branches:
#         report += "\n**Deleted branches:**\n"
#         for branch in deleted_branches:
#             repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
#             branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
#             report += f"\n{branch_url}\n"
    
#     if rebased_branches:
#         report += "\n**Rebased branches:**\n"
#         for branch in rebased_branches:
#             repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
#             branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
#             report += f"\nBranch URL: {branch_url}\n"
#             report += "Commits :\n"
            
#             for commit in branch["commits"]:
#                 new_commit = commit['name']
#                 report += f"    {new_commit} ({commit['link']} )\n"
    
#     return report

# def post_to_discord(report, webhook_url):
#     chunks = [report[i:i+2000] for i in range(0, len(report), 2000)]
    
#     for chunk in chunks:
#         payload = {
#             "content": chunk
#         }
#         response = requests.post(webhook_url, json=payload)
#         if response.status_code != 204:
#             print(f"Failed to post to Discord. Status code: {response.status_code}")

# def update_database(current_state, db_name='branch_state.db'):
#     conn = sqlite3.connect(db_name)
#     cursor = conn.cursor()
    
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS branch_state (
#             repo_owner TEXT,
#             repo_name TEXT,
#             branch_name TEXT,
#             commit_hash TEXT,
#             PRIMARY KEY (repo_owner, repo_name, branch_name)
#         )
#     ''')
    
#     for branch in current_state:
#         cursor.execute('''
#             INSERT INTO branch_state (repo_owner, repo_name, branch_name, commit_hash)
#             VALUES (?, ?, ?, ?)
#             ON CONFLICT(repo_owner, repo_name, branch_name)
#             DO UPDATE SET commit_hash=excluded.commit_hash
#         ''', (branch['repo_owner'], branch['repo_name'], branch['branch_name'], branch['commit_hash']))
    
#     conn.commit()
#     conn.close()
# def generate_merged_commits_without_pr_report(merged_commits_without_pr):
#     report = "**Merged Commits Without Pull Request**\n\n"

#     if merged_commits_without_pr:
#         report += "The following commits were merged into the main branch without an associated pull request:\n"
#         for commit in merged_commits_without_pr:
#             report += f"- {commit['name']} ({commit['link']})\n"
#     else:
#         report += "No commits were merged without a pull request.\n"

#     return report

# def main():
#     main_repo = config.MAIN_REPO
#     forks = config.FORKS
#     repo_family = [main_repo] + forks
#     current_state = fetch_current_repo_state(repo_family)
#     previous_state = load_previous_state()
#     new_branches, updated_branches, deleted_branches, rebased_branches = compare_states(current_state, previous_state)
#     merged_without_pr = find_merged_commits_without_pr(main_repo, current_state, previous_state)
#     if merged_without_pr:
#         print("Merged branches without PR:", merged_without_pr)
    
#     if new_branches or updated_branches or deleted_branches or rebased_branches:
#         report = generate_report(new_branches, updated_branches, deleted_branches, rebased_branches)
#         report = chunk_report(report)
#         send_report_to_discord(report)
#     if merged_without_pr:
#         merged_commits_without_pr_report = generate_merged_commits_without_pr_report(merged_without_pr)
#         report = chunk_report(merged_commits_without_pr_report)
#         send_report_to_discord(report)


# if __name__ == "__main__":
#     main()




import os
from github import Github
import requests
import json
import sqlite3
# from discord_report import send_report_to_discord
import re
import config

def wrap_urls_with_angle_brackets(text):
    url_pattern = r'(https?://\S+)'
    parts = text.split('\n')
    wrapped_parts = []
    for part in parts:
        wrapped_part = re.sub(url_pattern, r'<\1>', part.strip())
        wrapped_parts.append(wrapped_part)
    return '\n'.join(wrapped_parts)

def chunk_report(report):
    DISCORD_MESSAGE_LIMIT = 2000
    report = wrap_urls_with_angle_brackets(report)
    chunks = []
    lines = report.split('\n')
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) + 1 > DISCORD_MESSAGE_LIMIT:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            if current_chunk:
                current_chunk += "\n" + line
            else:
                current_chunk = line

    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

GITHUB_TOKEN = config.git_access_token
g = Github(GITHUB_TOKEN)

def fetch_current_repo_state(repo_family):
    current_state = []
    for repo_full_name in repo_family:
        repo = g.get_repo(repo_full_name)
        branches = repo.get_branches()
        for branch in branches:
            current_state.append({
                "repo_owner": repo.owner.login,
                "repo_name": repo.name,
                "branch_name": branch.name,
                "commit_hash": branch.commit.sha
            })
    return current_state

def load_previous_state(db_name='branch_state.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT repo_owner, repo_name, branch_name, commit_hash
        FROM branch_state
    ''')
    previous_state = []
    for row in cursor.fetchall():
        previous_state.append({
            "repo_owner": row[0],
            "repo_name": row[1],
            "branch_name": row[2],
            "commit_hash": row[3]
        })
    conn.close()
    return previous_state

def save_current_state(current_state):
    with open("previous_state.json", "w") as f:
        json.dump(current_state, f)

def convert_commits(paginated_commits):
    return [{"name": commit.commit.message.split('\n')[0], "link": commit.html_url} for commit in paginated_commits]

def compare_states(current_state, previous_state):
    new_branches = []
    updated_branches = []
    deleted_branches = []
    rebased_branches = []
    current_branch_keys = {(b['repo_owner'], b['repo_name'], b['branch_name']) for b in current_state}
    
    for current_branch in current_state:
        repo_full_name = f"{current_branch['repo_owner']}/{current_branch['repo_name']}"
        repo = g.get_repo(repo_full_name)
        
        previous_branch = next((b for b in previous_state 
                                if b["repo_owner"] == current_branch["repo_owner"] 
                                and b["repo_name"] == current_branch["repo_name"] 
                                and b["branch_name"] == current_branch["branch_name"]), None)
        
        if previous_branch is None:
            default_branch = repo.default_branch
            comparison = repo.compare(default_branch, current_branch["branch_name"])
            if comparison.commits:
                new_branches.append({
                    "repo_owner": current_branch["repo_owner"],
                    "repo_name": current_branch["repo_name"],
                    "branch_name": current_branch["branch_name"],
                    "commit_hash": current_branch["commit_hash"],
                    "commits": convert_commits(comparison.commits)
                })
        elif current_branch["commit_hash"] != previous_branch["commit_hash"]:
            comparison = repo.compare(previous_branch["commit_hash"], current_branch["commit_hash"])
            if comparison.commits:
                updated_branches.append({
                    "repo_owner": current_branch["repo_owner"],
                    "repo_name": current_branch["repo_name"],
                    "branch_name": current_branch["branch_name"],
                    "current_commit_hash": current_branch["commit_hash"],
                    "previous_commit_hash": previous_branch["commit_hash"],
                    "commits": convert_commits(comparison.commits)
                })
                
                if is_rebased(comparison):
                    rebased_branches.append({
                        "repo_owner": current_branch["repo_owner"],
                        "repo_name": current_branch["repo_name"],
                        "branch_name": current_branch["branch_name"],
                        "commits": convert_commits(comparison.commits)
                    })
    
    for previous_branch in previous_state:
        if (previous_branch['repo_owner'], previous_branch['repo_name'], previous_branch['branch_name']) not in current_branch_keys:
            deleted_branches.append(previous_branch)
    
    return new_branches, updated_branches, deleted_branches, rebased_branches

def is_rebased(comparison):
    # Access the SHA of the base commit directly
    base_commit_sha = comparison.base_commit.sha
    
    # Get a set of commit SHAs from the comparison commits
    comparison_commit_shas = {commit.sha for commit in comparison.commits}
    
    # Determine if the branch is rebased by checking if the base commit is in the comparison commits
    if base_commit_sha not in comparison_commit_shas:
        return True  # If the base commit SHA is not among the comparison commits, it might be rebased
    
    return False


def find_merged_commits_without_pr(main_repo, current_state, previous_state):
    merged_without_pr = []

    repo = g.get_repo(main_repo)
    main_branch_name = repo.default_branch

    current_main_branch = next((b for b in current_state if b["repo_owner"] == main_repo.split('/')[0] and 
                                b["repo_name"] == main_repo.split('/')[1] and 
                                b["branch_name"] == main_branch_name), None)

    previous_main_branch = next((b for b in previous_state if b["repo_owner"] == main_repo.split('/')[0] and 
                                 b["repo_name"] == main_repo.split('/')[1] and 
                                 b["branch_name"] == main_branch_name), None)

    previous_commit_hash = previous_main_branch["commit_hash"] if previous_main_branch else None
    new_commits = fetch_commits(main_repo, main_branch_name, previous_commit_hash)
    
    pulls = repo.get_pulls(state='closed', base=main_branch_name)

    pr_commit_shas = set()
    for pr in pulls:
        pr_commits = pr.get_commits()
        pr_commit_shas.update(commit.sha for commit in pr_commits)

    for commit in new_commits:
        commit_sha = commit.get("sha")
        if commit_sha and commit_sha not in pr_commit_shas:
            merged_without_pr.append(commit)

    return merged_without_pr

def fetch_commits(repo_full_name, branch_name, since_commit=None):
    repo = g.get_repo(repo_full_name)
    commits = []
    for commit in repo.get_commits(sha=branch_name):
        if since_commit and commit.sha == since_commit:
            break
        commits.append({
            "name": commit.commit.message.split('\n')[0],
            "link": commit.html_url,
            "sha": commit.sha
        })
    return commits

def get_github_profile_image(repo_owner):
    url = f"https://api.github.com/users/{repo_owner}"
    response = requests.get(url)
    
    if response.status_code == 200:
        user_data = response.json()
        return user_data.get("avatar_url")
    else:
        return None
    
def generate_report(new_branches, updated_branches, deleted_branches, rebased_branches):
    fields = []

    if new_branches:
        new_field = {
            "name": f"\n\n🌿 **New branches and commits** 🌿\n\n\n",
            "value": "",
            "inline": False
        }
        for branch in new_branches:
            if len(branch["commits"]) == 0:
                continue
            avatar = get_github_profile_image(branch["repo_owner"])
            repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
            branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
            new_field["value"] += f"\n* **branch** : [{branch['branch_name']} [{repo_full_name}]]({branch_url})\n"
            # if avatar:
            #     new_field["value"] += f"![Profile Image]{avatar}\n"
            for i, commit in enumerate(branch["commits"]):
                if i:
                    new_field["value"] += f"\n * [{commit['name']}]({commit['link']})"
                else : 
                    new_field["value"] += f" * [{commit['name']}]({commit['link']})"
        fields.append(new_field)

    if updated_branches:
        updated_field = {
            "name": f"\n\n🌿 **Updated branches and commits** 🌿\n",
            "value": "",
            "inline": False
        }
        for branch in updated_branches:
            repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
            branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
            updated_field["value"] += f"\n* **branch** : [{branch['branch_name']} [{repo_full_name}]]({branch_url})\n"
            for i, commit in enumerate(branch["commits"]):
                if i:
                    updated_field["value"] += f"\n * [{commit['name']}]({commit['link']})"
                else : 
                    updated_field["value"] += f" * [{commit['name']}]({commit['link']})"
        fields.append(updated_field)

    if deleted_branches:
        deleted_field = {
            "name": f"\n\n🌿 **Deleted branches** 🌿\n",
            "value": "",
            "inline": False
        }
        for branch in deleted_branches:
            repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
            branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
            deleted_field["value"] += f"\n* **branch** : [{branch['branch_name']} [{repo_full_name}]]({branch_url})\n"
        fields.append(deleted_field)

    if rebased_branches:
        rebased_field = {
            "name": f"\n\n🌿 **Rebased branches and commits** 🌿\n",
            "value": "",
            "inline": False
        }
        for branch in rebased_branches:
            repo_full_name = f"{branch['repo_owner']}/{branch['repo_name']}"
            branch_url = f"https://github.com/{repo_full_name}/tree/{branch['branch_name']}"
            rebased_field["value"] += f"\n* **branch** : [{branch['branch_name']} [{repo_full_name}]]({branch_url})\n"
            for i, commit in enumerate(branch["commits"]):
                if i:
                    rebased_field["value"] += f"\n * [{commit['name']}]({commit['link']})"
                else : 
                    rebased_field["value"] += f" * [{commit['name']}]({commit['link']})"
        fields.append(rebased_field)

    embed = {
        "title": "🌟 __ BRANCH REPORT __ 🌟",
        "description": "This is a report of branch activities.",
        "color": 642600,  # Hex color code in decimal
        "fields": fields,
        "thumbnail": {
            "url": "https://example.com/image.png"
        },
        # "footer": {
        #     "text": "This is a footer text"
        # }
    }

    return embed


def post_to_discord(embed, webhook_url):
    data = {
        "embeds": [embed]
    }

    response = requests.post(webhook_url, data=json.dumps(data), headers={"Content-Type": "application/json"})
    return response.status_code, response.text


def update_database(current_state, db_name='branch_state.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS branch_state (
            repo_owner TEXT,
            repo_name TEXT,
            branch_name TEXT,
            commit_hash TEXT,
            PRIMARY KEY (repo_owner, repo_name, branch_name)
        )
    ''')
    
    for branch in current_state:
        cursor.execute('''
            INSERT INTO branch_state (repo_owner, repo_name, branch_name, commit_hash)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(repo_owner, repo_name, branch_name)
            DO UPDATE SET commit_hash=excluded.commit_hash
        ''', (branch['repo_owner'], branch['repo_name'], branch['branch_name'], branch['commit_hash']))
    
    conn.commit()
    conn.close()

def generate_merged_commits_without_pr_report(merged_commits_without_pr):
    field = {
        "name": "The following commits were merged into the main branch without an associated pull request:\n\n",
        "value": "",
        "inline": False
    }

    if merged_commits_without_pr:
        for i, commit in enumerate(merged_commits_without_pr):
            if i:
                field["value"] += f"\n* [{commit['name']}]({commit['link']})"
            else : 
                field["value"] += f"* [{commit['name']}]({commit['link']})"
    else:
        field["value"] += "No commits were merged without a pull request.\n"

    embed = {
        "title": "🔥 **MERGED COMMITS WITHOUT PR** 🔥",
        "color": 12910592,  # Hex color code in decimal
        "fields": [field],
        "thumbnail": {
            "url": "https://example.com/image.png"
        },
        # "footer": {
        #     "text": "This is a footer text"
        # }
    }

    return embed

def branch_report():
    main_repo = config.MAIN_REPO
    forks = config.FORKS
    webhook = config.DISCORD_WEBHOOK_URL
    repo_family = [main_repo] + forks
    current_state = fetch_current_repo_state(repo_family)
    previous_state = load_previous_state()
    new_branches, updated_branches, deleted_branches, rebased_branches = compare_states(current_state, previous_state)
    merged_without_pr = find_merged_commits_without_pr(main_repo, current_state, previous_state)
    
    if merged_without_pr:
        print("Merged branches without PR:", merged_without_pr)
    
    if new_branches or updated_branches or deleted_branches or rebased_branches:
        report = generate_report(new_branches, updated_branches, deleted_branches, rebased_branches)
        # report = chunk_report(report)
        post_to_discord(report, webhook)
        # return report

    if merged_without_pr:
        merged_commits_without_pr_report = generate_merged_commits_without_pr_report(merged_without_pr)
        post_to_discord(merged_commits_without_pr_report, webhook)
    # update_database(current_state)
if __name__ == "__main__":
    branch_report()
