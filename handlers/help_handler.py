from .base_handler import BaseHandler

class HelpHandler(BaseHandler):
    def register_handlers(self, app):
        app.command("/bme-help")(self.handle_help)
    
    async def handle_help(self, ack, say):
        await ack()
        help_text = """
*BME IT Support Bot Help*

*Ticket Commands:*
• `/ticket-create` - Create a new support ticket
• `/ticket-status <id>` - Check ticket status
• `/my-tickets` - View your active tickets
• `/ticket-assign <id> <email>` - Assign ticket to someone
• `/ticket-close <id> <resolution>` - Close a ticket

*Priority Levels:*
• Low 🟢 - Regular requests
• Medium 🟠 - Time-sensitive issues
• High 🔴 - Critical issues
• SOS 🆘 - Can be added to any priority for emergencies (server down, security threats)

*Direct Messages:*
You can also DM me for:
• Quick IT questions
• Guidance on common issues
• Status updates on your tickets

*Need more help?*
Contact BME IT Support at `it-support@umich.edu`
"""
        await say(help_text) 