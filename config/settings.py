from pydantic import BaseSettings

class Settings(BaseSettings):
    # Slack settings
    SLACK_BOT_TOKEN: str
    SLACK_APP_TOKEN: str
    SLACK_SIGNING_SECRET: str
    
    # TeamDynamix settings
    TEAMDYNAMIX_BASE_URL: str
    TEAMDYNAMIX_USERNAME: str
    TEAMDYNAMIX_PASSWORD: str
    
    # OpenAI settings
    OPENAI_API_KEY: str
    
    # Google Drive settings
    GOOGLE_DRIVE_FOLDER_ID: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    
    class Config:
        env_file = ".env"

def get_settings():
    return Settings() 