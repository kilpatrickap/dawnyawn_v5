# dawnyawn/tools/gobuster_tool.py
from tools.base_tool import BaseTool

class GobusterTool(BaseTool):
    @property
    def name(self) -> str:
        return "gobuster_web_scan"

    @property
    def description(self) -> str:
        return (
            "Discovers hidden directories and files on a web server using Gobuster. "
            "The input must be the full base URL of the target, including http/https. "
            "Example: 'http://www.pentest-ground.com'"
        )

    def _construct_command(self, tool_input: str) -> str:
        # --- THE FIX: Reference the wordlist copied into our app directory ---
        # This path is now reliable and controlled by our project.
        wordlist = "/app/wordlists/common.txt"
        return f"gobuster dir -u {tool_input} -w {wordlist} -t 50 --no-error"