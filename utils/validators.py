import re
from typing import Tuple

def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format"""
    if not email:
        return False, "Email cannot be empty"
    
    # Check for umich.edu domain
    if not email.endswith('@umich.edu'):
        return False, "Only @umich.edu email addresses are allowed"
    
    # Basic email format validation
    email_pattern = r'^[a-zA-Z0-9._%+-]+@umich\.edu$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format"
    
    return True, ""

def validate_ticket_id(ticket_id: str) -> Tuple[bool, str]:
    """Validate ticket ID format"""
    if not ticket_id:
        return False, "Ticket ID cannot be empty"
    
    if not ticket_id.isdigit():
        return False, "Ticket ID must be a number"
    
    return True, "" 