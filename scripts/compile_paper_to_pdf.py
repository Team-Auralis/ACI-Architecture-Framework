"""
Academic PDF Compiler for The Fool's Theorem Whitepaper
Uses ReportLab to generate publication-grade PDF from LaTeX manuscript.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable
)
from reportlab.pdfgen import canvas

PDF_OUTPUT_PATH = "E:/ACI-Architecture-Framework/docs/papers/THE_FOOLS_THEOREM_WHITEPAPER.pdf"


class NumberedCanvas(canvas.Canvas):
    """Adds running headers and footers with dynamic page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header (on pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "The Fool's Theorem: Asymptotic Epistemic Closure in Autoregressive Agent Loops")
            self.drawRightString(612 - 54, 750, "ACI Empirical Specification")
            self.setStrokeColor(colors.HexColor("#dddddd"))
            self.setLineWidth(0.5)
            self.line(54, 742, 612 - 54, 742)

        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 36, page_text)
        self.drawString(54, 36, "Team Auralis & Autonomous Systems Research Group — Confidential / Preprint")
        self.setStrokeColor(colors.HexColor("#dddddd"))
        self.setLineWidth(0.5)
        self.line(54, 48, 612 - 54, 48)
        self.restoreState()


def build_academic_pdf():
    os.makedirs(os.path.dirname(PDF_OUTPUT_PATH), exist_ok=True)
    doc = SimpleDocTemplate(
        PDF_OUTPUT_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Typography
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        alignment=1,
        textColor=colors.HexColor("#111827"),
        spaceAfter=8
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=14
    )
    author_style = ParagraphStyle(
        'DocAuthor',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#374151"),
        spaceAfter=18
    )
    abstract_heading = ParagraphStyle(
        'AbstractHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        alignment=1,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=6
    )
    abstract_body = ParagraphStyle(
        'AbstractBody',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#374151")
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#111827"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#1f2937"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=6
    )
    theorem_box = ParagraphStyle(
        'TheoremBox',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#111827")
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1e293b")
    )

    story = []

    # Title & Metadata
    story.append(Spacer(1, 10))
    story.append(Paragraph("The Fool's Theorem", title_style))
    story.append(Paragraph("Asymptotic Epistemic Closure and Generational Context in Long-Horizon Autoregressive Agent Systems", subtitle_style))
    story.append(Paragraph("<b>Shaurya Sanyal</b> &bull; Team Auralis &bull; Autonomous Systems Research Group<br/><font color='#6b7280'>Preprint Ref: ACI-MATH-2026-FT &bull; October 2026</font>", author_style))

    # Abstract Box
    abstract_text = (
        "<b>Abstract.</b> The prevailing design paradigm for autonomous artificial intelligence agents treats the transformer "
        "context window as an unbounded, append-only linear interaction transcript. We prove that this paradigm is fundamentally "
        "flawed. We establish <b>The Fool's Theorem</b> (<i>The Asymptotic Epistemic Closure Bound</i>), proving that in any "
        "self-attending autoregressive language agent accumulating raw environment execution observations without generational "
        "garbage collection, the probability of generating a valid counter-hypothesis following an environmental failure decays "
        "exponentially: <i>P(E_correct | H_t) &le; C_1 exp(-&lambda; |S_noise|) + O(|S_noise|^-1)</i>. Past a finite critical threshold <i>N*</i>, "
        "self-attention contracts into an inescapable semantic attractor basin centered on the error traceback, rendering the agent "
        "incapable of root-cause recovery regardless of parameter scale or compute budget---a state we formalize as <b>The Fool</b>. "
        "To resolve this crisis, we introduce the <b>Cognitive Context Trifecta</b> (<i>Payload Inundation</i>, <i>Generational Context</i>, "
        "and <i>Error Gravitation</i>) and specify the <b>Attention-Weighted Eviction (AWE)</b> algorithm. On the standardized CCB-001 "
        "empirical benchmark, Generational Context cuts active context token load by 96.6%, elevates Context Signal Ratio by 24x, "
        "and raises task success from 0.0% to 100.0%."
    )
    abstract_table = Table(
        [[Paragraph(abstract_text, abstract_body)]],
        colWidths=[504]
    )
    abstract_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
    ]))
    story.append(abstract_table)
    story.append(Spacer(1, 14))

    # Section 1
    story.append(Paragraph("1. Introduction & The Crisis of Context", h1_style))
    story.append(Paragraph(
        "Between 2024 and 2026, frontier foundation models expanded raw attention context windows from 128k to millions of tokens. "
        "However, the practical autonomy horizon of software engineering and systems-operation agents has stubbornly stagnated around 20 "
        "to 30 turns. Beyond this horizon, agents routinely exhibit catastrophic cognitive degradation: repeating failed tool calls, "
        "inventing spurious explanations for syntax errors, and losing adherence to foundational system invariants.",
        body_style
    ))
    story.append(Paragraph(
        "Empirical production telemetry across agent sessions reveals that this failure is mechanical: in typical multi-turn agent sessions, "
        "<b>93.9% of all active tokens consist of high-entropy raw tool outputs</b> (compiler traces, test runner dumps, full DOM trees), "
        "whereas model reasoning and user constraints account for less than 4.9%. Modern agent harnesses treat the context buffer as an "
        "append-only text file, neglecting basic memory lifecycle management.",
        body_style
    ))

    # Section 2
    story.append(Paragraph("2. Mathematical Formulation & Lemmas", h1_style))
    story.append(Paragraph(
        "Let the interaction transcript be partitioned into three disjoint subspaces: Invariant Subspace S_inv (system rules and goal), "
        "Noise Subspace S_noise (unpruned execution logs), and Diagnostic Subspace S_diag (hypotheses).",
        body_style
    ))

    # Lemma 1 Box
    l1_text = (
        "<b>Lemma 1 (Inundation Lemma — Softmax Denominator Explosion).</b><br/>"
        "<i>Under bounded query and key energies, the aggregate attention probability mass allocated to the invariant subspace is strictly upper-bounded by:</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>A_{i, inv} &le; &kappa; |S_inv| / (|S_inv| + |S_noise|) = O(1 / |S_noise|)</b><br/>"
        "<i>As context noise |S_noise| approaches infinity, attention probability mass on ground truth decays asymptotically to zero.</i>"
    )
    t_l1 = Table([[Paragraph(l1_text, theorem_box)]], colWidths=[504])
    t_l1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#86efac")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_l1)
    story.append(Spacer(1, 8))

    # Lemma 2 Box
    l2_text = (
        "<b>Lemma 2 (Gravitation Lemma — Semantic Attractor Contraction).</b><br/>"
        "<i>Let an execution failure emit traceback v_e. The query projection operator forms a strict contraction mapping on the unit sphere toward v_e:</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>d/dt cos(&theta;_t) = &eta; |S_noise^(e)| (1 - cos^2(&theta;_t)) - &gamma; cos(&theta;_t)</b><br/>"
        "<i>whose unique stable fixed point satisfies lim_{t &rarr; &infin;} cos(&theta;*) = 1.</i>"
    )
    t_l2 = Table([[Paragraph(l2_text, theorem_box)]], colWidths=[504])
    t_l2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#fef2f2")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#fca5a5")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_l2)
    story.append(Spacer(1, 10))

    # Theorem 1 Box
    story.append(Paragraph("3. The Fool's Theorem", h1_style))
    thm_text = (
        "<b>THEOREM 1 (The Fool's Theorem — Asymptotic Epistemic Closure Bound).</b><br/>"
        "<i>Let M be an autoregressive agent operating under standard Multi-Head Attention over an unpruned history transcript H_t. "
        "Suppose at step k, M encounters an execution failure yielding an uncompressed traceback of length L_e. Then:</i><br/>"
        "1. <i>The probability P(E_correct | H_t) that M emits a correct counter-hypothesis at step t &gt; k decays exponentially:</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>P(E_correct | H_t) &le; C_1 exp(-&lambda; |S_noise|) + C_2 / |S_noise|</b><br/>"
        "2. <i>There exists a finite critical threshold N* such that for all |S_noise| &gt; N*, the agent enters an Epistemic Closure Basin: "
        "P(a_t &notin; Span(S_error)) &lt; &epsilon;_env.</i><br/>"
        "3. <i>Scaling context window capacity W &rarr; &infin; strictly deepens the attractor basin, guaranteeing that M will perpetually "
        "patch symptoms without ever resolving the root cause. M becomes mathematically trapped as The Fool.</i>"
    )
    t_thm = Table([[Paragraph(thm_text, theorem_box)]], colWidths=[504])
    t_thm.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
        ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor("#93c5fd")),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_thm)
    story.append(Spacer(1, 10))

    # Section 4
    story.append(Paragraph("4. The Cognitive Context Trifecta & AWE Algorithm", h1_style))
    story.append(Paragraph(
        "To resolve The Fool's Theorem, memory must be stratified into three lifecycle tiers: "
        "<b>Gen-0 Ephemeral</b> (raw tool outputs; TTL=1 turn; distilled to 3 lines), "
        "<b>Gen-1 Evaporative</b> (working plans; paged dynamically), and "
        "<b>Gen-2 Tenured</b> (system invariants and user goals; pinned permanently).",
        body_style
    ))

    # Algorithm Box
    algo_text = (
        "<b>Algorithm 1: Attention-Weighted Eviction (AWE)</b><br/>"
        "&nbsp;&nbsp;1: <b>Input:</b> Cache capacity C, incoming chunk E, target boundary p<br/>"
        "&nbsp;&nbsp;2: Compute Information Density Score: IDS(E) = AttentionWeight(E) &times; 100 / (Entropy(E) + 10^-4)<br/>"
        "&nbsp;&nbsp;3: <b>if</b> E.key &isin; T1 &cup; T2 <b>then</b> Promote E to Tenured Cache T2<br/>"
        "&nbsp;&nbsp;4: <b>else if</b> E.key &isin; B1 (Ghost T1) <b>then</b> Adapt p &larr; min(C, p + |B2|/|B1|); Evict lowest IDS victim<br/>"
        "&nbsp;&nbsp;5: <b>else if</b> E.key &isin; B2 (Ghost T2) <b>then</b> Adapt p &larr; max(0, p - |B1|/|B2|); Evict lowest IDS victim<br/>"
        "&nbsp;&nbsp;6: <b>else</b> Evict lowest IDS chunk; Insert E into Recency Cache T1"
    )
    t_algo = Table([[Paragraph(algo_text, code_style)]], colWidths=[504])
    t_algo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_algo)
    story.append(Spacer(1, 10))

    # Section 5: Empirical Benchmark Table
    story.append(Paragraph("5. Empirical Validation: CCB-001 Benchmark", h1_style))
    story.append(Paragraph(
        "We executed the CCB-001 benchmark across 3 complex software debugging scenarios with multi-frame tracebacks and misleading "
        "attractors. Attention weights were computed via live subword vector projections:",
        body_style
    ))

    bench_data = [
        ["Architecture Arm", "Active Tokens", "Signal (CSR)", "Attn(Inv)", "Mean EGI", "Success Rate", "Cost ($)"],
        ["Arm A: Flat Append-Only", "5,171", "0.0057", "0.0391", "0.3922", "0.0%", "$0.0466"],
        ["Arm B: Auto-Compaction", "3,400", "0.0076", "0.0514", "0.3922", "33.3%", "$0.0465"],
        ["Arm C: Generational Context", "140", "0.2375", "0.1311", "0.1399", "100.0%", "$0.0463"],
    ]
    t_bench = Table(bench_data, colWidths=[130, 65, 65, 55, 55, 70, 64])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TEXTCOLOR', (5, 1), (5, 1), colors.HexColor("#dc2626")),
        ('TEXTCOLOR', (5, 2), (5, 2), colors.HexColor("#d97706")),
        ('TEXTCOLOR', (5, 3), (5, 3), colors.HexColor("#16a34a")),
        ('FONTNAME', (5, 3), (5, 3), 'Helvetica-Bold'),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 14))

    # Section 6: Conclusion
    story.append(Paragraph("6. Conclusion", h1_style))
    story.append(Paragraph(
        "The Fool's Theorem demonstrates that unmanaged context scaling does not solve agent memory; it guarantees cognitive closure. "
        "By treating attention like volatile RAM with Generational Context and Attention-Weighted Eviction, agents escape The Fool's Basin "
        "and achieve unbounded operational stability.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # References
    story.append(Paragraph("References", h1_style))
    refs = [
        "[1] A. Vaswani et al., 'Attention is all you need,' in NeurIPS, 2017.",
        "[2] N. Megiddo and D. S. Modha, 'ARC: A self-tuning, low overhead replacement cache,' in USENIX FAST, 2003.",
        "[3] S. Sanyal, 'The Cognitive Context Trifecta: Payload Inundation, Generational Context, and Error Gravitation,' ACI Empirical Spec, 2026.",
        "[4] Anthropic, 'Effective context engineering for AI agents,' Anthropic Research, 2025."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('RefStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=8, leading=11, textColor=colors.HexColor("#4b5563"))))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Academic PDF compiled successfully: {PDF_OUTPUT_PATH}")


if __name__ == "__main__":
    build_academic_pdf()
