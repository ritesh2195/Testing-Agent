import os
from dotenv import load_dotenv

load_dotenv()  # loads .env if present

# Jira
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # change if needed

# Paths
FRAMEWORK_PATH = os.getenv("FRAMEWORK_PATH", "./sample_framework")
GIT_REPO_PATH = os.getenv("GIT_REPO_PATH", "./repo")

# Polling
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "60"))  # seconds
MAX_WORKERS = int(os.getenv("MAX_WORKERS", "3"))

# Notifications
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "")
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "sender@example.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT", "qa-team@example.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))

# TestRail (optional)
TESTRAIL_URL = os.getenv("TESTRAIL_URL", "")
TESTRAIL_PROJECT_ID = os.getenv("TESTRAIL_PROJECT_ID", "1")
TESTRAIL_USER = os.getenv("TESTRAIL_USER", "")
TESTRAIL_API_KEY = os.getenv("TESTRAIL_API_KEY", "")