import pytest
from slack_bolt.async_app import AsyncApp
from config.settings import Settings
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_settings():
    return Settings(
        SLACK_BOT_TOKEN="xoxb-test-token",
        SLACK_APP_TOKEN="xapp-test-token",
        SLACK_SIGNING_SECRET="test-secret",
        TEAMDYNAMIX_BASE_URL="https://test.teamdynamix.umich.edu",
        TEAMDYNAMIX_USERNAME="test_user",
        TEAMDYNAMIX_PASSWORD="test_pass",
        OPENAI_API_KEY="test-openai-key"
    )

@pytest.fixture
async def mock_app():
    app = AsyncApp(token="xoxb-test-token")
    app.client = AsyncMock()
    return app

@pytest.fixture
def mock_say():
    return AsyncMock()

@pytest.fixture
def mock_ack():
    return AsyncMock() 