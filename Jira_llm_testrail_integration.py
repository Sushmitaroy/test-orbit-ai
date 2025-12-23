import requests
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import json

load_dotenv()

#  Fetch jira details from .env file

JIRA_URL = os.getenv("JIRA_URL")
JIRA_ISSUE_KEY = os.getenv("JIRA_ISSUE_KEY")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_KEY = os.getenv("JIRA_API_KEY")

response = requests.get(f"{JIRA_URL}/rest/api/3/issue/{JIRA_ISSUE_KEY}",
    auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_KEY))

print(response.status_code)

issue = response.json() #stores response in json
requirement_text = f"""
Title: {issue['fields']['summary']}
Description: {issue['fields']['description']}
"""

print(requirement_text)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

prompt = PromptTemplate(
    input_variables=["feature"],
    template="""
You are a QA Engineer.

Return ONLY valid JSON.
Do not include explanations, text, markdown, or comments.

Include:
- Positive cases
- Negative cases
- Edge cases

Output format:
[
  {{
    "title": "string",
    "custom_steps": "- Step 1\\n- Step 2\\n- Step 3"
    ]
  }}
]

Feature:
{feature}
"""
)

chain = prompt | llm

response = chain.invoke({
    "feature": requirement_text})

raw_output = response.content
print("LLM OUTPUT:\n", raw_output)

# Convert JSON string → Python list
testcases = json.loads(raw_output)


# Fetch testrail details from .env file

TESTRAIL_URL = os.getenv("TESTRAIL_URL")
TESTRAIL_PROJECT_ID = os.getenv("TESTRAIL_PROJECT_ID")
TESTRAIL_SECTION_ID = os.getenv("TESTRAIL_SECTION_ID")
TESTRAIL_USER = os.getenv("TESTRAIL_USER")
TESTRAIL_API_KEY = os.getenv("TESTRAIL_API_KEY")


def add_test_case(testcase):
    response = requests.post(
        f"{TESTRAIL_URL}/index.php?/api/v2/add_case/{TESTRAIL_SECTION_ID}",
        auth=HTTPBasicAuth(TESTRAIL_USER, TESTRAIL_API_KEY),
        headers={"Content-Type": "application/json"},
        json=testcase
    )

    print("Status:", response.status_code)
    print("Response:", response.text)

    return response

for testcase in testcases:
    add_test_case(testcase)









