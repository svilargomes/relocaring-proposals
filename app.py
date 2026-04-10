"""
RELOCARING — Proposal Generator App
Run with:  streamlit run app.py
"""

import io
import os
import datetime
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate,
                                 Paragraph, Spacer, Table, TableStyle,
                                 PageBreak, HRFlowable, NextPageTemplate)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from PIL import Image as PILImage

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Relocaring — Proposal Generator",
    page_icon="📄",
    layout="centered"
)

# ── Brand colours ─────────────────────────────────────────────────────
TEAL       = colors.HexColor('#43708A')
TEAL_DARK  = colors.HexColor('#2A5570')
TEAL_LIGHT = colors.HexColor('#EAF3F8')
TEAL_MID   = colors.HexColor('#6490A8')
RED        = colors.HexColor('#C42728')
GREY_TEXT  = colors.HexColor('#4A5568')
GREY_RULE  = colors.HexColor('#D0DAE2')
WHITE      = colors.white

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
LOGO       = os.path.join(BASE_DIR, 'logo_relocaring.png')
LOGO_SMALL = os.path.join(BASE_DIR, 'logo_relocaring_footer.png')

COMPANY_PHONE   = "+351 910 147 707 / 918 841 086"
COMPANY_EMAIL   = "info@relocaring.com"
COMPANY_WEB     = "www.relocaring.com"
COMPANY_ADDRESS = "Rua D. Luís da Cunha, 63 · Casa Nortada · 2755-274 Alcabideche, Cascais"

