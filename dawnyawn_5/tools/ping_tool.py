# dawnyawn/tools/ping_tool.py
from tools.base_tool import BaseTool

class PingTool(BaseTool):
    @property
    def name(self) -> str:
        return "ping_check"

    @property
    def description(self) -> str:
        return (
            "Checks if a target host is online by sending ICMP packets. This is useful for "
            "verifying connectivity. The input must be a single IP address or hostname."
        )

    def _construct_command(self, tool_input: str) -> str:
        # '-c 4' is critical to ensure the command is self-terminating and doesn't run forever.
        return f"ping -c 4 {tool_input}"