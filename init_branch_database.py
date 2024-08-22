import sqlite3
from github import Github

def fetch_github_branches_and_commits(repo_owner, repo_name, access_token=None):
    # Initialize the GitHub client
    g = Github(access_token)
    main_repo = g.get_repo(f"{repo_owner}/{repo_name}")

    # Fetch branches and their latest commit hashes
    branches = {branch.name: branch.commit.sha for branch in main_repo.get_branches()}
    return branches

def initialize_database_with_branches(existing_data=None, db_name='branch_state.db'):
    # Connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Drop the table if it exists (useful for development/testing)
    cursor.execute('DROP TABLE IF EXISTS branch_state')

    # Create the table with the correct schema
    cursor.execute('''
        CREATE TABLE branch_state (
            branch_name TEXT PRIMARY KEY,
            commit_hash TEXT
        )
    ''')

    # Insert the initial branch data into the table
    if existing_data:
        for branch_name, commit_hash in existing_data.items():
            cursor.execute('''
                INSERT INTO branch_state (branch_name, commit_hash)
                VALUES (?, ?)
                ON CONFLICT(branch_name) DO UPDATE SET commit_hash=excluded.commit_hash
            ''', (branch_name, commit_hash))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Fetch branches and commits from the GitHub repository
    repo_owner = 'Eros-Rama'
    repo_name = 'bittensor'
    access_token = ''  # Replace with your GitHub access token if needed
    branch_data = fetch_github_branches_and_commits(repo_owner, repo_name, access_token)

    # Initialize the database with the fetched branch data
    initialize_database_with_branches(existing_data=branch_data)
