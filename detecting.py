from github import Github
import re


def format_report_prs(prs, main_repo):
    report_lines = []
    for pr_number in prs:
        # Retrieve the pull request object using the PR number
        pr = main_repo.get_pull(pr_number)
        
        # Now you can get the commits from the PR object
        commits = pr.get_commits()
        commit_list = [
            f"* {commit.commit.message.splitlines()[0]} ({commit.html_url} )"
            for commit in commits
        ]
        pr_line = f"#{pr.number} {pr.title} https://github.com/{pr.head.repo.full_name}/tree/{pr.head.ref} :arrow_right: https://github.com/{pr.base.repo.full_name}/tree/{pr.base.ref}"
        commit_lines = '\n'.join(commit_list)
        report_lines.append(f"{pr_line}\ncommits:\n{commit_lines}\n")
    return '\n'.join(report_lines)

def wrap_urls_with_angle_brackets(text):
    # Regular expression to match URLs
    url_pattern = r'(https?://\S+)'
    
    # Split the text by the arrow (:arrow_right:)
    parts = text.split(':arrow_right:')
    print(parts)
    # Wrap URLs in each part
    wrapped_parts = []
    for part in parts:
        wrapped_part = re.sub(url_pattern, r'<\1>', part.strip())
        wrapped_parts.append(wrapped_part)
    
    # Join the parts back with the arrow
    return ' :arrow_right: '.join(wrapped_parts)

def chanking_report(report):
    # Discord message limit
    DISCORD_MESSAGE_LIMIT = 2000

    # Function to wrap URLs with angle brackets


    # Wrap URLs in the entire report
    report = wrap_urls_with_angle_brackets(report)

    # Split the report into chunks
    chunks = []
    lines = report.split('\n')
    current_chunk = ""

    for line in lines:
        # Check if adding the line would exceed the limit
        if len(current_chunk) + len(line) + 1 > DISCORD_MESSAGE_LIMIT:
            # If it would, save the current chunk and start a new one
            chunks.append(current_chunk)
            current_chunk = line
        else:
            # Otherwise, add the line to the current chunk
            if current_chunk:
                current_chunk += "\n" + line
            else:
                current_chunk = line

    # Don't forget to add the last chunk
    if current_chunk:
        chunks.append(current_chunk)
    return chunks
    # Send each chunk as a separate message




def find_open_merged_pr(previous_state, current_state, main_repo):
    merged_prs = []
    unmerged_prs = []
    open_prs = []

    # Extract previous and current PR states
    prev_prs = previous_state['prs']
    curr_prs = current_state['prs']
    print(prev_prs)
    print(curr_prs)

    # Check for new PRs in the current state
    for pr_number, curr_state in curr_prs.items():
        if pr_number not in prev_prs:
            if curr_state == 'open':
                open_prs.append(pr_number)
            elif curr_state == 'closed':
                # Check if the PR is merged
                pr = main_repo.get_pull(pr_number)
                if pr.merged:  # Replace with actual check for merge status
                    merged_prs.append(pr_number)
                else:
                    unmerged_prs.append(pr_number)

    # Check existing PRs for state changes
    for pr_number, prev_state in prev_prs.items():
        curr_state = curr_prs.get(pr_number)
        
        if curr_state and prev_state == 'open' and curr_state == 'closed':
            # Check if the PR is merged
            pr = main_repo.get_pull(pr_number)
            if pr.merged:  # Replace with actual check for merge status
                merged_prs.append(pr_number)
            else:
                unmerged_prs.append(pr_number)

    report_merged_prs = format_report_prs(merged_prs, main_repo)
    report_faild_prs = format_report_prs(unmerged_prs, main_repo)
    report_open_prs = format_report_prs(open_prs, main_repo)
    print(report_merged_prs)
    print(type(report_merged_prs))
    report_merged_prs = chanking_report(report_merged_prs)
    report_faild_prs = chanking_report(report_faild_prs)
    report_open_prs = chanking_report(report_open_prs)

    print(merged_prs)
    print(unmerged_prs)
    print(open_prs)
    print(report_merged_prs)
    # exit(0)
    return report_merged_prs, report_open_prs, report_faild_prs
    

