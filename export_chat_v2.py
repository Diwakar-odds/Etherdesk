import json
import os

transcript_path = r"C:\Users\hp\.gemini\antigravity-ide\brain\352e7cc7-5ee9-47f4-b7f0-6eb9275177c5\.system_generated\logs\transcript.jsonl"
plan_path = r"C:\Users\hp\.gemini\antigravity-ide\brain\352e7cc7-5ee9-47f4-b7f0-6eb9275177c5\implementation_plan.md"
output_path = r"f:\bn\antimatter\antigravity_conversation_context.md"

def export():
    output_lines = ["# Antigravity to VS Code - Project Context & Conversation\n\n"]
    
    # Status Summary
    output_lines.append("## Project Status Summary\n\n")
    output_lines.append("### What is DONE ✅\n")
    output_lines.append("- Built a standalone FastAPI backend (`server.py`) to run on the laptop.\n")
    output_lines.append("- Built a responsive mobile-friendly frontend (`index.html`, `style.css`, `app.js`).\n")
    output_lines.append("- Implemented API endpoints for reading directories (`/api/files`), reading file contents (`/api/file`), running terminal commands (`/api/terminal`), and interacting via chat (`/api/chat`).\n")
    output_lines.append("- Implemented a bridge mechanism using `prompt.txt` and `response.txt` to let the mobile web app communicate directly with the Antigravity agent.\n")
    output_lines.append("- Configured a scheduled cron job inside Antigravity to read `prompt.txt` every minute, execute it, and write the result to `response.txt`.\n")
    output_lines.append("- Handled IP resolution (`get_local_ip()`) to easily connect from a mobile device on the same network.\n\n")

    output_lines.append("### What is LEFT ❌\n")
    output_lines.append("- Setting up the project in VS Code and replacing the Antigravity cron job with a custom VS Code agent/extension script if necessary.\n")
    output_lines.append("- Testing the end-to-end flow on VS Code.\n")
    output_lines.append("- Adding any desired authentication or security (e.g., password protection) to the web app.\n\n")
    
    # Implementation Plan
    output_lines.append("## Original Implementation Plan\n\n")
    if os.path.exists(plan_path):
        with open(plan_path, 'r', encoding='utf-8') as f:
            output_lines.extend(f.readlines())
            output_lines.append("\n\n")
    else:
        output_lines.append("*Implementation plan file not found.* \n\n")

    # Conversation History
    output_lines.append("## Full Conversation History\n\n")
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    step = json.loads(line)
                    source = step.get("source", "UNKNOWN")
                    step_type = step.get("type", "UNKNOWN")
                    content = step.get("content", "")

                    if source == "USER_EXPLICIT" and step_type == "USER_INPUT":
                        output_lines.append(f"### USER:\n{content}\n\n")
                    elif source == "MODEL" and step_type == "PLANNER_RESPONSE":
                        output_lines.append(f"### AI (Antigravity):\n{content}\n\n")
                except Exception as e:
                    pass

        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(output_lines)
        print(f"Successfully exported comprehensive context to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    export()
