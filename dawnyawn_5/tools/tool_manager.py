# dawnyawn/tools/tool_manager.py
import logging
from typing import Dict, Optional

# --- Import all your tool classes ---
from tools.base_tool import BaseTool
from tools.nmap_tool import NmapTool
from tools.gobuster_tool import GobusterTool
from tools.dns_tool import DnsTool
from tools.ping_tool import PingTool
from tools.curl_tool import CurlTool
from tools.whois_tool import WhoisTool
from tools.whatweb_tool import WhatWebTool
from tools.nikto_tool import NiktoTool
from tools.sqlmap_tool import SqlmapTool
from tools.hydra_tool import HydraTool
from tools.subdomain_tool import SubdomainTool


class ToolManager:
    """Manages the registration and execution of all available tools."""

    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        # --- Register all your tools here ---
        self._register_tool(NmapTool())
        self._register_tool(GobusterTool())
        self._register_tool(DnsTool())
        self._register_tool(PingTool())
        self._register_tool(CurlTool())
        self._register_tool(WhoisTool())
        self._register_tool(WhatWebTool())
        self._register_tool(NiktoTool())
        self._register_tool(SqlmapTool())
        self._register_tool(HydraTool())
        self._register_tool(SubdomainTool())

        self.finish_mission_tool_name = "finish_mission"
        logging.info("ToolManager initialized with %d tools.", len(self.tools))

    # ... (the rest of the file remains the same) ...
    def _register_tool(self, tool_instance: BaseTool):
        """Registers a single tool instance."""
        if tool_instance.name in self.tools:
            raise ValueError(f"Tool with name '{tool_instance.name}' is already registered.")
        self.tools[tool_instance.name] = tool_instance
        logging.info("  - Registered tool: '%s'", tool_instance.name)

    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """Retrieves a tool instance by its name."""
        return self.tools.get(tool_name)

    def get_tool_manifest(self) -> str:
        """
        Generates a formatted string of all available tools and their
        descriptions for the AI's system prompt.
        """
        manifest = []
        # Sort tools by name for a consistent prompt
        for tool_name in sorted(self.tools.keys()):
            tool = self.tools[tool_name]
            manifest.append(f'- `{tool.name}`: {tool.description}')

        manifest.append(
            '- `finish_mission`: Use this tool when all tasks are complete. The '
            'tool_input should be a final, detailed summary of all findings.'
        )
        return "\n".join(manifest)