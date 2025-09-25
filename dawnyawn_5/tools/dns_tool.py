# dawnyawn/tools/dns_tool.py
from tools.base_tool import BaseTool

class DnsTool(BaseTool):
    @property
    def name(self) -> str:
        return "dns_lookup"

    @property
    def description(self) -> str:
        return (
            "Performs a DNS lookup to find the IP address(es) for a given hostname. "
            "This is a fundamental first step in reconnaissance. The input must be a "
            "single hostname (e.g., 'www.pentest-ground.com')."
        )

    def _construct_command(self, tool_input: str) -> str:
        # 'dig +short' provides a clean, IP-only output that is easy for the agent to parse.
        return f"dig +short {tool_input}"