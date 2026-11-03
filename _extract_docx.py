import docx
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

def iter_block_items(parent):
    parent_elm = parent.element.body
    for child in parent_elm.iterchildren():
        if child.tag == qn('w:p'):
            yield Paragraph(child, parent)
        elif child.tag == qn('w:tbl'):
            yield Table(child, parent)

def dump_doc(path, out):
    d = docx.Document(path)
    with open(out, 'w', encoding='utf-8') as f:
        for block in iter_block_items(d):
            if isinstance(block, Paragraph):
                txt = block.text.strip()
                if txt:
                    style = block.style.name if block.style else ''
                    f.write(f"[{style}] {txt}\n")
                else:
                    f.write("\n")
            elif isinstance(block, Table):
                f.write("\n=== TABLE ===\n")
                seen = set()
                for row in block.rows:
                    cells = []
                    for c in row.cells:
                        ct = c.text.replace('\n', ' / ').strip()
                        cells.append(ct)
                    line = " | ".join(cells)
                    f.write(line + "\n")
                f.write("=== END TABLE ===\n")

if __name__ == '__main__':
    src = r"C:\Users\WekandaSamuel\Desktop\people-pluse-app\People_Pulse_Unified_Master_Specification ..docx"
    dst = r"C:\Users\WekandaSamuel\AppData\Local\Temp\cline\spec.txt"
    dump_doc(src, dst)
    print("done")
