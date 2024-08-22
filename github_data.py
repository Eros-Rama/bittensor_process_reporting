# github_data.py
from github import Github
import config

def get_repo_data():
    g = Github("")
    main_repo = g.get_repo(config.MAIN_REPO)
    forks = [g.get_repo(fork) for fork in config.FORKS]

    # print(main_repo)

    # Get branches and PRs
    main_branches = main_repo.get_branches()
    main_prs = main_repo.get_pulls(state='all')


    fork_branches = {fork.full_name: fork.get_branches() for fork in forks}
    print(main_branches)
    # exit(0)
    return main_branches, main_prs, fork_branches, main_repo




if __name__ == "__main__":
    get_repo_data()
