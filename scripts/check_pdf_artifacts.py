#!/usr/bin/env python3
"""
Check PDF for Unicode artifacts mentioned in O3 Pro audit.
This script extracts text from the PDF and searches for known artifacts.
"""

import sys
import subprocess
from pathlib import Path


def extract_pdf_text(pdf_path):
    """Extract text from PDF using pdftotext."""
    try:
        result = subprocess.run(
            ["pdftotext", str(pdf_path), "-"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error extracting text from PDF: {e}")
        return None
    except FileNotFoundError:
        print("pdftotext not found. Please install poppler-utils.")
        return None


def check_artifacts(text):
    """Check for known artifacts in the text."""
    artifacts = {
        "10ff¹ff Hz": "Corrupted superscript pattern for 10⁻¹⁷ Hz",
        "10ff1ff Hz": "Corrupted superscript pattern variant",
        "Hff": "Corrupted Hz unit",
        "ff27 times": "Corrupted approximation symbol",
        "ﬀ": "ff ligature",
        "ﬁ": "fi ligature",
        "ﬂ": "fl ligature",
    }

    found_artifacts = []
    lines = text.split("\n")

    for artifact, description in artifacts.items():
        for line_num, line in enumerate(lines, 1):
            if artifact in line:
                found_artifacts.append(
                    {
                        "artifact": artifact,
                        "description": description,
                        "line": line_num,
                        "context": line.strip(),
                    }
                )

    return found_artifacts


def main():
    if len(sys.argv) < 2:
        pdf_path = Path("output/oscillating_brane_theory_latest.pdf")
    else:
        pdf_path = Path(sys.argv[1])

    if not pdf_path.exists():
        print(f"PDF file not found: {pdf_path}")
        return

    print(f"Checking PDF for artifacts: {pdf_path}")

    # Extract text
    text = extract_pdf_text(pdf_path)
    if not text:
        return

    # Check for artifacts
    artifacts = check_artifacts(text)

    if artifacts:
        print(f"\n❌ Found {len(artifacts)} artifact(s):")
        for item in artifacts:
            print(f"\nLine {item['line']}: {item['artifact']}")
            print(f"Description: {item['description']}")
            print(f"Context: {item['context']}")
    else:
        print("\n✅ No artifacts found!")

    # Also check for correct patterns
    correct_patterns = ["10^{-17} Hz", "10⁻¹⁷ Hz", "1.6 × 10"]
    found_correct = []

    for pattern in correct_patterns:
        if pattern in text:
            found_correct.append(pattern)

    if found_correct:
        print(f"\n✅ Found correct patterns: {', '.join(found_correct)}")


if __name__ == "__main__":
    main()
