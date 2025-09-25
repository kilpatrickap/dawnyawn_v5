# dawnyawn/tools/whatweb_tool.py
from tools.base_tool import BaseTool

class WhatWebTool(BaseTool):
    @property
    def name(self) -> str:
        return "whatweb_scan"

    @property
    def description(self) -> str:
        return (
            "Identifies technologies used on a website, including CMS, web server, "
            "JavaScript libraries, and more. The input must be a full URL."
        )

    def _construct_command(self, tool_input: str) -> str:
        return f"whatweb '{tool_input}'"