# ── PDF generation function ───────────────────────────────────────────
def generate_pdf(client_name, service_description, proposal_date,
                 proposal_number, services, extra_notes):

    W, H = A4
    buffer = io.BytesIO()

    def _draw_logo(c, path, x, y, w):
        try:
            img = PILImage.open(path)
            h = w * img.height / img.width
            c.drawImage(path, x, y, width=w, height=h,
                        preserveAspectRatio=True, mask='auto')
        except: pass

    def _footer(c, page_num=None):
        c.setStrokeColor(TEAL_MID)
        c.setLineWidth(0.5)
        c.line(1.8*cm, 1.9*cm, W - 1.8*cm, 1.9*cm)
        _draw_logo(c, LOGO_SMALL, 1.8*cm, 0.45*cm, 68)
        c.setFont('Helvetica', 7)
        c.setFillColor(TEAL_MID)
        c.drawRightString(W - 1.8*cm, 1.3*cm,
            f'{COMPANY_EMAIL}  ·  {COMPANY_PHONE}  ·  {COMPANY_WEB}')
        if page_num:
            c.setFont('Helvetica-Bold', 8)
            c.setFillColor(TEAL)
            c.drawRightString(W - 1.8*cm, 0.55*cm, str(page_num))

    def bg_cover(c, doc):
        c.saveState()
        c.setFillColor(WHITE);     c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(TEAL);      c.rect(0, 0, 0.85*cm, H, fill=1, stroke=0)
        c.setFillColor(RED);       c.rect(0, H*0.75, 0.85*cm, H*0.25, fill=1, stroke=0)
        c.setFillColor(colors.HexColor('#F3F7F9'))
        c.rect(0.85*cm, H*0.38, W-0.85*cm, H*0.24, fill=1, stroke=0)
        c.setFillColor(TEAL_DARK); c.rect(0.85*cm, 0, W-0.85*cm, H*0.13, fill=1, stroke=0)
        c.setFillColor(RED);       c.rect(0.85*cm, H*0.13, W-0.85*cm, 0.28*cm, fill=1, stroke=0)
        _draw_logo(c, LOGO, W-185-1.8*cm, H-60-2.0*cm, 185)
        c.setFont('Helvetica-Bold', 50); c.setFillColor(TEAL_DARK)
        c.drawString(1.8*cm, H*0.53, 'FEE PROPOSAL')
        c.setFillColor(RED); c.rect(1.8*cm, H*0.38+6, 6.5*cm, 3, fill=1, stroke=0)
        c.setFont('Helvetica', 9.5); c.setFillColor(TEAL_MID)
        c.drawString(1.8*cm, H*0.38-10, 'Relocation & Immigration Services — Portugal')
        c.setFont('Helvetica-Bold', 7); c.setFillColor(RED)
        c.drawString(1.8*cm, H*0.295, 'ADDRESSED TO')
        c.setFont('Helvetica-Bold', 20); c.setFillColor(TEAL_DARK)
        c.drawString(1.8*cm, H*0.295-28, client_name.upper())
        c.setFont('Helvetica', 10); c.setFillColor(GREY_TEXT)
        c.drawString(1.8*cm, H*0.295-47, service_description)
        c.setFont('Helvetica', 8.5); c.setFillColor(TEAL_MID)
        c.drawString(1.8*cm, H*0.295-65, proposal_date)
        if proposal_number:
            c.setFont('Helvetica', 7.5); c.setFillColor(TEAL_MID)
            c.drawString(1.8*cm, H*0.295-82, f'Ref: {proposal_number}')
        c.setFont('Helvetica-Bold', 8.5); c.setFillColor(WHITE)
        c.drawString(2.2*cm, H*0.085, COMPANY_EMAIL)
        c.setFont('Helvetica', 8)
        c.drawString(2.2*cm, H*0.085-14, f'{COMPANY_PHONE}  ·  {COMPANY_WEB}')
        c.setFont('Helvetica', 7.5); c.setFillColor(colors.HexColor('#A8CBE0'))
        c.drawString(2.2*cm, H*0.085-27, COMPANY_ADDRESS)
        c.restoreState()

    def bg_inner(c, doc, page_num=None):
        c.saveState()
        c.setFillColor(WHITE);     c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(TEAL);      c.rect(0, 0, 0.55*cm, H, fill=1, stroke=0)
        c.setFillColor(RED);       c.rect(0, H-2.5*cm, 0.55*cm, 2.5*cm, fill=1, stroke=0)
        c.setFillColor(TEAL_LIGHT);c.rect(0.55*cm, H-1.0*cm, W-0.55*cm, 1.0*cm, fill=1, stroke=0)
        c.setFillColor(RED);       c.rect(W-1.0*cm, H-1.0*cm, 1.0*cm, 1.0*cm, fill=1, stroke=0)
        _footer(c, page_num)
        c.restoreState()

    def bg_p2(c, doc): bg_inner(c, doc, 2)
    def bg_p3(c, doc): bg_inner(c, doc, 3)
    def bg_p4(c, doc): bg_inner(c, doc, 4)
    def bg_p5(c, doc): bg_inner(c, doc, 5)

    def ps(name, **kw): return ParagraphStyle(name, **kw)

    S_LABEL   = ps('lbl', fontName='Helvetica-Bold', fontSize=8, textColor=TEAL_DARK, tracking=2)
    S_SECTION = ps('sec', fontName='Helvetica-Bold', fontSize=14, textColor=TEAL_DARK, spaceAfter=4)
    S_BODY    = ps('body', fontName='Helvetica', fontSize=9, textColor=GREY_TEXT, leading=15, alignment=TA_JUSTIFY, spaceAfter=8)
    S_SMALL   = ps('sm', fontName='Helvetica', fontSize=8, textColor=TEAL_MID, leading=13, spaceAfter=4)
    S_BULLET  = ps('bul', fontName='Helvetica', fontSize=8.5, textColor=GREY_TEXT, leading=14, spaceAfter=7, leftIndent=12, alignment=TA_JUSTIFY)
    S_TC      = ps('tc', fontName='Helvetica', fontSize=7.8, textColor=GREY_TEXT, leading=13, spaceAfter=5, alignment=TA_JUSTIFY)
    S_TC_HEAD = ps('tch', fontName='Helvetica-Bold', fontSize=13, textColor=TEAL_DARK, spaceAfter=6)

    class ReloDoc(BaseDocTemplate): pass

    doc = ReloDoc(buffer, pagesize=A4,
                  leftMargin=2.2*cm, rightMargin=1.8*cm,
                  topMargin=1.4*cm, bottomMargin=2.6*cm)

    cover_frame = Frame(1.8*cm, 2.2*cm, W-3.6*cm, H-4.4*cm, id='cover')
    inner_frame = Frame(1.8*cm, 2.6*cm, W-3.6*cm, H-3.8*cm, id='inner')

    doc.addPageTemplates([
        PageTemplate(id='cover',   frames=[cover_frame], onPage=bg_cover),
        PageTemplate(id='intro',   frames=[inner_frame], onPage=bg_p2),
        PageTemplate(id='fees',    frames=[inner_frame], onPage=bg_p3),
        PageTemplate(id='privacy', frames=[inner_frame], onPage=bg_p4),
        PageTemplate(id='tc',      frames=[inner_frame], onPage=bg_p5),
    ])

    story = []
    story.append(Spacer(1, 1*cm))
    story.append(NextPageTemplate('intro'))
    story.append(PageBreak())

    # Page 2 — Intro
    story.append(Paragraph("INTRODUCTION", S_LABEL))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(f"Dear {client_name},",
        ps('sal', fontName='Helvetica-Bold', fontSize=11, textColor=TEAL_DARK, spaceAfter=14)))
    intro_p1 = (f"Our sincere thanks for choosing <b>RELOCARING</b> to assist you with your "
                f"relocation and immigration journey to Portugal. We are pleased to present this "
                f"personalised proposal for <b>{client_name}</b>, outlining our recommended "
                f"services and associated fees.")
    for para in [intro_p1,
                 "With deep expertise in Professional Mobility and Immigration Services, RELOCARING strives to achieve excellence and deliver integrated, end-to-end solutions — offering peace of mind and a single, trusted point of contact throughout your entire process.",
                 "Our team works alongside qualified lawyers and solicitors to ensure that every aspect of your residency, legal and administrative requirements is handled professionally and with the care your move deserves."]:
        story.append(Paragraph(para, S_BODY))

    if extra_notes:
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(extra_notes, S_BODY))

    story.append(Spacer(1, 0.5*cm))

    overview = [
        ("VISA & IMMIGRATION", "Full management of your visa application, documentation review, AIMA appointments and residence permit."),
        ("NATIONALITY PROCESS", "End-to-end nationality application managed by a lawyer/solicitor, from checklist to IRN submission."),
        ("HOME SEARCH", "Personalised property search with accompanied viewings and lease negotiation."),
        ("SCHOOL SEARCH", "Identification and enrolment support for international and Portuguese schools."),
        ("ORIENTATION TOUR", "Guided half or full-day tour — neighbourhoods, services and lifestyle."),
        ("TAX & LEGAL ADVICE", "NIF, NISS, bank account, health centre registration and fiscal representation."),
    ]
    card_w = (W - 4.0*cm - 0.5*cm) / 2
    for i in range(0, len(overview), 2):
        def card(svc):
            t = Table([[Paragraph(svc[0], ps('ct', fontName='Helvetica-Bold', fontSize=8.5, textColor=TEAL_DARK))],
                       [Paragraph(svc[1], ps('cd', fontName='Helvetica', fontSize=8, textColor=GREY_TEXT, leading=13))]],
                      colWidths=[card_w])
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),TEAL_LIGHT),('LINEABOVE',(0,0),(-1,0),2.5,TEAL),
                                   ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
                                   ('TOPPADDING',(0,0),(0,0),8),('TOPPADDING',(0,1),(-1,-1),4),('BOTTOMPADDING',(0,-1),(-1,-1),10)]))
            return t
        g = Table([[card(overview[i]), card(overview[i+1])]], colWidths=[card_w, card_w], spaceBefore=6, hAlign='LEFT')
        g.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),
                                ('RIGHTPADDING',(0,0),(0,-1),6),('RIGHTPADDING',(1,0),(1,-1),0)]))
        story.append(g)
        story.append(Spacer(1, 0.25*cm))

    story.append(NextPageTemplate('fees'))
    story.append(PageBreak())

    # Page 3 — Fees
    story.append(Paragraph("SERVICES & FEES", S_LABEL))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Fee Proposal", S_SECTION))
    story.append(Paragraph("The fees outlined below are based on RELOCARING's understanding of your requirements at this stage. All fees are indicative and may be revised following review of further documentation. VAT, public costs, government fees, translations and certified copies are not included unless otherwise stated.", S_BODY))
    story.append(Spacer(1, 0.2*cm))

    col_w = [8.5*cm, 1.4*cm, 2.7*cm, 2.0*cm, 2.4*cm]
    def th(t): return Paragraph(f'<b>{t}</b>', ps('th', fontName='Helvetica-Bold', fontSize=8.5, textColor=WHITE, alignment=TA_CENTER))
    def td_l(t): return Paragraph(t, ps('tdl', fontName='Helvetica', fontSize=8.5, textColor=GREY_TEXT, alignment=TA_LEFT))
    def td_c(t): return Paragraph(t, ps('tdc', fontName='Helvetica', fontSize=8.5, textColor=GREY_TEXT, alignment=TA_CENTER))
    def td_r(t, bold=False, col=None): return Paragraph(t, ps('tdr', fontName='Helvetica-Bold' if bold else 'Helvetica', fontSize=8.5, textColor=col or GREY_TEXT, alignment=TA_RIGHT))

    fee_rows = [[th('SERVICES'), th('QTY'), th('UNIT PRICE'), th('DISC.'), th('TOTAL')]]
    grand_total = 0.0
    for idx, (name, qty, unit, disc) in enumerate(services):
        total = qty * unit * (1 - disc)
        grand_total += total
        disc_str = f"{int(disc*100)}%" if disc > 0 else "—"
        fee_rows.append([td_l(name), td_c(str(qty)),
                         td_r(f"{unit:,.2f} €".replace(',','.')),
                         td_c(disc_str),
                         td_r(f"{total:,.2f} €".replace(',','.'))])

    fee_rows.append([Paragraph('',ps('x')),Paragraph('',ps('x')),Paragraph('',ps('x')),
                     td_r('<b>TOTAL</b>', bold=True, col=TEAL_DARK),
                     td_r(f'<b>{grand_total:,.2f} €</b>'.replace(',','.'), bold=True, col=TEAL_DARK)])

    row_bgs = [('BACKGROUND',(0,i),(-1,i), TEAL_LIGHT if i%2==0 else WHITE) for i in range(1, len(fee_rows)-1)]
    fee_t = Table(fee_rows, colWidths=col_w, repeatRows=1)
    fee_t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),TEAL_DARK),*row_bgs,
                                ('BOX',(0,0),(-1,-2),0.5,GREY_RULE),('INNERGRID',(0,0),(-1,-2),0.5,GREY_RULE),
                                ('LINEABOVE',(0,-1),(-1,-1),1.5,TEAL_MID),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
                                ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
                                ('TOPPADDING',(0,-1),(-1,-1),10)]))
    story.append(fee_t)
    story.append(Spacer(1, 0.35*cm))
    story.append(Paragraph("* Public costs, translations, certified copies, document legalisations and VAT not included.", S_SMALL))
    story.append(Paragraph("* Displacement fees apply for distances exceeding 20 km from the Lisbon radius.", S_SMALL))
    story.append(Spacer(1, 0.45*cm))

    pay_t = Table([[Paragraph("PAYMENT CONDITIONS", ps('pch', fontName='Helvetica-Bold', fontSize=8, textColor=TEAL_DARK, tracking=1)),
                   Paragraph("50% upon acceptance of this proposal  +  50% upon submission of the process", ps('pcb', fontName='Helvetica', fontSize=8.5, textColor=GREY_TEXT))]],
                  colWidths=[5.5*cm, W-4.0*cm-5.5*cm])
    pay_t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),TEAL_LIGHT),('LINEABOVE',(0,0),(-1,-1),2.5,TEAL),
                                ('LINEBEFORE',(0,0),(0,-1),2.5,RED),('TOPPADDING',(0,0),(-1,-1),8),
                                ('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),10),
                                ('RIGHTPADDING',(0,0),(-1,-1),10),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(pay_t)
    story.append(Spacer(1, 0.45*cm))
    for b in ["Fees are indicative and based on information received. Additional details may impact final fees.",
              "All services must be authorised in writing prior to commencement.",
              "Services outside regular hours, weekends or public holidays incur a <b>30% surcharge</b>.",
              f"This proposal is valid for <b>60 days</b> from {proposal_date}."]:
        story.append(Paragraph(f'<font color="#C42728">◆</font>  {b}', S_BULLET))

    story.append(NextPageTemplate('privacy'))
    story.append(PageBreak())

    # Page 4 — Privacy
    story.append(Paragraph("DATA & PRIVACY", S_LABEL))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Notice of Terms of Use & Privacy Policy", S_SECTION))
    story.append(Paragraph("Please read this document carefully before signing.", S_SMALL))
    story.append(Spacer(1, 0.2*cm))
    for para in ["As part of your immigration and relocation process with Relocaring, Lda, we are required to gather and process sensitive personal information about you. The security and privacy of your personal information is of the utmost importance to us.",
                 "Your personal information will be stored in our secure database (SharePoint / Microsoft 365) and is always encrypted in transit and at rest. Physical copies are stored securely on-site and accessed only by your dedicated consultant when required for processing.",
                 "Your personal data may be shared with our business partners and relevant public entities solely to fulfil the services agreed with you. Beyond the agreed scope, it will not be processed or shared for any other purpose.",
                 f"At any time you may request access to, update, withdraw consent for, or request deletion of your personal data by contacting {COMPANY_EMAIL}."]:
        story.append(Paragraph(para, S_BODY))
    story.append(Spacer(1, 0.4*cm))
    story.append(Table([[Paragraph(f"I, <b>{client_name}</b>, give my informed consent to the gathering, storage and processing of mine and my family's personal data by Relocaring Lda., their Partners and relevant Public entities, for the purposes described above.",
                                   ps('cb', fontName='Helvetica', fontSize=9, textColor=TEAL_DARK, leading=15, alignment=TA_JUSTIFY))]],
                       colWidths=[W-4.0*cm],
                       style=[('BACKGROUND',(0,0),(-1,-1),TEAL_LIGHT),('LINEABOVE',(0,0),(-1,-1),2.5,TEAL),
                              ('LINEBEFORE',(0,0),(0,-1),2.5,RED),('TOPPADDING',(0,0),(-1,-1),12),
                              ('BOTTOMPADDING',(0,0),(-1,-1),12),('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14)]))
    story.append(Spacer(1, 0.8*cm))
    story.append(Table([[Paragraph('Signed', ps('sl', fontName='Helvetica', fontSize=8, textColor=TEAL_MID, tracking=1)),
                         Paragraph('Date', ps('sl2', fontName='Helvetica', fontSize=8, textColor=TEAL_MID, tracking=1))],
                        [Paragraph('_'*40, ps('sl3', fontName='Helvetica', fontSize=9, textColor=GREY_RULE)),
                         Paragraph('_'*24, ps('sl4', fontName='Helvetica', fontSize=9, textColor=GREY_RULE))]],
                       colWidths=[(W-4.0*cm)*0.62, (W-4.0*cm)*0.38],
                       style=[('VALIGN',(0,0),(-1,-1),'BOTTOM'),('LEFTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),4)]))

    story.append(NextPageTemplate('tc'))
    story.append(PageBreak())

    # Page 5 — T&C
    story.append(Paragraph("TERMS & CONDITIONS", S_LABEL))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Relocation and Immigration — Terms & Conditions", S_TC_HEAD))
    story.append(Spacer(1, 0.1*cm))
    for i, (h, t) in enumerate([
        ("Validity & Payment", "This proposal is valid for 60 days. Fees are invoiced 50% upon acceptance and 50% upon submission. All services must be authorised in writing."),
        ("Pricing & VAT", "All prices are in Euros and subject to VAT. Each invoice will be itemised by service. Fees are estimates; additional details may impact final costs."),
        ("Exclusions", "Services do not include translation fees, taxes, Government fees, courier costs, bank charges or other applicable third-party charges."),
        ("Liability", "RELOCARING assumes no responsibility for non-execution due to reasons beyond its control. Timing depends on public entities and timely delivery of documentation."),
        ("Out-of-Hours Services", "Services outside regular business hours, on weekends or public holidays incur a 30% surcharge, unless otherwise agreed in advance."),
        ("Additional Hours", "Additional hours may be charged if the client: (a) fails to provide required documents in due time; (b) provides incomplete information; (c) requests out-of-scope services; or (d) requires extra hours due to their own actions."),
        ("Third-Party Partners", "RELOCARING may engage qualified third-party partners for specific services. All legal matters are handled by lawyers or solicitors."),
        ("Displacement Fees", "Fees apply for distances exceeding 20 km from the Lisbon radius at €0.42/km."),
        ("Late Payment", "Interest on late payment applies in accordance with Portuguese law."),
        ("Cancellations", "Relocation: cancellable free of charge up to two weeks before arrival if under 2 hours of work performed. Immigration: 50% due if expertise already provided; 100% due after submission."),
    ], 1):
        story.append(Paragraph(f'<b>{i}. {h}</b>', ps(f'tchi{i}', fontName='Helvetica-Bold', fontSize=8, textColor=TEAL_DARK, spaceAfter=2)))
        story.append(Paragraph(t, S_TC))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GREY_RULE, spaceAfter=10))
    story.append(Table([[Paragraph("RELOCARING, LDA", ps('rld', fontName='Helvetica-Bold', fontSize=9, textColor=TEAL_DARK)),
                         Paragraph("CLIENT ACCEPTANCE", ps('caa', fontName='Helvetica-Bold', fontSize=9, textColor=WHITE))],
                        [Paragraph(" ", ps('sp')), Paragraph("Date: ___________________________", ps('cad', fontName='Helvetica', fontSize=8.5, textColor=WHITE))],
                        [Paragraph(" ", ps('sp2')), Paragraph("Signature: ______________________", ps('cas', fontName='Helvetica', fontSize=8.5, textColor=WHITE))]],
                       colWidths=[(W-4.0*cm)*0.45, (W-4.0*cm)*0.55],
                       style=[('BACKGROUND',(1,0),(1,-1),TEAL_DARK),('LINEABOVE',(1,0),(1,-1),3,RED),
                              ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
                              ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
                              ('VALIGN',(0,0),(-1,-1),'MIDDLE')]))

    doc.build([NextPageTemplate('cover')] + story)
    buffer.seek(0)
    return buffer, grand_total


# ══════════════════════════════════════════════════════════════════════
#  STREAMLIT UI
# ══════════════════════════════════════════════════════════════════════

# Header
st.image("logo_relocaring.png", width=220)
st.markdown("---")
st.title("Fee Proposal Generator")
st.caption("Fill in the fields below and click **Generate PDF** to download the proposal.")

# ── Section 1: Client Info ────────────────────────────────────────────
st.markdown("### 👤 Client Information")

col1, col2 = st.columns(2)
with col1:
    client_name = st.text_input("Client Name *", placeholder="e.g. John Smith")
with col2:
    proposal_number = st.text_input("Proposal Reference", placeholder="e.g. P01/26")

service_description = st.text_input(
    "Service Description (shown on cover) *",
    placeholder="e.g. Temporary Residence Permit & Nationality Process"
)

col3, col4 = st.columns(2)
with col3:
    proposal_date = st.date_input("Proposal Date", value=datetime.date.today())
    proposal_date_str = proposal_date.strftime("%-d %B, %Y") if hasattr(proposal_date, 'strftime') else str(proposal_date)

extra_notes = st.text_area(
    "Additional notes for introduction (optional)",
    placeholder="Add any personalised note for this client...",
    height=80
)

st.markdown("---")

# ── Section 2: Services & Pricing ─────────────────────────────────────
st.markdown("### 💶 Services & Pricing")
st.caption("Add up to 8 services. Leave Name empty to skip a row.")

# Available services from price list
SERVICE_OPTIONS = {
    "Custom / Type manually": "",
    "Temporary Residence Permit – Art. 15 (With Visa)": "Temporary Residence Permit – Art. 15\nIncludes: NIF · NISS · Bank Account · Health Centre registration",
    "Temporary Residence Permit – Without Visa (HQ/Blue Card)": "Temporary Residence Permit – Without Visa (HQ / Blue Card)\nIncludes: NIF · NISS · Bank Account · Health Centre registration",
    "Temporary Residence Permit – Without Visa (Others)": "Temporary Residence Permit – Without Visa\nIncludes: NIF · NISS · Bank Account · Health Centre registration",
    "Nationality Process": "Nationality Process\nOriginary / Descendant / Resident / Marriage / Conservation — full management by lawyer/solicitor with IRN follow-up",
    "D1 Visa – Subordinate": "D1 Residence Visa – Subordinate\nFull visa application management",
    "D2 Visa – Entrepreneur": "D2 Residence Visa – Entrepreneur\nFull visa application management",
    "D3 Visa – Highly Qualified": "D3 Residence Visa – Highly Qualified\nFull visa application management",
    "D7 Visa – Passive Income": "D7 Residence Visa – Passive Income\nFull visa application management",
    "D8 Visa – Digital Nomad": "D8 Residence Visa – Digital Nomad\nFull visa application management",
    "Home Search – 1 Day": "Home Search – 1 Day\nBetween 6 to 8 property visits (Lisbon region)",
    "Home Search – 2 Days": "Home Search – 2 Days\nBetween 12 to 14 property visits (Lisbon region)",
    "School Search": "School Search\nIdentification and enrolment support for international and Portuguese schools",
    "Orientation Tour – Half Day": "Orientation Tour – Half Day (4 hours)\nGuided tour of Lisbon region",
    "Orientation Tour – Full Day": "Orientation Tour – Full Day (up to 7 hours)\nGuided tour of Lisbon region",
    "AIMA Appointment": "AIMA Appointment\nAppointment scheduling and management",
    "AIMA Accompaniment": "AIMA Accompaniment\nPhysical accompaniment to AIMA appointment",
    "NIF – Tax Number": "NIF – Tax Number Registration\nNon-resident without fiscal representation",
    "NISS – Social Security": "NISS – Social Security Number\nOnline registration and appointment",
    "Bank Account Opening": "Bank Account Opening\nAssistance with Portuguese bank account",
    "TR Renewal – Online": "Temporary Residence Renewal – Online",
    "EU Registration Certificate": "EU Registration Certificate\nFor EU citizens registering in Portugal",
    "Family Reunion – Spouse": "Family Reunion – Spouse\nIncludes: NIF · NISS · Bank Account · Health Centre",
    "Family Reunion – per Child": "Family Reunion – per Child\nIncludes: NIF · Health Centre registration",
    "Driving Licence Exchange – EU": "Driving Licence Exchange – EU",
    "Driving Licence Exchange – Non-EU": "Driving Licence Exchange – Non-EU",
    "Car Legalization – EU": "Car Legalization – EU vehicle",
    "Car Legalization – Non-EU": "Car Legalization – Non-EU vehicle",
    "Utilities Setup": "Utilities Setup\nWater, Electricity, Gas, Internet (activation)",
    "Lease Agreement Negotiation": "Lease Agreement Negotiation\nInitial and final negotiation — Lawyer/Solicitor review",
    "Check-in / Check-out Report": "Check-in / Check-out Report",
    "Pet Registration": "Pet Registration",
}

PRICE_DEFAULTS = {
    "Temporary Residence Permit – Art. 15 (With Visa)": 893.00,
    "Temporary Residence Permit – Without Visa (HQ/Blue Card)": 1200.00,
    "Temporary Residence Permit – Without Visa (Others)": 800.00,
    "Nationality Process": 1500.00,
    "D1 Visa – Subordinate": 1260.00,
    "D2 Visa – Entrepreneur": 1575.00,
    "D3 Visa – Highly Qualified": 1260.00,
    "D7 Visa – Passive Income": 1575.00,
    "D8 Visa – Digital Nomad": 1155.00,
    "Home Search – 1 Day": 945.00,
    "Home Search – 2 Days": 1523.00,
    "School Search": 525.00,
    "Orientation Tour – Half Day": 420.00,
    "Orientation Tour – Full Day": 630.00,
    "AIMA Appointment": 210.00,
    "AIMA Accompaniment": 315.00,
    "NIF – Tax Number": 210.00,
    "NISS – Social Security": 200.00,
    "Bank Account Opening": 263.00,
    "TR Renewal – Online": 235.00,
    "EU Registration Certificate": 263.00,
    "Family Reunion – Spouse": 840.00,
    "Family Reunion – per Child": 210.00,
    "Driving Licence Exchange – EU": 263.00,
    "Driving Licence Exchange – Non-EU": 315.00,
    "Car Legalization – EU": 1125.00,
    "Car Legalization – Non-EU": 1125.00,
    "Utilities Setup": 210.00,
    "Lease Agreement Negotiation": 368.00,
    "Check-in / Check-out Report": 158.00,
    "Pet Registration": 158.00,
}

services = []
for i in range(1, 7):
    st.markdown(f"**Service {i}**")
    c1, c2, c3, c4 = st.columns([3, 1.2, 1.2, 1.2])

    with c1:
        selected = st.selectbox(
            f"Select service {i}",
            options=list(SERVICE_OPTIONS.keys()),
            key=f"sel_{i}",
            label_visibility="collapsed"
        )
        if selected == "Custom / Type manually":
            name = st.text_input(f"Service name {i}", placeholder="Service name and description", key=f"name_{i}", label_visibility="collapsed")
        else:
            name = SERVICE_OPTIONS[selected]
            st.caption(f"✓ {selected}")

    with c2:
        default_price = PRICE_DEFAULTS.get(selected, 0.0)
        price = st.number_input("Unit Price (€)", min_value=0.0, value=default_price, step=50.0, key=f"price_{i}", label_visibility="collapsed")
        st.caption("Unit price €")

    with c3:
        qty = st.number_input("Qty", min_value=1, value=1, step=1, key=f"qty_{i}", label_visibility="collapsed")
        st.caption("Qty")

    with c4:
        disc_options = {"No discount": 0.0, "10%": 0.10, "15%": 0.15, "20%": 0.20, "25%": 0.25, "30%": 0.30}
        disc_label = st.selectbox("Discount", options=list(disc_options.keys()), key=f"disc_{i}", label_visibility="collapsed")
        disc = disc_options[disc_label]
        st.caption("Discount")

    if name and price > 0:
        services.append((name, qty, price, disc))

st.markdown("---")

# ── Live total preview ────────────────────────────────────────────────
if services:
    st.markdown("### 🧮 Quote Summary")
    total_preview = 0.0
    for name, qty, price, disc in services:
        line_total = qty * price * (1 - disc)
        total_preview += line_total
        disc_str = f"(-{int(disc*100)}%)" if disc > 0 else ""
        display_name = name.split('\n')[0]
        st.markdown(f"- {display_name} × {qty} = **€{line_total:,.2f}** {disc_str}")
    st.success(f"**Total: €{total_preview:,.2f}**")
    st.markdown("---")

# ── Generate button ───────────────────────────────────────────────────
st.markdown("### 📄 Generate Proposal")

if st.button("⬇️ Generate & Download PDF", type="primary", use_container_width=True):
    if not client_name:
        st.error("Please enter a client name.")
    elif not service_description:
        st.error("Please enter a service description.")
    elif not services:
        st.error("Please add at least one service with a price.")
    else:
        with st.spinner("Generating proposal..."):
            try:
                pdf_buffer, grand_total = generate_pdf(
                    client_name, service_description, proposal_date_str,
                    proposal_number, services, extra_notes
                )
                filename = f"Relocaring_Proposal_{client_name.replace(' ', '_')}.pdf"
                st.download_button(
                    label=f"📥 Download  {filename}",
                    data=pdf_buffer,
                    file_name=filename,
                    mime="application/pdf",
                    use_container_width=True
                )
                st.success(f"✅ Proposal ready for **{client_name}** — Total: **€{grand_total:,.2f}**")
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
                st.exception(e)

st.markdown("---")
st.caption("Relocaring · info@relocaring.com · +351 910 147 707")
