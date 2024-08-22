from discord_report import send_report_to_discord

# Example report
report = [
    "Daily Report",
    "============",
    "Tasks Completed: 5",
    "Issues Found: 2",
    "Pending Tasks: 3"
]

# Send the report to Discord
send_report_to_discord(report)
