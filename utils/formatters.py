def format_ticket_message(ticket, include_details=False):
    """Format ticket information for Slack messages"""
    priority_indicator = get_priority_indicator(ticket['Priority'], ticket.get('IsEmergency', False))
    
    message = (
        f"{priority_indicator} *Ticket #{ticket['ID']}*\n"
        f"*{ticket['Title']}*\n"
        f"Status: {ticket['Status']} | Priority: {ticket['Priority']}\n"
    )
    
    if include_details and ticket.get('Description'):
        message += f"\n>Description: {ticket['Description']}\n"
    
    return message 