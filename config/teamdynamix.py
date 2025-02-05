import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# TeamDynamix API Configuration
TEAMDYNAMIX_CONFIG = {
    'base_url': os.getenv('TEAMDYNAMIX_BASE_URL', 'https://demotemplate.teamdynamix.com/TDWebApi/'),
    'username': os.getenv('TEAMDYNAMIX_USERNAME'),
    'password': os.getenv('TEAMDYNAMIX_PASSWORD'),
    
    # Optional configurations
    'timeout': int(os.getenv('TEAMDYNAMIX_TIMEOUT', 30)),  # Request timeout in seconds
    'max_retries': int(os.getenv('TEAMDYNAMIX_MAX_RETRIES', 3)),
    
    # API endpoints
    'endpoints': {
        'auth': '/api/auth',
        'tickets': '/api/tickets',
        'assets': '/api/assets',
        'users': '/api/people',
        'groups': '/api/groups'
    },
    
    # Default ticket settings
    'default_status_id': int(os.getenv('TEAMDYNAMIX_DEFAULT_STATUS_ID', 1)),
    'default_priority_id': int(os.getenv('TEAMDYNAMIX_DEFAULT_PRIORITY_ID', 1)),
    
    # Ticket form IDs
    'ticket_form_id': int(os.getenv('TEAMDYNAMIX_TICKET_FORM_ID', 1)),
    
    # Ticket types
    'ticket_types': {
        'incident': int(os.getenv('TEAMDYNAMIX_INCIDENT_TYPE_ID', 1)),
        'service_request': int(os.getenv('TEAMDYNAMIX_SERVICE_REQUEST_TYPE_ID', 2))
    },
    
    # Status IDs for different ticket states
    'status_ids': {
        'new': int(os.getenv('TEAMDYNAMIX_STATUS_NEW', 1)),
        'assigned': int(os.getenv('TEAMDYNAMIX_STATUS_ASSIGNED', 2)),
        'in_progress': int(os.getenv('TEAMDYNAMIX_STATUS_IN_PROGRESS', 3)),
        'closed': int(os.getenv('TEAMDYNAMIX_STATUS_CLOSED', 4))
    },
    
    # Notification settings
    'notifications': {
        'enabled': os.getenv('TEAMDYNAMIX_NOTIFICATIONS_ENABLED', 'true').lower() == 'true',
        'channel': os.getenv('TEAMDYNAMIX_NOTIFICATIONS_CHANNEL', '#help-desk')
    },
    
    # U-M Authentication settings
    'auth': {
        'login_url': 'https://weblogin.umich.edu/',
        'duo_enabled': True,  # Set to True if Duo 2FA is required
        'duo_config': {
            'host': os.getenv('TEAMDYNAMIX_DUO_HOST'),
            'signature': os.getenv('TEAMDYNAMIX_DUO_SIGNATURE')
        }
    }
}

# Optional: Custom configurations for different environments
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

if ENVIRONMENT == 'development':
    # Development-specific settings
    TEAMDYNAMIX_CONFIG['verify_ssl'] = False  # Only for development
    TEAMDYNAMIX_CONFIG['debug'] = True
else:
    # Production settings
    TEAMDYNAMIX_CONFIG['verify_ssl'] = True
    TEAMDYNAMIX_CONFIG['debug'] = False

def get_config():
    """
    Returns the TeamDynamix configuration.
    Validates required settings are present.
    """
    required_settings = ['username', 'password', 'base_url']
    
    for setting in required_settings:
        if not TEAMDYNAMIX_CONFIG.get(setting):
            raise ValueError(f"Missing required TeamDynamix configuration: {setting}")
    
    return TEAMDYNAMIX_CONFIG



