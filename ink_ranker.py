import subprocess
import json
import sys
from pathlib import Path
from docx import Document
from docx.shared import Pt
from PIL import Image
import fitz


BASE_DIR = Path(__file__).parent
SAMPLE_TEXT = BASE_DIR / "sample_text.txt"
FONTS_FILE = BASE_DIR / "fonts.txt"
OUTPUT_DIR = BASE_DIR / "output"
RESULTS_FILE = OUTPUT_DIR / "results.json"
DPI = 300
FONT_SIZE = 12
DARKNESS_THRESHOLD = 200  # pixels below this (per channel avg) count as "ink"
KEEP_SAMPLES = 3  # number of font render samples to keep for testing
BASELINE_FONT = "Arial"


def create_docx(text, font_name, out_path):
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = font_name
    style.font.size = Pt(FONT_SIZE)
    for paragraph in text.split("\n"):
        doc.add_paragraph(paragraph)
    doc.save(str(out_path))


def docx_to_pdf(docx_path, out_dir):
    subprocess.run([
        "soffice", "--headless", "--convert-to", "pdf",
        "--outdir", str(out_dir), str(docx_path)
    ], check=True, capture_output=True)
    return out_dir / docx_path.with_suffix(".pdf").name


def measure_ink(pdf_path):
    """Render PDF pages at target DPI and count total dark (ink) pixels."""
    doc = fitz.open(pdf_path)
    dark_pixels = 0
    zoom = DPI / 72  # PDF default is 72 DPI
    matrix = fitz.Matrix(zoom, zoom)
    for page in doc:
        pix = page.get_pixmap(matrix=matrix)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples).convert("L")
        pixels = img.get_flattened_data()
        dark_pixels += sum(1 for p in pixels if p < DARKNESS_THRESHOLD)
    page_count = len(doc)
    doc.close()
    return dark_pixels, page_count


def cleanup(out_dir, keep_fonts):
    """Remove generated files, keeping samples for specified fonts."""
    keep_prefixes = {f.replace(" ", "_") for f in keep_fonts}
    for f in out_dir.iterdir():
        if f.name == "results.json":
            continue
        stem_prefix = f.stem.split("_")[0] if "_" in f.stem else f.stem
        if stem_prefix not in keep_prefixes:
            f.unlink()


def run(fonts):
    OUTPUT_DIR.mkdir(exist_ok=True)
    text = SAMPLE_TEXT.read_text(encoding="utf-8")
    results = {}

    # ensure baseline font is processed first
    if BASELINE_FONT in fonts:
        fonts = [BASELINE_FONT] + [f for f in fonts if f != BASELINE_FONT]

    for font in fonts:
        safe_name = font.replace(" ", "_")
        docx_path = OUTPUT_DIR / f"{safe_name}.docx"
        print(f"Processing: {font}")

        create_docx(text, font, docx_path)
        pdf_path = docx_to_pdf(docx_path, OUTPUT_DIR)
        dark_pixels, page_count = measure_ink(pdf_path)

        results[font] = {
            "dark_pixels": dark_pixels,
            "dpi": DPI,
            "font_size": FONT_SIZE,
            "pages": page_count
        }
        print(f"  {font}: {dark_pixels:,} dark pixels ({page_count} pages)")

    # compute relative ink usage vs baseline
    baseline_pixels = results.get(BASELINE_FONT, {}).get("dark_pixels")
    if baseline_pixels:
        print(f"\n{'Font':<35} {'Ink vs ' + BASELINE_FONT:>15}")
        print("-" * 52)
        ranked = sorted(results.items(), key=lambda x: x[1]["dark_pixels"])
        for font, data in ranked:
            relative = data["dark_pixels"] / baseline_pixels * 100
            data["ink_vs_baseline"] = round(relative, 1)
            marker = " <-- baseline" if font == BASELINE_FONT else ""
            print(f"  {font:<33} {relative:>7.1f}%{marker}")

    # keep first N font samples for testing
    keep_fonts = fonts[:KEEP_SAMPLES]
    cleanup(OUTPUT_DIR, keep_fonts)

    RESULTS_FILE.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nResults saved to {RESULTS_FILE}")


def load_fonts():
    if not FONTS_FILE.exists():
        print(f"Font list not found: {FONTS_FILE}")
        sys.exit(1)
    fonts = [line.strip() for line in FONTS_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not fonts:
        print("No fonts listed in fonts.txt")
        sys.exit(1)
    return fonts


if __name__ == "__main__":
    run(load_fonts())
