# dawnyawn/tools/sqlmap_tool.py
from tools.base_tool import BaseTool

class SqlmapTool(BaseTool):
    @property
    def name(self) -> str:
        return "sqlmap_scan"

    @property
    def description(self) -> str:
        return (
            "Automates the process of detecting and exploiting SQL injection vulnerabilities. "
            "The input must be the FULL, specific URL that is suspected to be vulnerable, "
            "including all query parameters. Example: 'http://testphp.vulnweb.com/listproducts.php?cat=1'"
        )

    def _construct_command(self, tool_input: str) -> str:
        # '--batch' is absolutely critical for an autonomous agent. It prevents sqlmap
        # from asking interactive questions and makes it run with default answers.
        # --level=1 and --risk=1 are safe defaults for initial scans.
        return f"sqlmap -u '{tool_input}' --batch --level=1 --risk=1"