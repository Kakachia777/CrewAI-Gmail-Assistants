import datetime
from typing import TypedDict, List, Dict
from dataclasses import dataclass

@dataclass
class Email:
	id: str
	thread_id: str
	snippet: str
	sender: str
	timestamp: datetime

class EmailsState(TypedDict):
	checked_emails_ids: List[str]
	emails: List[Email]
	action_required_emails: Dict[str, Dict]
	complaint_emails: List[Email]
	summaries: List[str]
	last_check_time: datetime
