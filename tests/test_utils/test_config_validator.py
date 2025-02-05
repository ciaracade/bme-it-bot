from utils.config_validator import ConfigValidator

def test_validate_teamdynamix_config():
    config = {
        "base_url": "https://teamdynamix.umich.edu",
        "username": "test_user",
        "password": "test_pass",
        "status_ids": {"new": 1, "closed": 2}
    }
    
    errors = ConfigValidator.validate_teamdynamix_config(config)
    assert len(errors) == 0
    
    # Test invalid URL
    config["base_url"] = "https://invalid-domain.com"
    errors = ConfigValidator.validate_teamdynamix_config(config)
    assert len(errors) > 0
    assert any("umich.edu" in error for error in errors)

def test_validate_slack_config():
    config = {
        "SLACK_BOT_TOKEN": "xoxb-test-token",
        "SLACK_APP_TOKEN": "xapp-test-token"
    }
    
    errors = ConfigValidator.validate_slack_config(config)
    assert len(errors) == 0
    
    # Test invalid token format
    config["SLACK_BOT_TOKEN"] = "invalid-token"
    errors = ConfigValidator.validate_slack_config(config)
    assert len(errors) > 0 