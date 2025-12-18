from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Create LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Define prompt
prompt =PromptTemplate(input_variable=["feature"],
                       template="""
You are a QA Engineer.
Write detailed test cases for the following feature:
{feature}

Include:
- Positive cases
- Negative cases
- Edge cases
""")

#create chain
chain = prompt | llm

# Invoke
response = chain.invoke({
    "feature": "Login page with email and password"
})

print(response.content)
