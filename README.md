# BME IT Support Slack Bot

A Slack bot for the University of Michigan Biomedical Engineering department that handles IT support tickets with AI assistance and learning capabilities.

## Features

### Core Functionality
- Create and manage IT support tickets through Slack
- AI-powered ticket categorization and solution suggestions
- Integration with TeamDynamix ticketing system
- Automated solution learning from past tickets
- Documentation search from internal Google Drive

### Smart Features
- Learns from successful solutions
- Provides relevant documentation from internal knowledge base
- Tracks solution effectiveness through feedback
- Analyzes patterns in successful solutions
- Maintains a database of proven solutions

### Commands
```
/ticket-create - Create a new support ticket
/ticket-status <ticket_id> - Check ticket status
/my-tickets - View your assigned tickets
/ticket-assign <ticket_id> <email> - Assign ticket to someone
/ticket-close <ticket_id> <resolution> - Close a ticket
```

## Setup

### Prerequisites
```bash
# Python 3.8+
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### Environment Configuration
Create a `.env` file:
```env
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token
SLACK_SIGNING_SECRET=your-secret

# TeamDynamix Configuration
TEAMDYNAMIX_BASE_URL=https://your-instance.teamdynamix.com/TDWebApi/
TEAMDYNAMIX_USERNAME=service_account_username
TEAMDYNAMIX_PASSWORD=service_account_password

# Google Drive Configuration
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
GOOGLE_APPLICATION_CREDENTIALS=config/google_credentials.json

# OpenAI Configuration
OPENAI_API_KEY=your-api-key
```

### Database Setup
The bot uses SQLite by default:
```bash
# Initialize database
python scripts/init_db.py
```

### Google Drive Setup
1. Create a Google Cloud project
2. Enable Drive API
3. Create service account credentials
4. Download credentials to `config/google_credentials.json`
5. Share documentation folder with service account email

## Architecture

### Components
- `handlers/` - Slack command and event handlers
- `services/` - Core business logic services
- `models/` - Database models
- `utils/` - Helper utilities
- `tests/` - Test suite

### Services
- `TeamDynamixTickets` - TeamDynamix integration
- `OpenAIService` - AI solution generation
- `GoogleDriveService` - Documentation search
- `DatabaseService` - Solution storage and retrieval
- `AnalysisService` - Solution pattern analysis

### Data Flow
1. User creates ticket in Slack
2. Bot searches documentation and past solutions
3. AI generates solution using available information
4. Solution stored in database
5. Ticket created in TeamDynamix
6. On closure, bot requests feedback
7. Feedback updates solution success rate

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_handlers/test_ticket_handlers.py
```

## Development

### Adding New Features
1. Create feature branch
2. Add tests
3. Implement feature
4. Update documentation
5. Submit PR

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions focused

## Monitoring

### Logs
- Application logs in `logs/app.log`
- Error logs in `logs/error.log`
- Solution analytics in `logs/analytics.log`

### Analytics
Access solution analytics:
```python
from services.analysis_service import SolutionAnalysisService
analytics = SolutionAnalysisService(db_service)
stats = await analytics.analyze_solutions()
```

## Contributing
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License
MIT License - See LICENSE file

## Support
Contact BME IT Support for assistance