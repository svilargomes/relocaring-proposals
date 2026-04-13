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

# ── Password protection ───────────────────────────────────────────────
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if not st.session_state.authenticated:
        st.image("logo_relocaring.png", width=200)
        st.title("Relocaring — Proposal Generator")
        st.markdown("---")
        password = st.text_input("Enter password to access the app", type="password")
        if st.button("Login", use_container_width=True):
            if password == "relocaring2026":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
        st.stop()

check_password()

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

# ── Full 2026 service catalogue  (label: (pdf_text, price)) ──────────
SERVICE_CATALOGUE = {
    "— Select a service —": ("", 0.0),
    # RESIDENCE VISAS
    "D1 Visa – Subordinate":                         ("D1 Residence Visa – Subordinate\nFull visa application management", 1260.00),
    "D2 Visa – Entrepreneur":                        ("D2 Residence Visa – Entrepreneur\nFull visa application management", 1575.00),
    "D3 Visa – Highly Qualified":                    ("D3 Residence Visa – Highly Qualified\nFull visa application management", 1260.00),
    "D4 Visa – Student Internship":                  ("D4 Visa – Student Internship (non-EEA)\nFull visa application management", 840.00),
    "D5 Visa – University Student":                  ("D5 Visa – University Student\nFull visa application management", 840.00),
    "D6 Visa – Family Accompaniment (Spouse)":       ("D6 Visa – Family Accompaniment Spouse\nFull visa application management", 630.00),
    "D6 Visa – Family Accompaniment (Child)":        ("D6 Visa – Family Accompaniment per Child\nFull visa application management", 158.00),
    "D7 Visa – Passive Income":                      ("D7 Residence Visa – Passive Income\nFull visa application management", 1575.00),
    "D8 Visa – Digital Nomad":                       ("D8 Residence Visa – Digital Nomad\nFull visa application management", 1155.00),
    # SHORT STAY
    "Short Stay – Tourism/Schengen (With Accompaniment)":  ("Short Stay Visa – Tourism / Schengen (With Accompaniment)", 473.00),
    "Short Stay – Tourism/Schengen (Without Accompaniment)": ("Short Stay Visa – Tourism / Schengen (Without Accompaniment)", 315.00),
    # TEMPORARY STAY
    "Temporary Stay – Local Work":                   ("Temporary Stay Visa – Local Work", 1260.00),
    "Temporary Stay – Assignment":                   ("Temporary Stay Visa – Assignment", 945.00),
    "Temporary Stay – Others":                       ("Temporary Stay Visa – Others", 1050.00),
    # RESIDENCE PERMITS
    "Temp. Residence Permit – With Visa (Art.15)":              ("Temporary Residence Permit – Art. 15 (With Visa)\nIncludes: NIF · NISS · Bank Account · Health Centre", 893.00),
    "Temp. Residence Permit – Without Visa (HQ / Blue Card)":   ("Temporary Residence Permit – Without Visa (HQ / Blue Card)\nIncludes: NIF · NISS · Bank Account · Health Centre", 1260.00),
    "Temp. Residence Permit – Without Visa (Others)":           ("Temporary Residence Permit – Without Visa\nIncludes: NIF · NISS · Bank Account · Health Centre", 840.00),
    "Family Reunion – Spouse / Parents":                        ("Family Reunion – Spouse / Parents\nIncludes: NIF · NISS · Bank Account · Health Centre", 840.00),
    "Family Reunion – per Child":                               ("Family Reunion – per Child\nIncludes: NIF · Health Centre registration", 210.00),
    "EU Family Residence":                                      ("EU Family Residence Permit\nIncludes: NIF · NISS · Bank Account · Health Centre", 893.00),
    "EU Registration Certificate":                              ("EU Registration Certificate\nFor EU citizens registering in Portugal", 263.00),
    "TR Renewal – Online":                                      ("Temporary Residence Renewal – Online", 235.00),
    "TR Renewal – With Accompaniment":                          ("Temporary Residence Renewal – With Accompaniment", 550.00),
    # NATIONALITY
    "Nationality Process":                           ("Nationality Process\nOriginary / Descendant / Resident / Marriage / Conservation\nFull management by lawyer/solicitor with IRN follow-up", 1500.00),
    # APPOINTMENTS & ADMIN
    "AIMA Appointment":                              ("AIMA Appointment\nAppointment scheduling and management", 210.00),
    "AIMA Appointment – Urgent":                     ("AIMA Appointment – Urgent", 263.00),
    "AIMA Accompaniment":                            ("AIMA Accompaniment\nPhysical accompaniment to AIMA appointment (up to 3 hours)", 315.00),
    "Process Analysis – Docs (with AIMA)":           ("Process Analysis – Documentation Analysis & Validation with AIMA", 158.00),
    "Process Analysis – Visa Type A":                ("Process Analysis – Visa Type A\nChecklist + Documentation analysis + validation + Admin follow-up", 263.00),
    "Process Analysis – Visa Type B/H":              ("Process Analysis – Visa Type B/H\nChecklist + Documentation analysis + validation + Admin follow-up", 268.00),
    "Card Retrieval – With POA":                     ("Residence Card Retrieval – With Power of Attorney", 210.00),
    # ADMINISTRATIVE
    "NIF – Non-Resident (No Fiscal Rep)":            ("NIF – Tax Number (Non-Resident, Without Fiscal Representation)", 210.00),
    "NIF – Non-Resident (With Fiscal Rep)":          ("NIF – Tax Number (Non-Resident, With Fiscal Representation)\nWithout VAT representation", 315.00),
    "NIF – Resident":                                ("NIF – Tax Number (Resident)", 132.00),
    "NISS – Social Security":                        ("NISS – Social Security Number\nOnline registration and appointment", 200.00),
    "Bank Account Opening":                          ("Bank Account Opening\nAssistance with Portuguese bank account", 263.00),
    "Health Centre Registration":                    ("Health Centre Registration\nAfter Temporary Residence", 158.00),
    # RELOCATION
    "Orientation Tour – Half Day":                   ("Orientation Tour – Half Day (4 hours)\nGuided tour of Lisbon region", 420.00),
    "Orientation Tour – Full Day":                   ("Orientation Tour – Full Day (up to 7 hours)\nGuided tour of Lisbon region", 630.00),
    "Home Search – Half Day":                        ("Home Search – Half Day\nBetween 3 to 4 property visits (Lisbon region)", 473.00),
    "Home Search – 1 Day":                           ("Home Search – 1 Day\nBetween 6 to 8 property visits (Lisbon region)", 945.00),
    "Home Search – 2 Days":                          ("Home Search – 2 Days\nBetween 12 to 14 property visits (Lisbon region)", 1523.00),
    "Long-Term Accommodation – 1 Day":               ("Long-Term Accommodation Search – 1 Day\nIncludes: contract negotiation · check-in report · utilities", 1680.00),
    "Long-Term Accommodation – 2 Days":              ("Long-Term Accommodation Search – 2 Days\nIncludes: contract negotiation · check-in report · utilities", 2258.00),
    "Temporary Accommodation Search":                ("Temporary Accommodation Search\nUp to 4 options", 473.00),
    "School Search":                                 ("School Search\nIdentification and enrolment support for international and Portuguese schools", 525.00),
    "Lease Agreement Negotiation":                   ("Lease Agreement Negotiation\nInitial and final negotiation — Lawyer/Solicitor review", 368.00),
    "Check-in / Check-out Report":                   ("Check-in / Check-out Report", 158.00),
    "Utilities Setup":                               ("Utilities Setup\nWater, Electricity, Gas, Internet (activation)", 210.00),
    "Tenancy Management – VIP":                      ("Tenancy Management – VIP\nUp to 2 hours per week", 189.00),
    # LICENCES & VEHICLES
    "Driving Licence Exchange – EU":                 ("Driving Licence Exchange – EU", 263.00),
    "Driving Licence Exchange – Non-EU":             ("Driving Licence Exchange – Non-EU", 315.00),
    "Driving Licence Registration":                  ("Driving Licence Registration", 210.00),
    "Car Legalization – EU":                         ("Car Legalization – EU vehicle", 1125.00),
    "Car Legalization – Non-EU":                     ("Car Legalization – Non-EU vehicle", 1125.00),
    "Pet Registration":                              ("Pet Registration", 158.00),
    # DEPARTURES
    "Departure Management – EU (IMI)":               ("Departure Management – EU IMI\nAIMA + NIF + SS + Health Centre cancellation", 420.00),
    "Departure Management – EU + Relo":              ("Departure Management – EU + Relocation\nExtra: lease termination · check-out · deposit recovery · utilities · bank cancellation", 788.00),
    "Departure Management – Non-EU":                 ("Departure Management – Non-EU IMI + Relo\nExtra: lease termination · check-out · deposit recovery · utilities · bank cancellation", 1575.00),
    # SINGLE SERVICES
    "Apostille":                                     ("Apostille", 210.00),
    "Parish Certificate":                            ("Parish Certificate", 158.00),
    # CUSTOM
    "Custom / Type manually":                        ("", 0.0),
}

