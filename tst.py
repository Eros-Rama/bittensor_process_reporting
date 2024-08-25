import os
import subprocess
import requests

# Change to the directory where you want to create the Git repository
os.chdir('/Users/mac/Documents/Rhef task/monitoring_development_progress')

# Initialize the Git repository
subprocess.run(['git', 'init'])

# Create a new Python file
with open('tst.py', 'w') as file:
    file.write('print("Hello, world!")')

# Add the file to the Git repository
subprocess.run(['git', 'add', 'tst.py'])

# Commit the initial code
subprocess.run(['git', 'commit', '-m', 'Initial commit'])

# Define the GitHub repository details
repo_owner = 'owner_username'
repo_name = 'repository_name'

# Make a GET request to the GitHub API to fetch the commits
response = requests.get(f'https://api.github.com/repos/{repo_owner}/{repo_name}/commits')

# Check if the request was successful
if response.status_code == 200:
    commits = response.json()
    for commit in commits:
        commit_message = commit['commit']['message']
        commit_author = commit['commit']['author']['name']
        commit_date = commit['commit']['author']['date']
        print(f'Commit Message: {commit_message}')
        print(f'Commit Author: {commit_author}')
        print(f'Commit Date: {commit_date}')
else:
        print('Failed to fetch commits from GitHub API')