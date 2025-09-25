# dawnyawn/tools/base_tool.py
from abc import ABC, abstractmethod
from services.mcp_client import McpClient
from typing import Tuple


class BaseTool(ABC):
    """Abstract base class for all agent tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """The unique name of the tool (e.g., 'nmap_scan')."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """
        A detailed description for the AI to understand what the tool does
        and what input it expects. This is CRITICAL for the AI's reasoning.
        """
        pass

    def __init__(self):
        self.mcp_client = McpClient()

    @abstractmethod
    def _construct_command(self, tool_input: str) -> str:
        """
        Takes the simple input from the AI and constructs the full,
        executable shell command.
        """
        pass

    def execute(self, tool_input: str) -> Tuple[str, str]:
        """
        Executes the command on the remote Kali server via the McpClient.
        This method is shared by all tools.
        """
        full_command = self._construct_command(tool_input)
        print(f"  > Executing constructed command: `{full_command}`")
        return self.mcp_client.execute_command(full_command)