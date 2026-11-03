import re

spec = open(r"C:\Users\WekandaSamuel\AppData\Local\Temp\cline\spec.txt", encoding="utf-8").read().splitlines()

out = open(r"C:\Users\WekandaSamuel\AppData\Local\Temp\cline\spec-outline.txt", "w", encoding="utf-8")

line_no = 0
tables = 0
for line in spec:
    line_no += 1
    if line.startswith("["):
        m = re.match(r"^\[(Heading \d+|Normal|List Paragraph|List Bullet|List Number|Table)\]\s*(.*)$", line)
        if m and m.group(1) == "Heading 1":
            out.write(f"{line_no:>6} [H1] {m.group(2)}\n")
        elif m and m.group(1) == "Heading 2":
            out.write(f"{line_no:>6}   [H2] {m.group(2)}\n")
        elif m and m.group(1) == "Heading 3":
            out.write(f"{line_no:>6}     [H3] {m.group(2)}\n")
    elif line.startswith("=== TABLE ==="):
        tables += 1
        out.write(f"{line_no:>6} ===TABLE {tables}===\n")
    elif line.startswith("=== END TABLE"):
        pass
out.close()
print("outline written")
