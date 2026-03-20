import matplotlib.pyplot as plt
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


#Add footer to each page with disclaimer
def add_footer(canvas, doc):
    canvas.saveState()

    width, height = letter

    disclaimer = """
    This report is AI-generated based on provided data and prevailing market sentiment. 
    The content is for informational purposes only and does not constitute investment advice. 
    Users should exercise independent judgment and consult professional advisors before making investment decisions.
    """

    # 🔹 Smaller font
    canvas.setFont("Helvetica", 8)

    # 🔹 Position at bottom
    x = 40
    y = 40

    # Wrap text manually
    lines = disclaimer.split(". ")

    for line in lines:
        canvas.drawString(x, y, line.strip())
        y -= 10

    canvas.restoreState()

def save_allocation_chart(allocation, filename="allocation.png"):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(allocation, labels=allocation.index, autopct='%1.1f%%')
    ax.set_title("Portfolio Allocation")

    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)

    return filename

def save_sector_chart(df, filename="sector.png"):
    sector_perf = df.groupby('sector')['return'].mean()

    # 🔥 Wider figure (full-width feel)
    fig, ax = plt.subplots(figsize=(10, 2))  # 👈 key change

    sector_perf.plot(kind='bar', ax=ax, color="#4f46e5")

    # Labels & title
    ax.set_title("Sector Performance", fontsize=12)
    ax.set_ylabel("Return (%)")

    # 🔥 Horizontal labels (no tilt)
    ax.set_xticklabels(sector_perf.index, rotation=0, ha='center')

    # Optional: clean look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Add grid for readability
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    plt.tight_layout()  # 👈 prevents cutoff

    plt.savefig(filename, bbox_inches='tight', dpi=300)
    plt.close(fig)

    return filename

# def save_sector_chart(df, filename="sector.png"):
#     sector_perf = df.groupby('sector')['return'].mean()

#     fig, ax = plt.subplots(figsize=(5, 3))
#     sector_perf.plot(kind='bar', ax=ax)
#     ax.set_title("Sector Performance")
#     ax.set_ylabel("Return (%)")

#     plt.savefig(filename, bbox_inches='tight')
#     plt.close(fig)

#     return filename


def generate_pdf_report(metrics, risk_metrics, allocation, df, commentary, filename="report.pdf"):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    # 🔹 Title
    content.append(Paragraph("Investment Summary Report", styles['Title']))
    content.append(Spacer(1, 12))

    # 🔹 Key Metrics
    content.append(Paragraph("Key Metrics", styles['Heading2']))
    content.append(Spacer(1, 8))

    metrics_text = f"""
    Avg Return: {metrics['avg_return']:.2f}%<br/>
    Total Return: {metrics['total_return']:.2f}%<br/>
    Top Performer: {metrics['top_stock']} ({metrics['top_return']:.2f}%)<br/>
    Worst Performer: {metrics['worst_stock']} ({metrics['worst_return']:.2f}%)<br/>
    Volatility: {risk_metrics['volatility']:.2f}%<br/>
    Sharpe Ratio: {risk_metrics['sharpe_ratio']:.2f}
    """

    content.append(Paragraph(metrics_text, styles['BodyText']))
    content.append(Spacer(1, 16))

    # 🔹 Charts
    allocation_img = save_allocation_chart(allocation)
    sector_img = save_sector_chart(df)

    content.append(Paragraph("Portfolio Allocation", styles['Heading2']))
    content.append(Image(allocation_img, width=4*inch, height=4*inch))
    content.append(Spacer(1, 16))

    content.append(Paragraph("Sector Performance", styles['Heading2']))
    content.append(Image(sector_img, width=5*inch, height=1.8*inch))
    content.append(Spacer(1, 16))

    # 🔹 Commentary
    content.append(Paragraph("Portfolio Insights & Market Outlook", styles['Heading2']))
    content.append(Spacer(1, 8))
    #content.append(Paragraph(commentary, styles['BodyText']))
    bullet_text = commentary.replace("\n", "<br/>")
    content.append(Paragraph(bullet_text, styles['BodyText']))

    # 🔹 Disclaimer
    # small_style = ParagraphStyle(
    #     'small',
    #     parent=styles['BodyText'],
    #     fontSize=8,
    #     leading=10
    # )

    # disclaimer_text="This report has been generated using artificial intelligence (AI) tools based on the data inputs provided and publicly available market information. The commentary, analysis, and market outlook presented herein are AI-generated and may incorporate prevailing market sentiment, statistical patterns, and historical data trends."
    # "The views, opinions, and estimates expressed in this report are for informational purposes only and do not constitute investment advice, recommendation, or an offer to buy or sell any financial instruments. The content does not take into account the specific investment objectives, financial situation, or particular needs of any individual investor."
    # "The views, opinions, and estimates expressed in this report are for informational purposes only and do not constitute investment advice, recommendation, or an offer to buy or sell any financial instruments. The content does not take into account the specific investment objectives, financial situation, or particular needs of any individual investor."
    # "While reasonable care has been taken to ensure the accuracy of the data and the reliability of the analysis, no representation or warranty, express or implied, is made as to the completeness, accuracy, or correctness of the information contained herein. Market conditions are subject to change, and past performance is not indicative of future results."
    # "Users of this report are advised to exercise independent judgment and consult with qualified financial, legal, or tax advisors before making any investment decisions. The creators of this report and associated tools shall not be held liable for any direct or indirect losses arising from the use of this information."

    #content.append(Paragraph(disclaimer_text, small_style))
    # Build PDF
    #doc.build(content)
    doc.build(content, onFirstPage=add_footer, onLaterPages=add_footer)

    # Cleanup images
    if os.path.exists(allocation_img):
        os.remove(allocation_img)
    if os.path.exists(sector_img):
        os.remove(sector_img)

    return filename