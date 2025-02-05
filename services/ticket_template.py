from typing import Dict

class TicketTemplate:
    TEMPLATES = {
        'hardware': {
            'title': "{name} / Hardware Issue - {device_type}",
            'description': """
Hardware Issue Report:
- Device Type: {device_type}
- Issue Description: {description}
- Location: {location}
- Urgency: {urgency}
            """.strip()
        },
        'software': {
            'title': "{name} / Software Issue - {software_name}",
            'description': """
Software Issue Report:
- Software: {software_name}
- Version: {version}
- Issue Description: {description}
- Steps to Reproduce: {steps}
            """.strip()
        },
        'access': {
            'title': "{name} / Access Request - {system_name}",
            'description': """
Access Request:
- System: {system_name}
- Access Type: {access_type}
- Justification: {justification}
- Duration: {duration}
            """.strip()
        },
        'lab_equipment': {
            'title': "{name} / Lab Equipment - {equipment_type}",
            'description': """
Lab Equipment Issue:
- Equipment: {equipment_type}
- Lab Location: {lab_location}
- Issue Description: {description}
- Impact: {impact}
- Grant/Fund Number (if applicable): {fund_number}
            """.strip()
        },
        'network': {
            'title': "{name} / Network Issue - {issue_type}",
            'description': """
Network Issue Report:
- Type: {issue_type}
- Location: {location}
- Device MAC Address: {mac_address}
- Connection Type: {connection_type}
- Issue Description: {description}
            """.strip()
        },
        'research_software': {
            'title': "{name} / Research Software - {software_name}",
            'description': """
Research Software Request/Issue:
- Software Name: {software_name}
- License Type Needed: {license_type}
- Research Project: {project_name}
- PI Name: {pi_name}
- Fund Number: {fund_number}
- Issue/Request Details: {description}
            """.strip()
        }
    }

    @classmethod
    def get_template(cls, template_type: str) -> Dict[str, str]:
        """Get a ticket template by type"""
        return cls.TEMPLATES.get(template_type, cls.TEMPLATES['general'])

    @classmethod
    def fill_template(cls, template_type: str, **kwargs) -> Dict[str, str]:
        """Fill a template with provided values"""
        template = cls.get_template(template_type)
        return {
            'title': template['title'].format(**kwargs),
            'description': template['description'].format(**kwargs)
        } 