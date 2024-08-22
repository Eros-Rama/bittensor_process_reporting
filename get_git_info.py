import requests

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = ""

def get_branches(owner, repo):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/branches"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json()

def get_pull_requests(owner, repo):
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Example usage
branches = get_branches("opentensor", "bittensor")
pull_requests = get_pull_requests("opentensor", "bittensor")
print(len(branches))
print(branches[0])
print("\n\n")
print(len(pull_requests))
print(pull_requests[0])

































# {
#     'url',
#     'id',
#     'node_id',
#     'html_url',
#     'diff_url',
#     'patch_url',
#     'issue_url',
#     'number',
#     'state',
#     'locked',
#     'title',
#     'user': {
#         'login',
#         'id',
#         'node_id',
#         'avatar_url',
#         'gravatar_id',
#         'url',
#         'html_url',
#         'followers_url',
#         'following_url',
#         'gists_url',
#         'starred_url',
#         'subscriptions_url',
#         'organizations_url',
#         'repos_url',
#         'events_url',
#         'received_events_url',
#         'type',
#         'site_admin'
#     },
#     'body',
#     'created_at',
#     'updated_at',
#     'closed_at',
#     'merged_at',
#     'merge_commit_sha',
#     'assignee': {
#         'login',
#         'id',
#         'node_id',
#         'avatar_url',
#         'gravatar_id',
#         'url',
#         'html_url',
#         'followers_url',
#         'following_url',
#         'gists_url',
#         'starred_url',
#         'subscriptions_url',
#         'organizations_url',
#         'repos_url',
#         'events_url',
#         'received_events_url',
#         'type',
#         'site_admin'
#     },
#     'assignees': [
#         {
#             'login',
#             'id',
#             'node_id',
#             'avatar_url',
#             'gravatar_id',
#             'url',
#             'html_url',
#             'followers_url',
#             'following_url',
#             'gists_url',
#             'starred_url',
#             'subscriptions_url',
#             'organizations_url',
#             'repos_url',
#             'events_url',
#             'received_events_url',
#             'type',
#             'site_admin'
#         }
#     ],
#     'requested_reviewers': [
#         {
#             'login',
#             'id',
#             'node_id',
#             'avatar_url',
#             'gravatar_id',
#             'url',
#             'html_url',
#             'followers_url',
#             'following_url',
#             'gists_url',
#             'starred_url',
#             'subscriptions_url',
#             'organizations_url',
#             'repos_url',
#             'events_url',
#             'received_events_url',
#             'type',
#             'site_admin'
#         }
#     ],
#     'requested_teams',
#     'labels': [
#         {
#             'id',
#             'node_id',
#             'url',
#             'name',
#             'color',
#             'default',
#             'description'
#         }
#     ],
#     'milestone',
#     'draft',
#     'commits_url',
#     'review_comments_url',
#     'review_comment_url',
#     'comments_url',
#     'statuses_url',
#     'head': {
#         'label',
#         'ref',
#         'sha',
#         'user': {
#             'login',
#             'id',
#             'node_id',
#             'avatar_url',
#             'gravatar_id',
#             'url',
#             'html_url',
#             'followers_url',
#             'following_url',
#             'gists_url',
#             'starred_url',
#             'subscriptions_url',
#             'organizations_url',
#             'repos_url',
#             'events_url',
#             'received_events_url',
#             'type',
#             'site_admin'
#         },
#         'repo': {
#             'id',
#             'node_id',
#             'name',
#             'full_name',
#             'private',
#             'owner': {
#                 'login',
#                 'id',
#                 'node_id',
#                 'avatar_url',
#                 'gravatar_id',
#                 'url',
#                 'html_url',
#                 'followers_url',
#                 'following_url',
#                 'gists_url',
#                 'starred_url',
#                 'subscriptions_url',
#                 'organizations_url',
#                 'repos_url',
#                 'events_url',
#                 'received_events_url',
#                 'type',
#                 'site_admin'
#             },
#             'html_url',
#             'description',
#             'fork',
#             'url',
#             'forks_url',
#             'keys_url',
#             'collaborators_url',
#             'teams_url',
#             'hooks_url',
#             'issue_events_url',
#             'events_url',
#             'assignees_url',
#             'branches_url',
#             'tags_url',
#             'blobs_url',
#             'git_tags_url',
#             'git_refs_url',
#             'trees_url',
#             'statuses_url',
#             'languages_url',
#             'stargazers_url',
#             'contributors_url',
#             'subscribers_url',
#             'subscription_url',
#             'commits_url',
#             'git_commits_url',
#             'comments_url',
#             'issue_comment_url',
#             'contents_url',
#             'compare_url',
#             'merges_url',
#             'archive_url',
#             'downloads_url',
#             'issues_url',
#             'pulls_url',
#             'milestones_url',
#             'notifications_url',
#             'labels_url',
#             'releases_url',
#             'deployments_url',
#             'created_at',
#             'updated_at',
#             'pushed_at',
#             'git_url',
#             'ssh_url',
#             'clone_url',
#             'svn_url',
#             'homepage',
#             'size',
#             'stargazers_count',
#             'watchers_count',
#             'language',
#             'has_issues',
#             'has_projects',
#             'has_downloads',
#             'has_wiki',
#             'has_pages',
#             'has_discussions',
#             'forks_count',
#             'mirror_url',
#             'archived',
#             'disabled',
#             'open_issues_count',
#             'license': {
#                 'key',
#                 'name',
#                 'spdx_id',
#                 'url',
#                 'node_id'
#             },
#             'allow_forking',
#             'is_template',
#             'web_commit_signoff_required',
#             'topics',
#             'visibility',
#             'forks',
#             'open_issues',
#             'watchers',
#             'default_branch'
#         }
#     },
#     'base': {
#         'label',
#         'ref',
#         'sha',
#         'user': {
#             'login',
#             'id',
#             'node_id',
#             'avatar_url',
#             'gravatar_id',
#             'url',
#             'html_url',
#             'followers_url',
#             'following_url',
#             'gists_url',
#             'starred_url',
#             'subscriptions_url',
#             'organizations_url',
#             'repos_url',
#             'events_url',
#             'received_events_url',
#             'type',
#             'site_admin'
#         },
#         'repo': {
#             'id',
#             'node_id',
#             'name',
#             'full_name',
#             'private',
#             'owner': {
#                 'login',
#                 'id',
#                 'node_id',
#                 'avatar_url',
#                 'gravatar_id',
#                 'url',
#                 'html_url',
#                 'followers_url',
#                 'following_url',
#                 'gists_url',
#                 'starred_url',
#                 'subscriptions_url',
#                 'organizations_url',
#                 'repos_url',
#                 'events_url',
#                 'received_events_url',
#                 'type',
#                 'site_admin'
#             },
#             'html_url',
#             'description',
#             'fork',
#             'url',
#             'forks_url',
#             'keys_url',
#             'collaborators_url',
#             'teams_url',
#             'hooks_url',
#             'issue_events_url',
#             'events_url',
#             'assignees_url',
#             'branches_url',
#             'tags_url',
#             'blobs_url',
#             'git_tags_url',
#             'git_refs_url',
#             'trees_url',
#             'statuses_url',
#             'languages_url',
#             'stargazers_url',
#             'contributors_url',
#             'subscribers_url',
#             'subscription_url',
#             'commits_url',
#             'git_commits_url',
#             'comments_url',
#             'issue_comment_url',
#             'contents_url',
#             'compare_url',
#             'merges_url',
#             'archive_url',
#             'downloads_url',
#             'issues_url',
#             'pulls_url',
#             'milestones_url',
#             'notifications_url',
#             'labels_url',
#             'releases_url',
#             'deployments_url',
#             'created_at',
#             'updated_at',
#             'pushed_at',
#             'git_url',
#             'ssh_url',
#             'clone_url',
#             'svn_url',
#             'homepage',
#             'size',
#             'stargazers_count',
#             'watchers_count',
#             'language',
#             'has_issues',
#             'has_projects',
#             'has_downloads',
#             'has_wiki',
#             'has_pages',
#             'has_discussions',
#             'forks_count',
#             'mirror_url',
#             'archived',
#             'disabled',
#             'open_issues_count',
#             'license': {
#                 'key',
#                 'name',
#                 'spdx_id',
#                 'url',
#                 'node_id'
#             },
#             'allow_forking',
#             'is_template',
#             'web_commit_signoff_required',
#             'topics',
#             'visibility',
#             'forks',
#             'open_issues',
#             'watchers',
#             'default_branch'
#         }
#     },
#     '_links': {
#         'self': {
#             'href'
#         },
#         'html': {
#             'href'
#         },
#         'issue': {
#             'href'
#         },
#         'comments': {
#             'href'
#         },
#         'review_comments': {
#             'href'
#         },
#         'review_comment': {
#             'href'
#         },
#         'commits': {
#             'href'
#         },
#         'statuses': {
#             'href'
#         }
#     }
# }
