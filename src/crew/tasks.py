from crewai import Task
from textwrap import dedent
from typing import List, Dict


class EmailFilterTasks:
	@staticmethod
	def _create_task(description: str, agent) -> Task:
		return Task(
			description=dedent(description),
			agent=agent
		)

	def filter_emails_task(self, agent, emails: List[Dict]) -> Task:
		return self._create_task(
			f"""
			Analyze a batch of emails and filter out non-essential ones.
			
			EMAILS
			-------
			{self._format_emails(emails)}
			
			Your final answer MUST be the relevant thread_ids and sender, use bullet points.
			""",
			agent
		)

	@staticmethod
	def _format_emails(emails: List[Dict]) -> str:
		return "\n".join(
			f"ID: {email['id']}\n"
			f"- Thread ID: {email['threadId']}\n"
			f"- Snippet: {email['snippet']}\n"
			f"- From: {email['sender']}\n"
			f"--------"
			for email in emails
		)

	def action_required_emails_task(self, agent):
		return Task(
			description=dedent("""\
				For each email thread, pull and analyze the complete threads using only the actual Thread ID.
				understand the context, key points, and the overall sentiment
				of the conversation.

				Identify the main query or concerns that needs to be
				addressed in the response for each

				Your final answer MUST be a list for all emails with:
				- the thread_id
				- a summary of the email thread
				- a highlighting with the main points
				- identify the user and who he will be answering to
				- communication style in the thread
				- the sender's email address
				"""),
			agent=agent
		)

	def draft_responses_task(self, agent):
		return Task(
			description=dedent(f"""\
				Based on the action-required emails identified, draft responses for each.
				Ensure that each response is tailored to address the specific needs
				and context outlined in the email.

				- Assume the persona of the user and mimic the communication style in the thread.
				- Feel free to do research on the topic to provide a more detailed response, IF NECESSARY.
				- IF a research is necessary do it BEFORE drafting the response.
				- If you need to pull the thread again do it using only the actual Thread ID.

				Use the tool provided to draft each of the responses.
				When using the tool pass the following input:
				- to (sender to be responded)
				- subject
				- message

				You MUST create all drafts before sending your final answer.
				Your final answer MUST be a confirmation that all responses have been drafted.
				"""),
			agent=agent
		)

	def categorize_complaints_task(self, agent, emails):
		return Task(
			description=dedent(f"""\
	            Analyze the following emails and categorize those that contain customer complaints.

	            EMAILS
	            -------
	            {emails}

	            Your final answer MUST include the categorized complaint emails."""),
			agent=agent
		)

	def summarize_complaints_task(self, agent, complaints):
		return Task(
			description=dedent(f"""\
	            Summarize the contents of the following complaint emails.

	            COMPLAINT EMAILS
	            -------
	            {complaints}

	            Your final answer MUST include the summaries of the complaints."""),
			agent=agent
		)

	def compare_complaints_task(self, agent, new_complaints, existing_complaints):
		return Task(
			description=dedent(f"""\
	            Compare the new complaints against existing complaints and count the number of similar complaints.

	            NEW COMPLAINTS
	            -------
	            {new_complaints}

	            EXISTING COMPLAINTS
	            -------
	            {existing_complaints}

	            Your final answer MUST include the updated complaint counts and any new complaints."""),
			agent=agent
		)
