import os
from config.slack import connect_slack
from config.slack import connect_slack
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = connect_slack()

if __name__ == "__main__":
    SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    print("Beamy the BME Bot is running!")
    handler.start()

