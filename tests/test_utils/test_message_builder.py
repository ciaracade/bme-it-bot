from utils.message_builder import SlackMessageBuilder

def test_create_section():
    section = SlackMessageBuilder.create_section("Test message")
    assert section["type"] == "section"
    assert section["text"]["type"] == "mrkdwn"
    assert section["text"]["text"] == "Test message"

def test_create_ticket_view():
    ticket = {
        "ID": "12345",
        "Title": "Test Ticket",
        "Status": "Open",
        "Description": "Test description"
    }
    
    blocks = SlackMessageBuilder.create_ticket_view(ticket)
    
    assert len(blocks) == 3  # Header, Title/Status, Description
    assert blocks[0]["type"] == "header"
    assert "12345" in blocks[0]["text"]["text"] 