# dawnyawn/tools/hydra_tool.py
from tools.base_tool import BaseTool

class HydraTool(BaseTool):
    @property
    def name(self) -> str:
        return "hydra_bruteforce"

    @property
    def description(self) -> str:
        return (
            "Performs a brute-force attack to find a valid password for a given user and service. "
            "The input MUST be a comma-separated string in the format: service,hostname,username. "
            "The tool will automatically use the standard password list. "
            "Supported services: ftp, ssh, http-post-form. "
            "Example: 'ftp,192.168.1.1,admin' or 'ssh,target.com,root'"
        )

    def _construct_command(self, tool_input: str) -> str:
        try:
            service, hostname, username = tool_input.strip().split(',')
            password_list = "/app/wordlists/common.txt" # Using our self-contained wordlist

            if service.strip() not in ['ftp', 'ssh', 'http-post-form']:
                return f"echo 'Error: Unsupported service \"{service}\". Use ftp, ssh, or http-post-form.'"

            # The '-t 4' task flag is a good default for performance.
            return f"hydra -t 4 -l {username.strip()} -P {password_list} {service.strip()}://{hostname.strip()}"

        except ValueError:
            return "echo 'Error: Invalid input format. Expected: service,hostname,username'"