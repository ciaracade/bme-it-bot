from slack_bolt.async_app import AsyncApp
from services.database_service import DatabaseService
from utils.message_builder import SlackMessageBuilder
import logging

class FeedbackHandler:
    def __init__(self, app: AsyncApp):
        self.app = app
        self.db_service = DatabaseService()
        self.register_handlers(app)

    def register_handlers(self, app: AsyncApp):
        app.action("solution_helpful")(self.handle_solution_helpful)
        app.action("solution_not_helpful")(self.handle_solution_not_helpful)

    async def request_feedback(self, ticket_id: str, solution_id: int, channel: str):
        """Send feedback request message to Slack"""
        try:
            blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Was the solution for ticket #{ticket_id} helpful?*"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "👍 Yes, it helped"
                            },
                            "style": "primary",
                            "action_id": "solution_helpful",
                            "value": f"{ticket_id}:{solution_id}"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "👎 No, didn't help"
                            },
                            "style": "danger",
                            "action_id": "solution_not_helpful",
                            "value": f"{ticket_id}:{solution_id}"
                        }
                    ]
                }
            ]

            await self.app.client.chat_postMessage(
                channel=channel,
                blocks=blocks,
                text="Was the solution helpful?"
            )

        except Exception as e:
            logging.error(f"Error requesting feedback: {e}")

    async def handle_solution_helpful(self, ack, body, say):
        """Handle when user marks solution as helpful"""
        await ack()
        try:
            ticket_id, solution_id = body["actions"][0]["value"].split(":")
            await self.db_service.update_solution_success(int(solution_id), True)
            
            await say("Thanks for your feedback! I'll remember this solution for similar issues. 📝")
            
            # Update the original message to remove buttons
            if "message_ts" in body:
                blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"✅ Solution for ticket #{ticket_id} was marked as helpful"
                        }
                    }
                ]
                
                await self.app.client.chat_update(
                    channel=body["channel"]["id"],
                    ts=body["message_ts"],
                    blocks=blocks,
                    text="Solution was helpful"
                )

        except Exception as e:
            logging.error(f"Error handling helpful feedback: {e}")
            await say("Sorry, there was an error processing your feedback.")

    async def handle_solution_not_helpful(self, ack, body, say):
        """Handle when user marks solution as not helpful"""
        await ack()
        try:
            ticket_id, solution_id = body["actions"][0]["value"].split(":")
            await self.db_service.update_solution_success(int(solution_id), False)
            
            # Update the original message
            if "message_ts" in body:
                blocks = [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"❌ Solution for ticket #{ticket_id} was marked as not helpful"
                        }
                    }
                ]
                
                await self.app.client.chat_update(
                    channel=body["channel"]["id"],
                    ts=body["message_ts"],
                    blocks=blocks,
                    text="Solution was not helpful"
                )

            # Ask for additional feedback
            await say({
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "I'm sorry the solution wasn't helpful. Would you mind sharing what didn't work? This will help improve future solutions."
                        }
                    },
                    {
                        "type": "input",
                        "block_id": "feedback_input",
                        "element": {
                            "type": "plain_text_input",
                            "action_id": "feedback_text",
                            "multiline": True,
                            "placeholder": {
                                "type": "plain_text",
                                "text": "What could have been better?"
                            }
                        },
                        "label": {
                            "type": "plain_text",
                            "text": "Feedback"
                        }
                    }
                ]
            })

        except Exception as e:
            logging.error(f"Error handling not helpful feedback: {e}")
            await say("Sorry, there was an error processing your feedback.") 