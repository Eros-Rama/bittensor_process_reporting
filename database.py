import sqlite3
import json
from github import Github

def load_previous_state():
    conn = sqlite3.connect('state.db')
    c = conn.cursor()

    # Ensure the table exists
    c.execute('''CREATE TABLE IF NOT EXISTS state (data TEXT)''')

    # Fetch the single item from the table
    c.execute('SELECT data FROM state LIMIT 1')
    row = c.fetchone()
    conn.close()

    # Return the previous state as a dictionary, or initialize if empty
    if row and row[0]:
        print(row[0])
        print(type(row[0]))
        try:
            return_cur = row[0].replace("'", '"')
            return json.loads(return_cur)
        except json.JSONDecodeError:
            print("Error decoding JSON from database. Returning default state.")
            return {"branches": [], "prs": []}
    else:
        return {"branches": [], "prs": []}

def update_database(current_state):
    conn = sqlite3.connect('state.db')
    c = conn.cursor()

    # Convert the current state to a JSON string
    json_data = json.dumps(current_state)

    # Clear the existing entry and insert the new state
    c.execute('DELETE FROM state')
    c.execute('INSERT INTO state (data) VALUES (?)', (json_data,))
    conn.commit()
    conn.close()


def fetch_github_branches_and_commits(repo_owner, repo_name, access_token=None):
    # Initialize the GitHub client
    g = Github(access_token)
    main_repo = g.get_repo(f"{repo_owner}/{repo_name}")

    # Fetch branches and their latest commit hashes
    branches = {branch.name: branch.commit.sha for branch in main_repo.get_branches()}
    return branches

def update_database_with_branches(new_data=None, db_name='branch_state.db'):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Update the branch state data
    if new_data:
        for branch_name, commit_hash in new_data.items():
            cursor.execute('''
                INSERT INTO branch_state (branch_name, commit_hash)
                VALUES (?, ?)
                ON CONFLICT(branch_name) DO UPDATE SET commit_hash=excluded.commit_hash
            ''', (branch_name, commit_hash))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# if __name__ == "__main__":
#     # Fetch the latest branches and commits from the GitHub repository
#     repo_owner = 'Eros-Rama'
#     repo_name = 'bittensor'
#     access_token = ''  # Replace with your GitHub access token if needed
#     latest_branch_data = fetch_github_branches_and_commits(repo_owner, repo_name, access_token)

#     # Update the database with the latest branch data
#     update_database_with_branches(new_data=latest_branch_data)
