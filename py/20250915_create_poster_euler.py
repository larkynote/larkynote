import numpy as np
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 1. オイラーの式による円のグラフ生成
def create_euler_plot(filename="euler_plot.png"):
    """
    Creates a plot of a circle with a cross-shaped real and imaginary axis.
    """
    plt.figure(figsize=(8, 8), dpi=100)
    ax = plt.gca()

    ax.set_facecolor('black')
    
    # 軸を十字型に設定
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    
    # オイラーの式で円周上の点を生成
    theta = np.linspace(0, 2 * np.pi, 500)
    z = np.exp(1j * theta)
    
    x_coords_real = np.real(z)
    y_coords_imaginary = np.imag(z)

    plt.scatter(x_coords_real, y_coords_imaginary, c=theta, cmap='hsv', s=5, alpha=0.8)
    
    # 軸のラベルを設定
    plt.title("Euler's Formula: $e^{i\\theta} = cos(\\theta) + isin(\\theta)$", color="white")
    plt.xlabel("Re(z)", color="white", loc='right')
    plt.ylabel("Im(z)", color="white", loc='top')
    
    ax.set_aspect('equal', adjustable='box')
    
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    plt.grid(True, linestyle='--', color='gray', alpha=0.5)
    plt.tight_layout()
    plt.savefig(filename, dpi=100, facecolor='black')
    plt.close()
    print(f"Graph saved as {filename}")
    return filename

# 2. PDFポスターの生成 (変更なし)
def create_poster(logo_text="NOOSOLOGY", pdf_filename="poster.pdf", graph_image="euler_plot.png"):
    """
    Creates a PDF poster with a large logo and a complex plane graph.
    """
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4
    
    try:
        pdfmetrics.registerFont(TTFont('Times-Bold', 'Times-Bold.ttf'))
        c.setFont("Times-Bold", 1)
    except:
        print("Times-Bold.ttfが見つかりません。デフォルトのHelvetica-Boldを使用します。")
    
    c.setFillColorRGB(0, 0, 0)
    logo_font_size = 80
    
    if 'Times-Bold' in pdfmetrics.getRegisteredFontNames():
        c.setFont("Times-Bold", logo_font_size)
    else:
        c.setFont("Helvetica-Bold", logo_font_size)
    
    text_width = pdfmetrics.stringWidth(logo_text, "Helvetica-Bold", logo_font_size)
    c.drawString((width - text_width) / 2, height - 1.5*inch, logo_text)
    
    try:
        img_width = 6.0 * inch
        img_height = 6.0 * inch
        c.drawImage(graph_image, (width - img_width) / 2, (height - img_height) / 2 - 0.5*inch, width=img_width, height=img_height)
    except FileNotFoundError:
        print(f"Error: {graph_image} not found. Please run graph generation first.")
    
    c.setFont("Helvetica", 12)
    c.drawString(inch, 1.0 * inch, "A NOOSOLOGY PROJECT")
    c.drawString(width - 2.5 * inch, 1.0 * inch, "2025")
    
    c.showPage()
    c.save()
    print(f"Poster saved as {pdf_filename}")

# メイン処理
if __name__ == "__main__":
    graph_filename = create_euler_plot()
    create_poster(graph_image=graph_filename)