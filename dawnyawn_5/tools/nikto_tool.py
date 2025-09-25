# dawnyawn/tools/nikto_tool.py
from tools.base_tool import BaseTool

class NiktoTool(BaseTool):
    @property
    def name(self) -> str:
        return "nikto_web_vuln_scan"

    @property
    def description(self) -> str:
        return (
            "Scans a web server for over 6700 potentially dangerous files/CGIs, checks for "
            "outdated server versions, and other common web vulnerabilities. Can be 'noisy'. "
            "The input must be the full base URL."
        )

    def _construct_command(self, tool_input: str) -> str:
        # return f"nikto -host '{tool_input}' -maxtime 60"
        return f"nikto -Display 1234EP -o report.html -Format htm -Tuning 123bde -host '{tool_input}'"
