
import asyncio
from playwright.async_api import async_playwright
import markdown
import os

async def generate_pdf():
    input_file = "priority_issues.md"
    html_file = "priority_issues.html"
    output_file = "Intelsoft_Priority_Issues_Report.pdf"
    
    with open(input_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; margin: 0; padding: 0; background-color: #fff; }}
            .page-border {{
                position: fixed;
                top: 0;
                left: 0;
                bottom: 0;
                right: 0;
                border: 2px solid #2c3e50;
                z-index: 1000;
                pointer-events: none;
            }}
            .report-content {{
                padding: 40px;
            }}
            h1, h2, h3 {{ color: #2c3e50; page-break-after: avoid; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; page-break-inside: avoid; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #f7f9fa; color: #2c3e50; font-weight: bold; }}
            img {{ max-width: 100%; height: auto; border: 1px solid #ddd; margin: 20px 0; display: block; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); page-break-inside: avoid; }}
        </style>
    </head>
    <body>
        <div class="page-border"></div>
        <div class="report-content">
            {html_body}
        </div>
    </body>
    </html>
    """
    
    file_path = os.path.abspath(html_file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Intermediate HTML saved to: {file_path}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        url = f"file:///{file_path.replace(os.sep, '/')}"
        print(f"Navigating to: {url}")
        await page.goto(url)
        await page.wait_for_load_state("networkidle")
        await page.pdf(path=output_file, format="A4", print_background=True, margin={"top": "2cm", "right": "2cm", "bottom": "2cm", "left": "2cm"})
        await browser.close()
        print(f"PDF generated: {output_file}")
    
    if os.path.exists(html_file):
        os.remove(html_file)

if __name__ == "__main__":
    asyncio.run(generate_pdf())
