from typing import List, Dict, Any

class SlackMessageBuilder:
    @staticmethod
    def create_section(text: str) -> Dict[str, Any]:
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        }

    @staticmethod
    def create_button(text: str, action_id: str, value: str) -> Dict[str, Any]:
        return {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": text
            },
            "action_id": action_id,
            "value": value
        }

    @staticmethod
    def create_ticket_view(ticket: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create a detailed ticket view"""
        blocks = []
        
        # Header
        blocks.append({
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"Ticket #{ticket['ID']}"
            }
        })
        
        # Title and Status
        blocks.append({
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Title:*\n{ticket['Title']}"
                },
                {
                    "type": "mrkdwn",
                    "text": f"*Status:*\n{ticket['Status']}"
                }
            ]
        })
        
        # Description
        if ticket.get('Description'):
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Description:*\n{ticket['Description']}"
                }
            })
        
        return blocks 