from typing import List, Dict
import re

class ConfigValidator:
    @staticmethod
    def validate_teamdynamix_config(config: Dict) -> List[str]:
        """Validate TeamDynamix configuration"""
        errors = []
        
        # Required fields
        required_fields = ['base_url', 'username', 'password']
        for field in required_fields:
            if not config.get(field):
                errors.append(f"Missing required field: {field}")
        
        # URL format
        if config.get('base_url'):
            if not re.match(r'https?://.*\.umich\.edu.*', config['base_url']):
                errors.append("base_url must be a valid umich.edu URL")
        
        # Status IDs
        status_ids = config.get('status_ids', {})
        if not all(isinstance(v, int) for v in status_ids.values()):
            errors.append("All status IDs must be integers")
        
        return errors

    @staticmethod
    def validate_slack_config(config: Dict) -> List[str]:
        """Validate Slack configuration"""
        errors = []
        
        # Token format
        if config.get('SLACK_BOT_TOKEN'):
            if not config['SLACK_BOT_TOKEN'].startswith('xoxb-'):
                errors.append("Invalid bot token format")
        
        if config.get('SLACK_APP_TOKEN'):
            if not config['SLACK_APP_TOKEN'].startswith('xapp-'):
                errors.append("Invalid app token format")
        
        return errors 