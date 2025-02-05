from .base_handler import BaseHandler
from services.teamdynamix.tickets import TeamDynamixTickets
from utils.formatters import format_ticket_message
from utils.validators import validate_email
from handlers.feedback_handler import FeedbackHandler

class TicketHandler(BaseHandler):
    def __init__(self, app):
        self.tdx_tickets = TeamDynamixTickets()
        self.feedback_handler = FeedbackHandler(app)
        super().__init__(app)
    
    def register_handlers(self, app):
        app.command("/ticket-create")(self.handle_create_ticket)
        app.command("/ticket-status")(self.handle_ticket_status)
        app.command("/my-tickets")(self.handle_my_tickets)
        app.command("/ticket-assign")(self.handle_assign_ticket)
        app.command("/ticket-close")(self.handle_close_ticket)
        
        # Modal handlers
        app.view("ticket_create_modal")(self.handle_ticket_create_modal_submit)
    
    async def handle_create_ticket(self, body, say):
        """Handle ticket creation from Slack"""
        try:
            user_email = body['user']['email']
            title = body['text']
            description = body.get('description', '')

            # Get AI solution with solution ID
            solution, solution_id = await self.openai_service.get_completion(
                description, 
                ticket_id=None  # We'll update this after ticket creation
            )

            # Create ticket in TeamDynamix with the solution
            ticket = await self.tdx_tickets.create_ticket(
                email_address=user_email,
                description=f"{description}\n\nProposed Solution:\n{solution}",
                priority=body.get('priority'),
                is_emergency=body.get('is_emergency', False)
            )

            # Now update the solution with the actual ticket ID
            if solution_id:
                await self.db_service.update_solution_ticket_id(
                    solution_id=solution_id,
                    ticket_id=ticket['ID']
                )

            await say(f"✅ Ticket created successfully! Ticket ID: {ticket['ID']}")

        except Exception as e:
            await say(f"❌ Error creating ticket: {str(e)}")

    async def handle_ticket_status(self, body, say):
        """Handle ticket status check from Slack"""
        try:
            ticket_id = body['ticket_id']  # Extract ticket ID from command
            ticket = await self.tdx_tickets.get_ticket(ticket_id)
            
            # Format ticket information for Slack
            status_message = (
                f"🎫 *Ticket {ticket['ID']}*\n"
                f"Title: {ticket['Title']}\n"
                f"Status: {ticket['Status']}\n"
                f"Priority: {ticket['Priority']}\n"
                f"Created: {ticket['CreatedDate']}"
            )
            
            await say(status_message)

        except Exception as e:
            await say(f"❌ Error retrieving ticket: {str(e)}")

    async def handle_my_tickets(self, body, say):
        """Handle request to view user's tickets"""
        try:
            user_email = body['user']['email']
            tickets = await self.tdx_tickets.get_tickets_by_assignee(user_email)
            
            if not tickets:
                await say("You don't have any active tickets.")
                return

            # Group tickets by status
            tickets_by_status = {}
            for ticket in tickets:
                status = ticket['Status']
                if status not in tickets_by_status:
                    tickets_by_status[status] = []
                tickets_by_status[status].append(ticket)

            # Format message with sections
            message = "*Your Assigned Tickets:*\n"
            for status, status_tickets in tickets_by_status.items():
                message += f"\n*{status}*\n"
                for ticket in status_tickets:
                    priority_indicator = self.tdx_tickets._get_priority_indicator(ticket['Priority'])
                    message += (
                        f"{priority_indicator} *{ticket['ID']}* - {ticket['Title']}\n"
                        f">Status: {ticket['Status']} | Priority: {ticket['Priority']}\n\n"
                    )
            
            await say(message)

        except Exception as e:
            await say(f"❌ Error retrieving your tickets: {str(e)}")

    async def handle_assign_ticket(self, body, say):
        """Handle ticket assignment"""
        try:
            args = body['text'].split()
            if len(args) < 2:
                await say("Usage: /ticket-assign <ticket_id> <email>")
                return

            ticket_id = args[0]
            assignee_email = args[1]

            ticket = await self.tdx_tickets.assign_ticket(ticket_id, assignee_email)
            await say(f"✅ Ticket {ticket_id} assigned to {assignee_email}")

        except Exception as e:
            await say(f"❌ Error assigning ticket: {str(e)}")

    async def handle_close_ticket(self, body, say):
        """Handle ticket closure"""
        try:
            args = body['text'].split(maxsplit=1)
            if len(args) < 2:
                await say("Usage: /ticket-close <ticket_id> <resolution>")
                return

            ticket_id = args[0]
            resolution = args[1]

            # Get the solution ID from the ticket (you'll need to store this when creating the ticket)
            ticket = await self.tdx_tickets.get_ticket(ticket_id)
            solution_id = ticket.get('solution_id')  # You'll need to add this to your ticket data

            # Close the ticket
            closed_ticket = await self.tdx_tickets.close_ticket(ticket_id, resolution)
            await say(f"✅ Ticket {ticket_id} has been closed\nResolution: {resolution}")

            # Request feedback if we have a solution ID
            if solution_id:
                await self.feedback_handler.request_feedback(
                    ticket_id=ticket_id,
                    solution_id=solution_id,
                    channel=body['channel_id']
                )

        except Exception as e:
            await say(f"❌ Error closing ticket: {str(e)}")

    async def handle_ticket_create_modal(self, ack, body, client):
        """Handle the ticket creation modal"""
        await ack()
        
        try:
            await client.views_open(
                trigger_id=body["trigger_id"],
                view={
                    "type": "modal",
                    "callback_id": "ticket_create_modal",
                    "title": {"type": "plain_text", "text": "Create IT Support Ticket"},
                    "submit": {"type": "plain_text", "text": "Submit"},
                    "blocks": [
                        {
                            "type": "input",
                            "block_id": "email_block",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "email",
                                "placeholder": {"type": "plain_text", "text": "Enter requester's email or full name with email"}
                            },
                            "label": {"type": "plain_text", "text": "From"},
                            "hint": {"type": "plain_text", "text": "Format: email@umich.edu or First Last <email@umich.edu>"}
                        },
                        {
                            "type": "input",
                            "block_id": "description_block",
                            "element": {
                                "type": "plain_text_input",
                                "action_id": "description",
                                "multiline": True,
                                "placeholder": {"type": "plain_text", "text": "Describe the issue..."}
                            },
                            "label": {"type": "plain_text", "text": "Description"}
                        },
                        {
                            "type": "input",
                            "block_id": "priority_block",
                            "element": {
                                "type": "static_select",
                                "action_id": "priority",
                                "options": [
                                    {"text": {"type": "plain_text", "text": "Low ��"}, "value": "1"},
                                    {"text": {"type": "plain_text", "text": "Medium ��"}, "value": "2"},
                                    {"text": {"type": "plain_text", "text": "High 🔴"}, "value": "3"}
                                ]
                            },
                            "label": {"type": "plain_text", "text": "Priority"}
                        },
                        {
                            "type": "input",
                            "block_id": "emergency_block",
                            "element": {
                                "type": "checkboxes",
                                "action_id": "is_emergency",
                                "options": [
                                    {
                                        "text": {
                                            "type": "plain_text",
                                            "text": "Mark as SOS/Emergency 🆘 (Server down, security threat, etc.)"
                                        },
                                        "value": "emergency"
                                    }
                                ]
                            },
                            "label": {"type": "plain_text", "text": "Emergency Status"}
                        }
                    ]
                }
            )
        except Exception as e:
            await say(f"❌ Error opening ticket creation form: {str(e)}") 