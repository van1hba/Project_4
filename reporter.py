# scanner/reporter.py

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm

# small paragraph style for table cell content
styles = getSampleStyleSheet()
cell_style = ParagraphStyle(
    name="CellStyle",
    parent=styles["Normal"],
    fontSize=9,
    leading=11
)


def _cell_text(value):
    """
    Convert a cell value (which might be a list, dict, or other) into
    a safe string and wrap it in a Paragraph so ReportLab can measure/wrap it.
    """
    if value is None:
        text = "N/A"
    elif isinstance(value, (list, tuple)):
        # join lists/tuples into a readable string
        text = ", ".join(map(str, value)) if value else "N/A"
    elif isinstance(value, dict):
        # convert dict -> key: val pairs
        parts = []
        for k, v in value.items():
            parts.append(f"{k}: {v}")
        text = "; ".join(parts) if parts else "N/A"
    else:
        text = str(value)

    return Paragraph(text, cell_style)


def generate_pdf(filename, results):
    """
    results: dict mapping section name -> list of finding dicts
    Each finding dict should contain keys like "url", "payload", "missing", "issue"
    This function creates a nicely formatted PDF with tables.
    """
    doc = SimpleDocTemplate(filename, leftMargin=18*mm, rightMargin=18*mm,
                            topMargin=18*mm, bottomMargin=18*mm)
    styles_local = getSampleStyleSheet()

    story = []

    # Title
    title = "<b>Web Security Assessment Report</b>"
    story.append(Paragraph(title, styles_local['Title']))
    story.append(Spacer(1, 8))

    # Summary line
    total_findings = sum(len(v) for v in results.values() if isinstance(v, list))
    story.append(Paragraph(f"<b>Total findings: {total_findings}</b>", styles_local['Normal']))
    story.append(Spacer(1, 12))

    # For each section, create a table
    for section, data in results.items():
        story.append(Paragraph(f"<b>{section}</b>", styles_local['Heading2']))
        story.append(Spacer(1, 6))

        if not data:
            story.append(Paragraph("No issues found.", styles_local['Normal']))
            story.append(Spacer(1, 10))
            continue

        # Table header
        table_data = [
            [
                Paragraph("<b>URL</b>", styles_local['Normal']),
                Paragraph("<b>Details</b>", styles_local['Normal']),
                Paragraph("<b>Issue</b>", styles_local['Normal'])
            ]
        ]

        # Fill rows
        for item in data:
            url = item.get("url", "N/A")
            # prefer payload, otherwise missing list or other details
            details = item.get("payload", item.get("missing", item.get("details", "N/A")))
            issue = item.get("issue", "N/A")

            row = [
                _cell_text(url),
                _cell_text(details),
                _cell_text(issue)
            ]
            table_data.append(row)

        # Build table — set column widths relative to page width
        # Adjust column widths if your PDF page size / margins differ.
        col_widths = [90*mm, 60*mm, 40*mm]

        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))

        story.append(table)
        story.append(Spacer(1, 14))

    # Build the PDF
    doc.build(story)