# ── Default intro paragraphs ──────────────────────────────────────────
DEFAULT_P1 = "Our sincere thanks for choosing RELOCARING to assist you with your relocation and immigration journey to Portugal. We are pleased to present this personalised proposal outlining our recommended services and fees."
DEFAULT_P2 = "With deep expertise in Professional Mobility and Immigration Services, RELOCARING strives to achieve excellence and deliver integrated, end-to-end solutions — offering peace of mind and a single, trusted point of contact throughout your entire process."
DEFAULT_P3 = "Our team works alongside qualified lawyers and solicitors to ensure that every aspect of your residency, legal and administrative requirements is handled professionally and with the care your move deserves."

DEFAULT_CARDS = {
    "VISA & IMMIGRATION":  "Full management of your visa application, documentation review, AIMA appointments and residence permit.",
    "NATIONALITY PROCESS": "End-to-end nationality application managed by a qualified lawyer/solicitor, from checklist to IRN submission.",
    "HOME SEARCH":         "Personalised property search with accompanied viewings and lease negotiation support.",
    "SCHOOL SEARCH":       "Identification and enrolment support for international and Portuguese schools.",
    "ORIENTATION TOUR":    "Guided half or full-day tour of the Lisbon area — neighbourhoods, services and lifestyle.",
    "TAX & LEGAL ADVICE":  "NIF, NISS, bank account, health centre registration and fiscal representation services.",
}

