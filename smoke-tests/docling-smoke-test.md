# Docling Smoke Test

## 1. Title & Purpose

Docling is the HX document-processing component on HX-16. This smoke test validates that Docling can convert a deterministic local PDF to Markdown and, for the HX-assigned configuration, that the pre-staged Granite-Docling VLM can process the same document on CPU.

**Scope:** Docling core conversion plus the HX-required Granite-Docling CPU-first probe. Docling MCP remains a separate companion gate.

## 2. Prerequisites

- Docling is installed natively in the accepted HX-16 Python environment.
- Python `3.10+` is available; current Docling releases no longer support Python 3.9.
- The `docling` CLI is available.
- Granite-Docling is already staged/cached locally for the HX-16 VLM test. The smoke test must not depend on downloading the model at execution time.
- CPU execution is available. The Granite-Docling smoke path explicitly uses:

```text
--device cpu
```

- No environment variable is required for the basic conversion test.
- If the accepted model cache uses a non-default location, the corresponding model-cache environment variable/path must already be part of the HX-16 configuration before the test starts.
- No external document URL, database, API key, Docker, Podman, Kubernetes, or temporary container is required.

## 3. Test Steps

1. Create a disposable working directory.

```bash
mkdir -p hx-docling-smoke
cd hx-docling-smoke
```

2. Save the following as `make_smoke_pdf.py`. It creates a one-page PDF using only the Python standard library.

```python
from pathlib import Path

TEXT = "HX DOCLING SMOKE 9271"
OUT = Path("hx-docling-smoke.pdf")

content = f"BT /F1 28 Tf 72 720 Td ({TEXT}) Tj ET".encode("ascii")
objects = [
    b"<< /Type /Catalog /Pages 2 0 R >>",
    b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
    b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
    b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    b"<< /Length %d >>\nstream\n" % len(content) + content + b"\nendstream",
]

pdf = bytearray(b"%PDF-1.4\n")
offsets = [0]
for number, obj in enumerate(objects, start=1):
    offsets.append(len(pdf))
    pdf.extend(f"{number} 0 obj\n".encode("ascii"))
    pdf.extend(obj)
    pdf.extend(b"\nendobj\n")

xref = len(pdf)
pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
pdf.extend(b"0000000000 65535 f \n")
for offset in offsets[1:]:
    pdf.extend(f"{offset:010d} 00000 n \n".encode("ascii"))

pdf.extend(
    (
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref}\n%%EOF\n"
    ).encode("ascii")
)

OUT.write_bytes(pdf)
print(f"created {OUT} with token: {TEXT}")
```

3. Generate the sample PDF.

```bash
python3 make_smoke_pdf.py
```

4. Run the normal Docling conversion using the Python API. Save as `docling_native_smoke.py`.

```python
from pathlib import Path
from docling.document_converter import DocumentConverter

TOKEN = "HX DOCLING SMOKE 9271"
source = Path("hx-docling-smoke.pdf")

result = DocumentConverter().convert(source)
markdown = result.document.export_to_markdown()

assert "HX" in markdown, markdown
assert "DOCLING" in markdown, markdown
assert "9271" in markdown, markdown

Path("hx-docling-native.md").write_text(markdown, encoding="utf-8")
print("DOCLING_NATIVE_SMOKE_PASS")
```

Run it:

```bash
python3 docling_native_smoke.py
```

5. Run the HX-required Granite-Docling VLM path on CPU.

```bash
mkdir -p hx-docling-vlm-out

docling hx-docling-smoke.pdf \
  --pipeline vlm \
  --vlm-model granite_docling \
  --device cpu \
  --output hx-docling-vlm-out
```

6. Validate the VLM output.

```bash
python3 - <<'PY'
from pathlib import Path

files = list(Path("hx-docling-vlm-out").glob("*.md"))
assert files, "no Granite-Docling Markdown output found"
text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in files)
upper = text.upper()
assert "HX" in upper, text
assert "DOCLING" in upper, text
assert "9271" in upper, text
print("DOCLING_GRANITE_SMOKE_PASS")
PY
```

7. Record the Docling version, Granite-Docling model/revision, device (`cpu`), conversion output, and console results with the normal HX smoke-test evidence.

## 4. Sample Data

The generated PDF contains one known text line:

```text
HX DOCLING SMOKE 9271
```

The PDF is created locally by the test itself. No downloaded test document is required.

## 5. Expected Output

The PDF generator prints:

```text
created hx-docling-smoke.pdf with token: HX DOCLING SMOKE 9271
```

The normal Docling conversion must print:

```text
DOCLING_NATIVE_SMOKE_PASS
```

The Granite-Docling CPU-first probe must print:

```text
DOCLING_GRANITE_SMOKE_PASS
```

Pass means:

- Docling imports and converts the generated PDF successfully;
- normal Markdown output contains `HX`, `DOCLING`, and `9271`;
- Granite-Docling runs with `--device cpu` and exits successfully;
- the Granite-Docling Markdown output contains `HX`, `DOCLING`, and `9271`;
- no external source document or cloud model is needed during execution.

## 6. Cleanup / Teardown

After evidence capture, remove only the disposable smoke-test artifacts:

```bash
cd ..
rm -rf hx-docling-smoke
```

Do **not** remove the installed Docling environment, Granite-Docling model cache, or any persistent HX-16 application configuration.

**No containers are created by this test.**

## Evidence

Retain the run through the standard bundle described in
`docs/05-evidence/README.md`: manifest, result, cleanup proof, and the
supporting capture of the generator output and the Markdown from both conversion paths.

Record the Docling version, the Granite-Docling checkpoint and revision, the
device used for the Granite run, the `HX`, `DOCLING` and `9271` values found
in each Markdown output, and confirmation that no external source document
or cloud model was needed.
