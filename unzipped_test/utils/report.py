import io

try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_report(trust_score, explanation, profile=None, anomalies=None, risk_level=None):
    """Generate a professional PDF report of the data quality analysis.

    Creates a downloadable PDF containing trust score, explanation,
    dataset overview, anomaly summary, and risk assessment.

    Args:
        trust_score: The overall trust score (0-100).
        explanation: The AI/rule-based explanation string.
        profile: Optional data profile dictionary for detailed reporting.
        anomalies: Optional anomaly counts dictionary.
        risk_level: Optional risk level string.

    Returns:
        bytes or None: PDF content as bytes for download, or None if reportlab unavailable.
    """
    if not REPORTLAB_AVAILABLE:
        return None

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Title'],
        fontSize=24, spaceAfter=20, textColor=colors.HexColor('#1a1a2e')
    )
    heading_style = ParagraphStyle(
        'CustomHeading', parent=styles['Heading2'],
        fontSize=14, spaceAfter=10, textColor=colors.HexColor('#16213e')
    )

    content = []

    # Title
    content.append(Paragraph("🕵️ Data Lie Detector — Quality Report", title_style))
    content.append(Spacer(1, 12))

    # Trust Score
    content.append(Paragraph(f"Trust Score: {trust_score} / 100", heading_style))
    content.append(Spacer(1, 8))

    # Risk Level
    if risk_level:
        content.append(Paragraph(f"Decision Risk: {risk_level}", heading_style))
        content.append(Spacer(1, 8))

    # Explanation
    content.append(Paragraph("Analysis Summary", heading_style))
    content.append(Paragraph(explanation, styles["BodyText"]))
    content.append(Spacer(1, 12))

    # Dataset Overview
    if profile:
        content.append(Paragraph("Dataset Overview", heading_style))
        overview_data = [
            ["Metric", "Value"],
            ["Rows", str(profile.get("rows", "N/A"))],
            ["Columns", str(profile.get("cols", "N/A"))],
            ["Duplicate Rows", str(profile.get("duplicates", "N/A"))],
            ["Numeric Columns", str(len(profile.get("numeric_cols", [])))],
            ["Categorical Columns", str(len(profile.get("categorical_cols", [])))],
        ]
        table = Table(overview_data, colWidths=[3 * inch, 3 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ]))
        content.append(table)
        content.append(Spacer(1, 12))

    # Anomalies
    if anomalies:
        content.append(Paragraph("Anomaly Summary", heading_style))
        anomaly_data = [["Column", "Outlier Count"]]
        for col, count in anomalies.items():
            anomaly_data.append([col, str(count)])
        table = Table(anomaly_data, colWidths=[3 * inch, 3 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ]))
        content.append(table)

    doc.build(content)
    buffer.seek(0)
    return buffer.getvalue()
