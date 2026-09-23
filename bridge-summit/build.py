"""Rebuild the Bridge Summit program PDF.

1. `npm i pretendard` in this folder, then `node render.js` -> new_pages.pdf (pp.4-7)
2. `python3 build.py <original.pdf>` -> TheBridgeSummit_2026_Official_Program.pdf
   Keeps pp.1-3 and 8-10 of the original, swaps in pp.4-7, and updates the
   check-in / opening times (09:00 / 09:30) on pp.2, 9, 10.
"""
import sys
import pymupdf as fitz

FONT = 'node_modules/pretendard/dist/public/static/Pretendard-Regular.otf'
BG = (12/255, 12/255, 13/255)
MUTED = (0x92/255, 0x8d/255, 0x88/255)


def replace_lines(page, repl):
    todo = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            text = ''.join(s['text'] for s in l['spans']).strip()
            for old, new in repl:
                if text == old:
                    s0 = l['spans'][0]
                    todo.append((fitz.Rect(l['bbox']), s0['origin'], s0['size'], new))
    for r, *_ in todo:
        page.add_redact_annot(r + (-0.5, -0.5, 0.5, 0.5), fill=BG)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
    for _, origin, size, new in todo:
        page.insert_text(origin, new, fontsize=size, fontname='pret', fontfile=FONT, color=MUTED)
    return len(todo)


src = fitz.open(sys.argv[1])
out = fitz.open()
out.insert_pdf(src, from_page=0, to_page=2)
out.insert_pdf(fitz.open('new_pages.pdf'))
out.insert_pdf(src, from_page=7, to_page=9)
box = [('월요일 · 입장 09:30', '월요일 · 입장 09:00'), ('오프닝 10:00', '오프닝 09:30')]
assert replace_lines(out[1], box) == 2
assert replace_lines(out[8], box) == 2
assert replace_lines(out[9], [('입장 09:30 · 오프닝 10:00', '입장 09:00 · 오프닝 09:30')]) == 1
out.set_metadata(src.metadata)
out.save('TheBridgeSummit_2026_Official_Program.pdf', garbage=3, deflate=True)
