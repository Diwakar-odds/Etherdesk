import json
import sys

transcript_path = r"C:\Users\hp\.gemini\antigravity-ide\brain\352e7cc7-5ee9-47f4-b7f0-6eb9275177c5\.system_generated\logs\transcript.jsonl"
output_path = r"f:\bn\antimatter\antigravity_conversation_context.md"

def export():
    print(f"Reading from {transcript_path}")
    output_lines = ["# Antigravity to VS Code - Conversation Context\n\n"]
    output_lines.append("## Project Context: Antimatter App\n")
    output_lines.append("The user and the agent built a custom remote control bridge named 'Antimatter'.\n")
    output_lines.append("The goal was to allow the user to send prompts from their phone and have the Antigravity IDE (on the laptop) execute them.\n")
    output_lines.append("Architecture: FastAPI backend, HTML/JS frontend, communicating with Antigravity via `prompt.txt` and `response.txt` read by a scheduled cron job.\n\n")
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
        print(f"Successfully exported conversation to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    export()
