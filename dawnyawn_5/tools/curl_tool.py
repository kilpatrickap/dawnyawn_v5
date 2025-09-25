# dawnyawn/tools/curl_tool.py
from tools.base_tool import BaseTool

class CurlTool(BaseTool):
    @property
    def name(self) -> str:
        return "fetch_web_content"

    @property
    def description(self) -> str:
        return (
            "Retrieves the full HTML content or data from a given URL. Excellent for "
            "grabbing homepages, API responses, or specific files. The input must be "
            "a full URL, including 'http://' or 'https://'."
        )

    def _construct_command(self, tool_input: str) -> str:
        # -sSL: Silent mode, show errors, and follow redirects. A robust combination for scripting.
        return f"curl -sSL '{tool_input}'"