# ── PDF generator ─────────────────────────────────────────────────────
def generate_pdf(client_name, service_description, proposal_date,
                 proposal_number, services, intro_paragraphs, cards_overview):

    W, H = A4
    buffer = io.BytesIO()

    def _draw_logo(c, path, x, y, w):
        try:
            img = PILImage.open(path)
            h = w * img.height / img.width
            c.drawImage(path, x, y, width=w, height=h, preserveAspectRatio=True, mask='auto')
        except: pass

    def _footer(c, page_num=None):
        c.setStrokeColor(TEAL_MID); c.setLineWidth(0.5)
        c.line(1.8*cm, 1.9*cm, W-1.8*cm, 1.9*cm)
        _draw_logo(c, LOGO_SMALL, 1.8*cm, 0.45*cm, 68)
        c.setFont('Helvetica', 7); c.setFillColor(TEAL_MID)
        c.drawRightString(W-1.8*cm, 1.3*cm, f'{COMPANY_EMAIL}  ·  {COMPANY_PHONE}  ·  {COMPANY_WEB}')
        if page_num:
            c.setFont('Helvetica-Bold', 8); c.setFillColor(TEAL)
            c.drawRightString(W-1.8*cm, 0.55*cm, str(page_num))

    def bg_cover(c, doc):
        c.saveState()
        c.setFillColor(WHITE);      c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(TEAL);       c.rect(0,0,0.85*cm,H,fill=1,stroke=0)
        c.setFillColor(RED);        c.rect(0,H*0.75,0.85*cm,H*0.25,fill=1,stroke=0)
        c.setFillColor(colors.HexColor('#F3F7F9'))
        c.rect(0.85*cm,H*0.38,W-0.85*cm,H*0.24,fill=1,stroke=0)
        c.setFillColor(TEAL_DARK);  c.rect(0.85*cm,0,W-0.85*cm,H*0.13,fill=1,stroke=0)
        c.setFillColor(RED);        c.rect(0.85*cm,H*0.13,W-0.85*cm,0.28*cm,fill=1,stroke=0)
        _draw_logo(c, LOGO, W-185-1.8*cm, H-60-2.0*cm, 185)
        c.setFont('Helvetica-Bold',50); c.setFillColor(TEAL_DARK)
        c.drawString(1.8*cm, H*0.53, 'FEE PROPOSAL')
        c.setFillColor(RED); c.rect(1.8*cm,H*0.38+6,6.5*cm,3,fill=1,stroke=0)
        c.setFont('Helvetica',9.5); c.setFillColor(TEAL_MID)
        c.drawString(1.8*cm, H*0.38-10, 'Relocation & Immigration Services — Portugal')
        c.setFont('Helvetica-Bold',7); c.setFillColor(RED)
        c.drawString(1.8*cm, H*0.295, 'ADDRESSED TO')
        c.setFont('Helvetica-Bold',20); c.setFillColor(TEAL_DARK)
        c.drawString(1.8*cm, H*0.295-28, client_name.upper())
        c.setFont('Helvetica',10); c.setFillColor(GREY_TEXT)
        c.drawString(1.8*cm, H*0.295-47, service_description)
        c.setFont('Helvetica',8.5); c.setFillColor(TEAL_MID)
        c.drawString(1.8*cm, H*0.295-65, proposal_date)
        if proposal_number:
            c.setFont('Helvetica',7.5); c.setFillColor(TEAL_MID)
            c.drawString(1.8*cm, H*0.295-82, f'Ref: {proposal_number}')
        c.setFont('Helvetica-Bold',8.5); c.setFillColor(WHITE)
        c.drawString(2.2*cm, H*0.085, COMPANY_EMAIL)
        c.setFont('Helvetica',8)
        c.drawString(2.2*cm, H*0.085-14, f'{COMPANY_PHONE}  ·  {COMPANY_WEB}')
        c.setFont('Helvetica',7.5); c.setFillColor(colors.HexColor('#A8CBE0'))
        c.drawString(2.2*cm, H*0.085-27, COMPANY_ADDRESS)
        c.restoreState()

    def bg_inner(c, doc, page_num=None):
        c.saveState()
        c.setFillColor(WHITE);      c.rect(0,0,W,H,fill=1,stroke=0)
        c.setFillColor(TEAL);       c.rect(0,0,0.55*cm,H,fill=1,stroke=0)
        c.setFillColor(RED);        c.rect(0,H-2.5*cm,0.55*cm,2.5*cm,fill=1,stroke=0)
        c.setFillColor(TEAL_LIGHT); c.rect(0.55*cm,H-1.0*cm,W-0.55*cm,1.0*cm,fill=1,stroke=0)
        c.setFillColor(RED);        c.rect(W-1.0*cm,H-1.0*cm,1.0*cm,1.0*cm,fill=1,stroke=0)
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
    doc = ReloDoc(buffer, pagesize=A4, leftMargin=2.2*cm, rightMargin=1.8*cm,
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

    # Page 2
    story.append(Paragraph("INTRODUCTION", S_LABEL))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(f"Dear {client_name},",
        ps('sal', fontName='Helvetica-Bold', fontSize=11, textColor=TEAL_DARK, spaceAfter=14)))
    for para_text in intro_paragraphs:
        if para_text.strip():
            story.append(Paragraph(para_text.replace("RELOCARING", "<b>RELOCARING</b>"), S_BODY))
    story.append(Spacer(1, 0.5*cm))

    card_w = (W - 4.0*cm - 0.5*cm) / 2
    items = list(cards_overview.items())
    for i in range(0, len(items), 2):
        def card(title, desc):
            t = Table([[Paragraph(title, ps('ct', fontName='Helvetica-Bold', fontSize=8.5, textColor=TEAL_DARK))],
                       [Paragraph(desc, ps('cd', fontName='Helvetica', fontSize=8, textColor=GREY_TEXT, leading=13))]],
                      colWidths=[card_w])
            t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),TEAL_LIGHT),('LINEABOVE',(0,0),(-1,0),2.5,TEAL),
                                   ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
                                   ('TOPPADDING',(0,0),(0,0),8),('TOPPADDING',(0,1),(-1,-1),4),
                                   ('BOTTOMPADDING',(0,-1),(-1,-1),10)]))
            return t
        lt, ld = items[i]
        if i+1 < len(items):
            rt, rd = items[i+1]
            g = Table([[card(lt,ld), card(rt,rd)]], colWidths=[card_w,card_w], spaceBefore=6, hAlign='LEFT')
            g.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),
                                   ('RIGHTPADDING',(0,0),(0,-1),6),('RIGHTPADDING',(1,0),(1,-1),0)]))
        else:
            g = Table([[card(lt,ld), Spacer(card_w,1)]], colWidths=[card_w,card_w], spaceBefore=6)
            g.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0)]))
        story.append(g)
        story.append(Spacer(1, 0.25*cm))

    story.append(NextPageTemplate('fees'))
    story.append(PageBreak())

    # Page 3
    story.append(Paragraph("SERVICES & FEES", S_LABEL))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Fee Proposal", S_SECTION))
    story.append(Paragraph("The fees outlined below are based on RELOCARING's understanding of your requirements at this stage. All fees are indicative and may be revised following review of further documentation. VAT, public costs, government fees, translations and certified copies are not included unless otherwise stated.", S_BODY))
    story.append(Spacer(1, 0.2*cm))

    col_w = [8.5*cm, 1.4*cm, 2.7*cm, 2.0*cm, 2.4*cm]
    def th(t): return Paragraph(f'<b>{t}</b>', ps('th', fontName='Helvetica-Bold', fontSize=8.5, textColor=WHITE, alignment=TA_CENTER))
    def td_l(t): return Paragraph(t, ps('tdl', fontName='Helvetica', fontSize=8.5, textColor=GREY_TEXT))
    def td_c(t): return Paragraph(t, ps('tdc', fontName='Helvetica', fontSize=8.5, textColor=GREY_TEXT, alignment=TA_CENTER))
    def td_r(t, bold=False, col=None): return Paragraph(t, ps('tdr', fontName='Helvetica-Bold' if bold else 'Helvetica', fontSize=8.5, textColor=col or GREY_TEXT, alignment=TA_RIGHT))

    fee_rows = [[th('SERVICES'), th('QTY'), th('UNIT PRICE'), th('DISC.'), th('TOTAL')]]
    grand_total = 0.0
    for idx, (name, qty, unit, disc) in enumerate(services):
        total = qty * unit * (1 - disc)
        grand_total += total
        disc_str = f"{disc*100:.0f}%" if disc > 0 else "—"
        fee_rows.append([td_l(name), td_c(str(qty)),
                         td_r(f"{unit:,.2f} €".replace(',','.')),
                         td_c(disc_str),
                         td_r(f"{total:,.2f} €".replace(',','.'))])
    fee_rows.append([Paragraph('',ps('x')),Paragraph('',ps('x')),Paragraph('',ps('x')),
                     td_r('<b>TOTAL</b>', bold=True, col=TEAL_DARK),
                     td_r(f'<b>{grand_total:,.2f} €</b>'.replace(',','.'), bold=True, col=TEAL_DARK)])
    row_bgs = [('BACKGROUND',(0,i),(-1,i),TEAL_LIGHT if i%2==0 else WHITE) for i in range(1,len(fee_rows)-1)]
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
                   Paragraph("50% upon acceptance of this proposal  +  50% upon submission of the process",
                             ps('pcb', fontName='Helvetica', fontSize=8.5, textColor=GREY_TEXT))]],
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

    # Page 4
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
    story.append(Table([[Paragraph(
        f"I, <b>{client_name}</b>, give my informed consent to the gathering, storage and processing of mine and my family's personal data by Relocaring Lda., their Partners and relevant Public entities, for the purposes described above.",
        ps('cb', fontName='Helvetica', fontSize=9, textColor=TEAL_DARK, leading=15, alignment=TA_JUSTIFY))]],
        colWidths=[W-4.0*cm],
        style=[('BACKGROUND',(0,0),(-1,-1),TEAL_LIGHT),('LINEABOVE',(0,0),(-1,-1),2.5,TEAL),
               ('LINEBEFORE',(0,0),(0,-1),2.5,RED),('TOPPADDING',(0,0),(-1,-1),12),
               ('BOTTOMPADDING',(0,0),(-1,-1),12),('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14)]))
    story.append(Spacer(1, 0.8*cm))
    story.append(Table([[Paragraph('Signed', ps('sl', fontName='Helvetica', fontSize=8, textColor=TEAL_MID, tracking=1)),
                         Paragraph('Date',   ps('sl2', fontName='Helvetica', fontSize=8, textColor=TEAL_MID, tracking=1))],
                        [Paragraph('_'*40, ps('sl3', fontName='Helvetica', fontSize=9, textColor=GREY_RULE)),
                         Paragraph('_'*24, ps('sl4', fontName='Helvetica', fontSize=9, textColor=GREY_RULE))]],
                       colWidths=[(W-4.0*cm)*0.62,(W-4.0*cm)*0.38],
                       style=[('VALIGN',(0,0),(-1,-1),'BOTTOM'),('LEFTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),4)]))

    story.append(NextPageTemplate('tc'))
    story.append(PageBreak())

    # Page 5
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
                       colWidths=[(W-4.0*cm)*0.45,(W-4.0*cm)*0.55],
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

st.image("logo_relocaring.png", width=220)
st.markdown("---")
st.title("Fee Proposal Generator")
st.caption("Fill in the fields below and click **Generate PDF** to download the proposal.")

# ── SECTION 1: Client Info ────────────────────────────────────────────
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
col3, _ = st.columns(2)
with col3:
    proposal_date = st.date_input("Proposal Date", value=datetime.date.today())
    try:
        proposal_date_str = proposal_date.strftime("%-d %B, %Y")
    except:
        proposal_date_str = proposal_date.strftime("%d %B, %Y").lstrip("0")

st.markdown("---")

# ── SECTION 2: Introduction paragraphs ───────────────────────────────
st.markdown("### ✍️ Introduction Text")
st.caption("Toggle each paragraph on/off and edit the text directly if needed.")

intro_paragraphs = []

with st.expander("📝 Paragraph 1 — Thanks & purpose", expanded=True):
    show_p1 = st.checkbox("Include", value=True, key="show_p1")
    p1 = st.text_area("", value=DEFAULT_P1, height=90, key="p1", disabled=not show_p1)
    if show_p1: intro_paragraphs.append(p1)

with st.expander("📝 Paragraph 2 — Expertise & solutions", expanded=True):
    show_p2 = st.checkbox("Include", value=True, key="show_p2")
    p2 = st.text_area("", value=DEFAULT_P2, height=90, key="p2", disabled=not show_p2)
    if show_p2: intro_paragraphs.append(p2)

with st.expander("📝 Paragraph 3 — Lawyers & care", expanded=True):
    show_p3 = st.checkbox("Include", value=True, key="show_p3")
    p3 = st.text_area("", value=DEFAULT_P3, height=90, key="p3", disabled=not show_p3)
    if show_p3: intro_paragraphs.append(p3)

with st.expander("📝 Custom paragraph (optional)", expanded=False):
    show_custom = st.checkbox("Include a custom paragraph", value=False, key="show_custom")
    custom_p = st.text_area("", placeholder="Add a personalised note for this client...",
                            height=90, key="custom_para", disabled=not show_custom)
    if show_custom and custom_p.strip(): intro_paragraphs.append(custom_p)

st.markdown("---")

# ── SECTION 3: Service overview cards ────────────────────────────────
st.markdown("### 🗂️ Service Overview Cards")
st.caption("Choose which service cards appear on the introduction page. Edit descriptions if needed.")

selected_cards = {}
card_cols = st.columns(2)
for idx, (title, desc) in enumerate(DEFAULT_CARDS.items()):
    with card_cols[idx % 2]:
        with st.expander(f"🔷 {title}", expanded=False):
            include = st.checkbox("Include this card", value=True, key=f"card_{idx}")
            edited = st.text_area("Description", value=desc, height=70,
                                  key=f"card_desc_{idx}", disabled=not include)
            if include:
                selected_cards[title] = edited

st.markdown("---")

# ── SECTION 4: Services & Pricing ────────────────────────────────────
st.markdown("### 💶 Services & Pricing")
st.caption("Select a service — the 2026 price loads automatically. You can override the price if needed.")

service_labels = list(SERVICE_CATALOGUE.keys())
services = []

for i in range(1, 9):
    with st.expander(f"Service {i}", expanded=(i <= 2)):
        c1, c2, c3, c4 = st.columns([3, 1.5, 0.8, 1.8])

        with c1:
            selected = st.selectbox("Service", options=service_labels,
                                    key=f"sel_{i}", label_visibility="collapsed")

        pdf_desc, default_price = SERVICE_CATALOGUE[selected]

        with c2:
            price = st.number_input("Price €", min_value=0.0,
                                    value=float(default_price),
                                    step=10.0, format="%.2f",
                                    key=f"price_{i}", label_visibility="collapsed")
            is_auto = (price == default_price and default_price > 0)
            st.caption("🟢 Auto price" if is_auto else "✏️ Custom price")

        with c3:
            qty = st.number_input("Qty", min_value=1, value=1, step=1,
                                  key=f"qty_{i}", label_visibility="collapsed")
            st.caption("Qty")

        with c4:
            disc_presets = {
                "No discount": 0.0, "5%": 0.05, "10%": 0.10,
                "15%": 0.15, "20%": 0.20, "25%": 0.25,
                "30%": 0.30, "40%": 0.40, "50%": 0.50,
                "Custom %": -1,
            }
            disc_label = st.selectbox("Discount", options=list(disc_presets.keys()),
                                      key=f"disc_{i}", label_visibility="collapsed")
            if disc_label == "Custom %":
                custom_pct = st.number_input("Enter %", min_value=0.0, max_value=100.0,
                                             value=0.0, step=0.5, key=f"custom_disc_{i}")
                disc = custom_pct / 100
            else:
                disc = disc_presets[disc_label]
            st.caption("Discount")

        # Description override
        if selected == "Custom / Type manually":
            pdf_desc = st.text_area("Service description for PDF *",
                                    placeholder="Service name and description...",
                                    height=70, key=f"custom_desc_{i}")
        elif selected != "— Select a service —" and pdf_desc:
            if st.checkbox("Edit description for PDF", key=f"edit_{i}"):
                pdf_desc = st.text_area("", value=pdf_desc, height=70,
                                        key=f"desc_edit_{i}")

        # Line total preview
        if selected != "— Select a service —" and pdf_desc and price > 0:
            line_total = qty * price * (1 - disc)
            disc_str = f"  (−{disc*100:.0f}%)" if disc > 0 else ""
            st.info(f"**Line total: €{line_total:,.2f}**{disc_str}")
            services.append((pdf_desc, qty, price, disc))

st.markdown("---")

# ── Quote summary ─────────────────────────────────────────────────────
if services:
    st.markdown("### 🧮 Quote Summary")
    grand = 0.0
    for name, qty, price, disc in services:
        line = qty * price * (1 - disc)
        grand += line
        d_str = f" (−{disc*100:.0f}%)" if disc > 0 else ""
        st.markdown(f"- {name.split(chr(10))[0]}  ×{qty}  =  **€{line:,.2f}**{d_str}")
    st.success(f"### 💰 Total: €{grand:,.2f}")
    st.markdown("---")

# ── Generate ──────────────────────────────────────────────────────────
st.markdown("### 📄 Generate Proposal")

if st.button("⬇️ Generate & Download PDF", type="primary", use_container_width=True):
    errors = []
    if not client_name:           errors.append("Client name is required.")
    if not service_description:   errors.append("Service description for cover is required.")
    if not services:              errors.append("Add at least one service.")
    if not intro_paragraphs:      errors.append("Include at least one introduction paragraph.")

    if errors:
        for e in errors: st.error(e)
    else:
        with st.spinner("Generating proposal..."):
            try:
                pdf_buffer, grand_total = generate_pdf(
                    client_name, service_description, proposal_date_str,
                    proposal_number, services, intro_paragraphs, selected_cards
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
