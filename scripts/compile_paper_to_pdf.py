"""
Academic PDF Compiler for The Softmax Inundation Bound & Generational Context Whitepaper
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
            self.drawString(54, 750, "Softmax Inundation and Generational Context in Long-Horizon Agent Systems")
            self.drawRightString(612 - 54, 750, "ACI Research Preprint")
            self.setStrokeColor(colors.HexColor("#dddddd"))
            self.setLineWidth(0.5)
            self.line(54, 742, 612 - 54, 742)

        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 36, page_text)
        self.drawString(54, 36, "Team Auralis & Autonomous Systems Research Group — Preprint Ref: ACI-MATH-2026-FT-REV2")
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
        fontSize=18,
        leading=22,
        alignment=1,
        textColor=colors.HexColor("#111827"),
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=12
    )
    author_style = ParagraphStyle(
        'DocAuthor',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#374151"),
        spaceAfter=14
    )
    abstract_body = ParagraphStyle(
        'AbstractBody',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#374151")
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#111827"),
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#1f2937"),
        spaceAfter=5
    )
    theorem_box = ParagraphStyle(
        'TheoremBox',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#111827")
    )
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#1e293b")
    )

    story = []

    # Title & Metadata
    story.append(Spacer(1, 6))
    story.append(Paragraph("Softmax Inundation and Generational Context in Long-Horizon Agent Systems", title_style))
    story.append(Paragraph("Analytical Attention Dilution Bounds and the Generational Memory Architecture", subtitle_style))
    story.append(Paragraph("<b>Shaurya Sanyal</b> &bull; Team Auralis &bull; Autonomous Systems Research Group<br/><font color='#6b7280'>Preprint Ref: ACI-MATH-2026-FT-REV2 &bull; October 2026</font>", author_style))

    # Abstract Box
    abstract_text = (
        "<b>Abstract.</b> Autonomous AI agent architectures routinely treat the transformer context window as an unbounded, "
        "append-only linear interaction transcript. We analyze the theoretical and empirical consequences of this paradigm. "
        "We formalize the <b>Softmax Inundation Bound</b>, an analytical upper bound showing that under bounded projection energy, "
        "the maximum aggregate self-attention probability mass allocated to a fixed set of invariant constraint tokens decays "
        "asymptotically as <i>O(L_u / |S_noise|)</i> when unpruned execution observations accumulate. This attention dilution creates "
        "a systemic vulnerability: as noisy tracebacks dominate context length, attention heads dilute focus from foundational system "
        "invariants toward high-entropy symptom tokens. To resolve this failure mode, we specify <b>Generational Context</b>, an "
        "operating-system-inspired memory architecture that separates memory into <b>Gen-0 Ephemeral</b> (tool outputs distilled to 3-line "
        "signatures and evicted in 1 turn), <b>Gen-1 Evaporative</b> (working memory paged via the Attention-Weighted Eviction algorithm), "
        "and <b>Gen-2 Tenured</b> (permanently pinned invariants). We prove that Generational Context maintains a non-zero lower bound "
        "on invariant attention uniformly for all interaction turns <i>t &isin; N</i>, eliminating unbounded softmax dilution and stabilizing "
        "long-horizon autonomy."
    )
    abstract_table = Table([[Paragraph(abstract_text, abstract_body)]], colWidths=[504])
    abstract_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(abstract_table)
    story.append(Spacer(1, 10))

    # Section 1
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph(
        "Despite expansions in foundation model context windows, practical autonomy in multi-turn software engineering loops "
        "remains fragile. Agents frequently lose adherence to system constraints, repeat failed tool invocations, and apply "
        "superficial micro-patches around symptoms rather than addressing root causes.",
        body_style
    ))
    story.append(Paragraph(
        "In typical agent sessions, over 90% of active tokens consist of raw tool outputs (compiler stderr, test dumps, DOM trees). "
        "We analyze this pathology via <b>Payload Inundation</b> (attention dilution), <b>Error Gravitation</b> (semantic bias toward "
        "error tracebacks), and <b>Generational Context</b> (multi-tiered memory management).",
        body_style
    ))

    # Section 2: Mathematical Formulation
    story.append(Paragraph("2. The Softmax Inundation Bound", h1_style))
    story.append(Paragraph(
        "Let context tokens be partitioned into Invariant Subspace S_inv (|S_inv| = L_u) and Observation Subspace S_noise. "
        "Under bounded query and key energies ||q_i||_2 &le; M_Q and ||k_j||_2 &le; M_K, let &kappa; = exp(2 M_Q M_K / sqrt(d_k)).",
        body_style
    ))

    # Theorem 1 Box
    thm1_text = (
        "<b>Theorem 1 (Softmax Inundation Upper Bound).</b><br/>"
        "<i>For any query position i, the aggregate attention probability mass allocated to the invariant subspace S_inv is upper-bounded by:</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>A_{i, inv} &le; &kappa; L_u / (L_u + |S_noise|) = O(L_u / |S_noise|)</b><br/>"
        "<i>Proof Sketch:</i> By Cauchy-Schwarz, -M_Q M_K &le; q_i^T k_j &le; M_Q M_K. The numerator is bounded above by "
        "L_u exp(M_Q M_K / sqrt(d_k)) and the denominator is bounded below by (L_u + |S_noise|) exp(-M_Q M_K / sqrt(d_k)). "
        "Dividing numerator by denominator yields the result directly."
    )
    t_thm1 = Table([[Paragraph(thm1_text, theorem_box)]], colWidths=[504])
    t_thm1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#86efac")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_thm1)
    story.append(Spacer(1, 8))

    # Section 3: Generational Context
    story.append(Paragraph("3. Generational Context & Retention Guarantee", h1_style))
    story.append(Paragraph(
        "Generational Context stratifies memory into three lifecycle tiers: "
        "<b>Gen-0 Ephemeral</b> (tool outputs distilled to 3 lines and purged in 1 turn), "
        "<b>Gen-1 Evaporative</b> (working memory paged via AWE), and "
        "<b>Gen-2 Tenured</b> (permanently pinned invariants).",
        body_style
    ))

    # Theorem 2 Box
    thm2_text = (
        "<b>Theorem 2 (Generational Retention Guarantee).</b><br/>"
        "<i>Under Generational Context with bounded distillation ||&sigma;_distill(G_0)|| &le; K_0 and working capacity ||G_1|| &le; C_1, "
        "the active non-invariant tokens satisfy |S_non-inv^(t)| &le; C_1 + K_0 = C_bound for all turns t. The invariant attention is strictly lower-bounded:</i><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>A_{i, inv} &ge; L_u / (L_u + &kappa; C_bound) &gt; 0</b><br/>"
        "<i>Invariant attention remains strictly bounded away from zero uniformly for all interaction turns t &isin; N.</i>"
    )
    t_thm2 = Table([[Paragraph(thm2_text, theorem_box)]], colWidths=[504])
    t_thm2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#93c5fd")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_thm2)
    story.append(Spacer(1, 8))

    # Section 4: AWE Algorithm
    story.append(Paragraph("4. The Attention-Weighted Eviction (AWE) Algorithm", h1_style))
    algo_text = (
        "<b>Algorithm 1: AWE with Hard Capacity Invariant</b><br/>"
        "&nbsp;&nbsp;1: <b>Input:</b> Capacity C, incoming chunk E, boundary parameter p<br/>"
        "&nbsp;&nbsp;2: <b>if</b> E.tokens &gt; C <b>then</b> Truncate E.content to C tokens; E.tokens &larr; C<br/>"
        "&nbsp;&nbsp;3: Compute IDS(E) = AttentionWeight(E) &times; 100 / (Entropy(E) + 10^-4) [or tier prior if unmeasured]<br/>"
        "&nbsp;&nbsp;4: <b>if</b> E.key &isin; T1 &cup; T2 <b>then</b> Update and promote to T2<br/>"
        "&nbsp;&nbsp;5: <b>else if</b> E.key &isin; B1 <b>then</b> Adapt p &larr; min(C, p + |B2|/|B1| &times; E.tokens); Evict lowest IDS victim<br/>"
        "&nbsp;&nbsp;6: <b>else if</b> E.key &isin; B2 <b>then</b> Adapt p &larr; max(0, p - |B1|/|B2| &times; E.tokens); Evict lowest IDS victim<br/>"
        "&nbsp;&nbsp;7: <b>else</b> Evict lowest IDS chunk; Insert E into T1; <b>assert</b> total_tokens() &le; C"
    )
    t_algo = Table([[Paragraph(algo_text, code_style)]], colWidths=[504])
    t_algo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#cbd5e1")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_algo)
    story.append(Spacer(1, 8))

    # Section 5: Token Footprint Table
    story.append(Paragraph("5. Empirical Token Compaction Results", h1_style))
    bench_data = [
        ["Architecture Arm", "Mean Active Tokens", "Context Signal Ratio (CSR)", "Token Reduction"],
        ["Arm A: Flat Append-Only", "5,171", "0.0057", "Baseline (0.0%)"],
        ["Arm B: Auto-Compaction", "3,400", "0.0076", "-34.2%"],
        ["Arm C: Generational Context", "140", "0.2375", "-97.3% (41x CSR)"],
    ]
    t_bench = Table(bench_data, colWidths=[150, 110, 130, 114])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8.5),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TEXTCOLOR', (3, 3), (3, 3), colors.HexColor("#16a34a")),
        ('FONTNAME', (3, 3), (3, 3), 'Helvetica-Bold'),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 10))

    # Section 6: Related Work & Conclusion
    story.append(Paragraph("6. Related Work & Conclusion", h1_style))
    story.append(Paragraph(
        "Our work connects with Liu et al. (2023) on context retrieval degradation, Xiao et al. (2023) on attention sinks, "
        "Packer et al. (2023) on MemGPT tiered memory, and Megiddo & Modha (2003) on ARC. By formalizing the Softmax Inundation Bound "
        "and providing the Generational Context architecture, we offer a deterministic, verifiable memory framework that preserves "
        "foundational constraints across arbitrary interaction horizons.",
        body_style
    ))
    story.append(Spacer(1, 6))

    refs = [
        "[1] A. Vaswani et al., 'Attention is all you need,' in NeurIPS, 2017.",
        "[2] N. Megiddo and D. S. Modha, 'ARC: A self-tuning, low overhead replacement cache,' in USENIX FAST, 2003.",
        "[3] N. F. Liu et al., 'Lost in the middle: How language models use long contexts,' TACL, 2024.",
        "[4] G. Xiao et al., 'Efficient streaming language models with attention sinks,' in ICLR, 2024.",
        "[5] C. Packer et al., 'MemGPT: Towards LLMs as operating systems,' arXiv:2310.08560, 2023."
    ]
    for r in refs:
        story.append(Paragraph(r, ParagraphStyle('RefStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10, textColor=colors.HexColor("#4b5563"))))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Academic PDF compiled successfully: {PDF_OUTPUT_PATH}")


if __name__ == "__main__":
    build_academic_pdf()
