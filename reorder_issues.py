
import re

input_file = "issue_report/priority_issues.md"
output_file = "issue_report/priority_issues.md"

def reorder_issues():
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by "## Issue #" to separate blocks
    # We need a regex that captures the issue header
    # But files might have other level 2 headers. 
    # Let's assume all issues start with "## Issue #X:"
    
    # Strategy:
    # 1. Split into chunks based on "## Issue #"
    # 2. Filter out the one we want to delete ("Notification System Error")
    # 3. Re-assemble with new numbers
    
    # We'll use a regex to find all issue headers and their content
    # Pattern: ^## Issue #\d+:(.*?)(?=^## Issue #|\Z)
    # matching multiline, dotall
    
    # Actually, simpler: Read line by line.
    
    lines = content.split('\n')
    new_lines = []
    
    issue_counter = 1
    inside_deleted_issue = False
    
    for line in lines:
        if line.strip().startswith("## Issue #"):
            # Check if this is the issue to delete
            if "Notification System Error" in line:
                inside_deleted_issue = True
                print(f"Removing: {line.strip()}")
                continue
            else:
                inside_deleted_issue = False
                # Renumber
                # Extract title part after the number
                # "## Issue #15: Something" -> "## Issue #1: Something"
                match = re.search(r"## Issue #\d+:(.*)", line)
                if match:
                    title = match.group(1)
                    new_line = f"## Issue #{issue_counter}:{title}"
                    new_lines.append(new_line)
                    print(f"Renumbered: {new_line}")
                    issue_counter += 1
                else:
                    # Fallback if format is weird
                    new_lines.append(line)
        else:
            if not inside_deleted_issue:
                new_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"Total issues remaining: {issue_counter - 1}")

if __name__ == "__main__":
    reorder_issues()
