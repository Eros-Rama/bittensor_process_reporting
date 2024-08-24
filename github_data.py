# github_data.py
from github import Github
import config
import config
def get_repo_data():
    access_token = config.git_access_token 
    g = Github(access_token)
    main_repo = g.get_repo(config.MAIN_REPO)
    forks = [g.get_repo(fork) for fork in config.FORKS]
    fork_branches = {fork.full_name: fork.get_branches() for fork in forks}
    # exit(0)
    return fork_branches, main_repo




if __name__ == "__main__":
    get_repo_data()
