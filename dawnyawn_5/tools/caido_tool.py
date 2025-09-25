# dawnyawn/tools/caido_tool.py
from tools.base_tool import BaseTool

class CaidoTool(BaseTool):
    @property
    def name(self) -> str:
        return "caido_passive_scan"

    @property
    def description(self) -> str:
        return (
            "A modern, passive web application security scanner. It analyzes a target "
            "to find low-hanging fruit and informational vulnerabilities without sending "
            "aggressive traffic. The input must be the full base URL."
        )

    def _construct_command(self, tool_input: str) -> str:
        # Runs a headless, non-interactive scan. The exact flags might vary,
        # but this represents a common pattern for CLI tools.
        return f"caido-cli scan start --headless --no-interaction '{tool_input}'"