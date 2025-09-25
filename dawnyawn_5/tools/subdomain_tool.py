# dawnyawn/tools/subdomain_tool.py
from tools.base_tool import BaseTool

class SubdomainTool(BaseTool):
    @property
    def name(self) -> str:
        return "subdomain_scan"

    @property
    def description(self) -> str:
        return (
            "Performs a DNS-based subdomain enumeration using a wordlist to discover hidden "
            "subdomains for a target. The input must be the root domain name, NOT a URL. "
            "Example: 'pentest-ground.com'"
        )

    def _construct_command(self, tool_input: str) -> str:
        # Use the same wordlist we use for directory scanning for this example.
        wordlist = "/app/wordlists/common.txt"
        return f"gobuster dns -d {tool_input} -w {wordlist} -t 50"