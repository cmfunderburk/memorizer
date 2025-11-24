"""
File I/O with Context Manager

Ensures file is closed even if errors occur.
"""
=== MEMO START ===
# Reading
with open('input.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    # or for line in f: ...

# Writing (overwrites)
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write("Hello\n")
    
# Appending
with open('log.txt', 'a') as f:
    f.write("New entry\n")

