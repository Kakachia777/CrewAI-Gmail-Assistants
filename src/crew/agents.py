import os
from functools import lru_cache
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.get_thread import GmailGetThread
from langchain_community.tools.tavily_search import TavilySearchResults
from textwrap import dedent
from crewai import Agent
from .tools import CreateDraftTool

os.environ["OPENAI_MODEL_NAME"]="gpt-4o-mini"


class EmailFilterAgents():
    def __init__(self):
        self._gmail = None

    @property
    @lru_cache(maxsize=1)
    def gmail(self):
        if not self._gmail:
            self._gmail = GmailToolkit()
        return self._gmail

    def _create_base_agent(self, role, goal, backstory, tools=None):
        return Agent(
            role=role,
            goal=goal,
            backstory=dedent(backstory),
            tools=tools,
            verbose=True,
            allow_delegation=False
        )

    def email_filter_agent(self):
        return self._create_base_agent(
            role='Senior Email Analyst',
            goal='Filter out non-essential emails',
            backstory="""
                As a Senior Email Analyst, you have extensive experience in email content analysis.
                You are adept at distinguishing important emails from spam, newsletters, and other
                irrelevant content."""
        )

    def email_action_agent(self):
        return self._create_base_agent(
            role='Email Action Specialist',
            goal='Identify action-required emails and compile a list of their IDs',
            backstory="""
                With a keen eye for detail and a knack for understanding context, you specialize
                in identifying emails that require immediate action. Your skill set includes interpreting
                the urgency and importance of an email based on its content and context."""
        )

    def email_response_writer(self):
        return self._create_base_agent(
            role='Email Response Writer',
            goal='Draft responses to action-required emails',
            backstory="""
                You are a skilled writer, adept at crafting clear, concise, and effective email responses.
                Your strength lies in your ability to communicate effectively, ensuring that each response is
                tailored to address the specific needs and context of the email."""
        )

    def complaint_categorizer_agent(self):
        return self._create_base_agent(
            role='Complaint Categorizer',
            goal='Categorize emails that contain customer complaints',
            backstory="""
                As a Complaint Categorizer, you have the ability to detect and categorize emails containing customer complaints.
                Your role is crucial in ensuring that all complaints are identified and processed appropriately."""
        )

    def complaint_summarizer_agent(self):
        return self._create_base_agent(
            role='Complaint Summarizer',
            goal='Summarize the contents of complaint emails',
            backstory="""
                As a Complaint Summarizer, your expertise lies in extracting the essence of customer complaints
                and summarizing them concisely."""
        )

    def complaint_comparison_agent(self):
        return self._create_base_agent(
            role='Complaint Comparison Specialist',
            goal='Compare new complaints against existing ones and count similar complaints',
            backstory="""
                As a Complaint Comparison Specialist, you ensure that recurring complaints are tracked and documented.
                Your role involves comparing new complaints with existing ones and updating the count of similar complaints."""
        )
