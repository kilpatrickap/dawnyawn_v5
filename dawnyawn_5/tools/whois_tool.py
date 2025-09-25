# dawnyawn/tools/whois_tool.py
from tools.base_tool import BaseTool

class WhoisTool(BaseTool):
    @property
    def name(self) -> str:
        return "whois_lookup"

    @property
    def description(self) -> str:
        return (
            "Retrieves domain registration information (owner, contact info, name servers) "
            "for a given domain name. The input must be a domain name (e.g., 'pentest-ground.com')."
        )

    def _construct_command(self, tool_input: str) -> str:
        return f"whois {tool_input}"