# dawnyawn/agent/thought_engine.py (Final Version with Enhanced Logging and Smart Task Completion)
import re
import json
import logging
from pydantic import BaseModel
from pydantic_core import ValidationError
from config import get_llm_client, LLM_MODEL_NAME, LLM_REQUEST_TIMEOUT
from tools.tool_manager import ToolManager
from models.task_node import TaskNode, TaskStatus
from typing import List, Dict


class ToolSelection(BaseModel):
    tool_name: str
    tool_input: str


class PlanUpdate(BaseModel):
    completed_task_ids: List[int]


def _clean_json_response(response_str: str) -> str:
    """Finds and extracts a JSON object from a string that might be wrapped in Markdown."""
    match = re.search(r'\{.*\}', response_str, re.DOTALL)
    if match:
        return match.group(0)
    return response_str


class ThoughtEngine:
    """AI Reasoning component. Decides the next action and assesses plan status."""

    def __init__(self, tool_manager: ToolManager):
        self.client = get_llm_client()
        self.tool_manager = tool_manager
        self.system_prompt_template = f"""
You are an expert penetration tester and command-line AI. Your SOLE function is to output a single, valid JSON object that represents the next best command to execute.

I. RESPONSE FORMATTING RULES (MANDATORY)
1.  **JSON ONLY:** Your entire response MUST be a single JSON object. Do not add explanations or any other text.
2.  **CORRECT SCHEMA:** The JSON object MUST have exactly two keys: `"tool_name"` and `"tool_input"`.
3.  **STRING INPUT:** The value for `"tool_input"` MUST be a single string.

II. STRATEGIC ANALYSIS & COMMAND RULES (HOW TO THINK)
1.  **FOCUS ON PENDING TASKS:** Look at the strategic plan and focus only on tasks with a 'PENDING' status.
2.  **DO NOT REPEAT YOURSELF:** If you have already used a tool and it did not complete the task, DO NOT use that same tool with the same input again. Choose a different tool to make progress.
3.  **Learn from Failures:** If a tool fails or provides no useful information for the current task, choose a different tool.
4.  **Goal Completion:** Once all tasks in the plan are 'COMPLETED', you MUST use the `finish_mission` tool.

III. AVAILABLE TOOLS:
{self.tool_manager.get_tool_manifest()}
"""

    def _format_plan(self, plan: List[TaskNode]) -> str:
        if not plan: return "No plan provided."
        return "\n".join([f"  - Task {task.task_id} [{task.status}]: {task.description}" for task in plan])

    def _log_plan_status(self, plan: List[TaskNode]):
        """Logs the current status of all tasks for user visibility."""
        logging.info("--- Current Mission Status ---")
        if not plan:
            logging.info("  No plan has been generated yet.")
        else:
            for task in plan:
                if task.status == TaskStatus.COMPLETED:
                    icon = "✅"
                elif task.status == TaskStatus.FAILED:
                    icon = "❌"
                else: # PENDING or RUNNING
                    icon = "📝"
                logging.info(f"  {icon} Task {task.task_id} [{task.status.value}]: {task.description}")
        logging.info("------------------------------")


    def choose_next_action(self, goal: str, plan: List[TaskNode], history: List[Dict]) -> ToolSelection:
        logging.info("🤔 Thinking about the next step...")
        self._log_plan_status(plan)

        all_tasks_completed = all(task.status == TaskStatus.COMPLETED for task in plan)

        if all_tasks_completed and plan:
            logging.info("✅ All plan tasks are complete. Forcing finish_mission.")
            user_prompt = (
                "CRITICAL: All tasks in the strategic plan are now marked as 'COMPLETED'.\n"
                "You MUST now use the `finish_mission` tool.\n"
                "Review the full execution history and provide a detailed, final summary of your findings as the `tool_input`.\n"
                "Your response MUST be the required JSON object.\n\n"
                f"**Main Goal:** {goal}\n\n"
                f"**Execution History:**\n{json.dumps(history, indent=2)}"
            )
        else:
            user_prompt = (
                f"Based on the goal, plan, and history below, decide the single best tool to use next to progress on a PENDING task. Respond with a single, valid JSON object.\n\n"
                f"**Main Goal:** {goal}\n\n"
                f"**Strategic Plan:**\n{self._format_plan(plan)}\n\n"
                f"**Execution History (most recent last):\n{json.dumps(history, indent=2)}"
            )
        try:
            response = self.client.chat.completions.create(
                model=LLM_MODEL_NAME,
                messages=[{"role": "system", "content": self.system_prompt_template},
                          {"role": "user", "content": user_prompt}],
                timeout=LLM_REQUEST_TIMEOUT,
                response_format={"type": "json_object"},
                temperature=0.2
            )
            raw_response = response.choices[0].message.content
            selection = ToolSelection.model_validate_json(_clean_json_response(raw_response))

            if all_tasks_completed and plan:
                logging.info("AI is summarizing the mission to finish.")
            else:
                logging.info(f"AI's Next Action: Using tool '{selection.tool_name}' with input '{selection.tool_input}'")


            return selection
        except (ValidationError, json.JSONDecodeError) as e:
            logging.error("Critical Error during thought process: %s", type(e).__name__)
            return ToolSelection(tool_name="finish_mission",
                                 tool_input="Mission failed: The AI produced an invalid JSON response.")

    def get_completed_task_ids(self, goal: str, plan: List[TaskNode], history: List[Dict]) -> List[int]:
        """Asks the AI to identify which tasks are complete based on the latest action."""
        # --- THE FIX: This prompt is now much stricter about analysis tasks ---
        plan_update_prompt = (
            "You are an expert project manager AI. Your job is to determine which tasks are now complete. "
            "Review the strategic plan and the observation from the MOST RECENT command.\n\n"
            "**CRITICAL INSTRUCTION:** The output from one command (like a port scan) might contain all the information needed to complete subsequent 'analysis' tasks. "
            "For example, if Task 1 is 'Scan the target' and Task 2 is 'Identify the web server', the output of the `nmap` scan for Task 1 likely contains the web server name, completing Task 2 at the same time.\n\n"
            "**BE STRICT:** Only mark a task as complete if the observation explicitly and fully provides the information required by the task description. If a task requires an Nmap scan, the observation MUST contain Nmap results.\n\n"
            "Identify ALL task IDs that are now fully completed by the last action's observation. "
            "Your response MUST be a single JSON object with one key: `\"completed_task_ids\"`, which is a list of integers. "
            "Example: `{\"completed_task_ids\": [1, 2]}`. If no tasks were completed, return an empty list.\n\n"
            f"**Strategic Plan:**\n{self._format_plan(plan)}\n\n"
            f"**Most Recent Action & Observation:**\n{json.dumps(history[-1], indent=2) if history else 'No actions yet.'}"
        )
        try:
            response = self.client.chat.completions.create(
                model=LLM_MODEL_NAME,
                messages=[{"role": "system", "content": "You are a JSON-only plan updating assistant."},
                          {"role": "user", "content": plan_update_prompt}],
                timeout=LLM_REQUEST_TIMEOUT,
                response_format={"type": "json_object"},
                temperature=0.0
            )
            raw_response = response.choices[0].message.content
            update = PlanUpdate.model_validate_json(_clean_json_response(raw_response))
            # Log which tasks the AI has marked as complete
            if update.completed_task_ids:
                logging.info("AI assessment: The last action completed Task IDs: %s", update.completed_task_ids)
            else:
                logging.info("AI assessment: The last action did not complete any new tasks.")
            return update.completed_task_ids
        except (ValidationError, json.JSONDecodeError) as e:
            logging.error("AI failed to identify completed tasks with valid JSON: %s", e)
            return []  # Return an empty list on failure