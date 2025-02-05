# Ticket Priorities
PRIORITY_LOW = 1
PRIORITY_MEDIUM = 2
PRIORITY_HIGH = 3

# Priority Indicators
PRIORITY_INDICATORS = {
    'High': '🔴',
    'Medium': '🟠',
    'Low': '🟢',
    'Emergency': '🆘'
}

# Ticket Status IDs
STATUS_NEW = 1
STATUS_ASSIGNED = 2
STATUS_IN_PROGRESS = 3
STATUS_CLOSED = 4

# Status Names
STATUS_NAMES = {
    STATUS_NEW: 'New',
    STATUS_ASSIGNED: 'Assigned',
    STATUS_IN_PROGRESS: 'In Progress',
    STATUS_CLOSED: 'Closed'
}

# Error Messages
ERROR_MESSAGES = {
    'auth_failed': 'Authentication failed. Please check your credentials.',
    'ticket_not_found': 'Ticket not found.',
    'invalid_email': 'Invalid email address.',
    'invalid_ticket_id': 'Invalid ticket ID.',
    'permission_denied': 'You do not have permission to perform this action.',
    'duo_required': 'Duo authentication required. Please contact IT support.',
} 