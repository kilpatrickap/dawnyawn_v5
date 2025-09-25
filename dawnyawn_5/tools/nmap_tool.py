# dawnyawn/tools/nmap_tool.py
from tools.base_tool import BaseTool

class NmapTool(BaseTool):
    @property
    def name(self) -> str:
        return "nmap_scan"

    @property
    def description(self) -> str:
        return (
            "Performs a comprehensive Nmap scan on a target to discover open ports, "
            "running services, and their versions. The input must be a single IP "
            "address or a hostname."
        )

    def _construct_command(self, tool_input: str) -> str:
        # Here we define the best-practice flags for a version scan.
        # The AI doesn't need to know this, only that it wants to find services.
        return f"nmap -sV -T4 --open {tool_input}"