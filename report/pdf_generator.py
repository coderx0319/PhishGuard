from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, file_path="report.pdf"):
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    elements = []

    def add_section(title, content):
        elements.append(Paragraph(f"<b>{title}</b>", styles["Heading2"]))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(str(content), styles["Normal"]))
        elements.append(Spacer(1, 20))

    # Title
    elements.append(Paragraph("Phishing Email Analysis Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    # Sections
    add_section("Risk Score", data.get("risk_score"))
    add_section("Risk Reasons", data.get("risk_reasons"))
    add_section("IOCs", data.get("iocs"))
    add_section("Expanded URLs", data.get("expanded_urls"))
    add_section("HTML Analysis", data.get("html_analysis"))
    add_section("WHOIS", data.get("whois"))
    add_section("Email Auth", data.get("email_auth"))
    add_section("Threat Intelligence", data.get("threat_intel"))
    add_section("Attachments", data.get("attachments"))

    doc.build(elements)

    return file_path