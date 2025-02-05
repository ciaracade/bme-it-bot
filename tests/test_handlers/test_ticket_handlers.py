import pytest
from handlers.ticket_handlers import TicketHandler
from utils.exceptions import ValidationError

@pytest.mark.asyncio
async def test_handle_create_ticket_success(mock_app, mock_say):
    handler = TicketHandler(mock_app)
    handler.tdx_tickets.create_ticket = AsyncMock(return_value={"ID": "12345"})
    
    body = {
        "user": {"email": "test@umich.edu"},
        "text": "Test ticket",
        "description": "Test description"
    }
    
    await handler.handle_create_ticket(body, mock_say)
    
    mock_say.assert_called_once_with("✅ Ticket created successfully! Ticket ID: 12345")

@pytest.mark.asyncio
async def test_handle_ticket_status(mock_app, mock_say):
    handler = TicketHandler(mock_app)
    handler.tdx_tickets.get_ticket = AsyncMock(return_value={
        "ID": "12345",
        "Title": "Test Ticket",
        "Status": "Open",
        "Priority": "High",
        "CreatedDate": "2024-02-04T12:00:00"
    })
    
    body = {"ticket_id": "12345"}
    await handler.handle_ticket_status(body, mock_say)
    
    mock_say.assert_called_once()
    assert "Ticket 12345" in mock_say.call_args[0][0]

@pytest.mark.asyncio
async def test_handle_emergency_ticket(mock_app, mock_say):
    handler = TicketHandler(mock_app)
    handler.tdx_tickets.create_ticket = AsyncMock(return_value={"ID": "12345"})
    
    body = {
        "user": {"email": "test@umich.edu"},
        "text": "Server down",
        "description": "Critical server failure",
        "is_emergency": True
    }
    
    await handler.handle_create_ticket(body, mock_say)
    handler.tdx_tickets.create_ticket.assert_called_with(
        email_address="test@umich.edu",
        description="Critical server failure",
        is_emergency=True
    ) 