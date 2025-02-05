from slack_bolt.async_app import AsyncApp

class NotificationService:
    def __init__(self, app: AsyncApp, config: dict):
        self.app = app
        self.config = config
        self.notification_channel = config['notifications']['channel']

    async def notify_ticket_update(self, ticket_id, update_type, details):
        """Send notification to Slack channel about ticket updates"""
        if not self.config['notifications']['enabled']:
            return

        priority_indicator = self._get_priority_indicator(details.get('priority', 'Medium'))
        
        message_templates = {
            'created': f"{priority_indicator} New ticket created: #{ticket_id}\n*{{uniqname}} / {{title}}*\nPriority: {{priority}}",
            'updated': f"{priority_indicator} Ticket #{ticket_id} updated\n*{{uniqname}} / {{title}}*\n{{details}}",
            'closed': f"✅ Ticket #{ticket_id} closed\n*{{uniqname}} / {{title}}*\nResolution: {{details}}",
            'assigned': f"👤 Ticket #{ticket_id} assigned to {{assignee}}\n*{{uniqname}} / {{title}}*"
        }

        message = message_templates.get(update_type, f"🔔 Ticket #{ticket_id} {{update_type}}")
        formatted_message = message.format(**details)

        await self.app.client.chat_postMessage(
            channel=self.notification_channel,
            text=formatted_message
        )

    def _get_priority_indicator(self, priority):
        """Match TeamDynamix priority indicators"""
        return {
            'Emergency': '🔴',
            'High': '🟡',
            'Medium': '🟡',
            'Low': '🟢'
        }.get(priority, '⚪') 