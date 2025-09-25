# dawnyawn/tools/john_tool.py
from tools.base_tool import BaseTool

class JohnTheRipperTool(BaseTool):
    @property
    def name(self) -> str:
        return "john_crack_hash"

    @property
    def description(self) -> str:
        return (
            "An offline password cracker for cracking password hashes. The input must be the "
            "full path to a file inside the container that contains the password hashes to crack. "
            "It will use the default wordlist to attempt to crack them."
        )

    def _construct_command(self, tool_input: str) -> str:
        # This two-part command first runs the cracking session, and then the '--show'
        # command prints any cracked passwords it found to stdout, ensuring we get the result.
        wordlist = "/app/wordlists/xato-net-10-million-passwords-1000000.txt"
        hash_file = tool_input.strip()
        return f"john --wordlist={wordlist} {hash_file} && john --show {hash_file}"