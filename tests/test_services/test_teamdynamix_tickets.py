import pytest
from services.teamdynamix.tickets import TeamDynamixTickets
from utils.exceptions import TeamDynamixError

@pytest.mark.asyncio
async def test_extract_first_name():
    tdx = TeamDynamixTickets()
    
    # Test email only
    assert tdx._extract_first_name("john@umich.edu") == "john"
    
    # Test full name with email
    assert tdx._extract_first_name("John Doe <john@umich.edu>") == "John"

@pytest.mark.asyncio
async def test_format_ticket_title():
    tdx = TeamDynamixTickets()
    title = tdx._format_ticket_title("John", "Printer not working")
    assert title == "John / Printer not working"

@pytest.mark.asyncio
async def test_get_priority_indicator():
    tdx = TeamDynamixTickets()
    
    # Test normal priorities
    assert tdx._get_priority_indicator("High") == "🔴"
    assert tdx._get_priority_indicator("Medium") == "🟠"
    assert tdx._get_priority_indicator("Low") == "🟢"
    
    # Test emergency
    assert "🆘" in tdx._get_priority_indicator("High", is_emergency=True) 