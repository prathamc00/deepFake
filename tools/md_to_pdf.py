from pathlib import Path
import textwrap

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "REPORT.md"
DST = ROOT / "REPORT.pdf"


def clean_line(line: str) -> str:
    # Normalize markdown symbols for plain PDF text rendering.
    line = line.replace("`", "")
    line = line.replace("**", "")
    line = line.replace("### ", "")
    line = line.replace("## ", "")
    line = line.replace("# ", "")
    return line.rstrip()


def wrap_long_tokens(line: str, max_token_len: int = 60) -> str:
    parts = line.strip().split(" ")
    wrapped_parts = []
    for token in parts:
        if len(token) > max_token_len:
            wrapped_parts.append(" ".join(textwrap.wrap(token, width=max_token_len, break_long_words=True)))
        else:
            wrapped_parts.append(token)
    return " ".join(wrapped_parts)


def render_markdown_to_pdf(src: Path, dst: Path) -> None:
    content = src.read_text(encoding="utf-8")
    lines = content.splitlines()

    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_title("Deepfake Detection System Report")
    pdf.set_author("Project Author")

    pdf.set_font("Times", size=12)
    cell_width = 180

    for raw in lines:
        line = wrap_long_tokens(clean_line(raw))

        if not line:
            pdf.ln(4)
            continue

        if raw.startswith("# "):
            pdf.set_font("Times", style="B", size=18)
            pdf.multi_cell(cell_width, 10, line)
            pdf.ln(2)
            pdf.set_font("Times", size=12)
        elif raw.startswith("## "):
            pdf.set_font("Times", style="B", size=14)
            pdf.multi_cell(cell_width, 8, line)
            pdf.ln(1)
            pdf.set_font("Times", size=12)
        elif raw.startswith("### "):
            pdf.set_font("Times", style="B", size=12)
            pdf.multi_cell(cell_width, 7, line)
            pdf.set_font("Times", size=12)
        elif raw.lstrip().startswith("- "):
            bullet = "- " + line.lstrip()[2:]
            pdf.multi_cell(cell_width, 7, bullet)
        elif raw[:2].isdigit() and raw[1:3] == ". ":
            pdf.multi_cell(cell_width, 7, line)
        else:
            pdf.multi_cell(cell_width, 7, line)

    pdf.output(str(dst))


if __name__ == "__main__":
    render_markdown_to_pdf(SRC, DST)
    print(f"Created: {DST}")
