
import asyncio
from playwright.async_api import async_playwright
import markdown
import os

async def generate_pdf():
    input_file = "issue_report.md"
    html_file = "issue_report.html"  # Intermediate file to resolve relative paths
    output_file = "Intelsoft_LMS_Issue_Report.pdf"
    
    # Read markdown
    with open(input_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert to HTML
    html_body = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
    
    # Full HTML structure
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 40px; }}
            h1, h2, h3 {{ color: #2c3e50; page-break-after: avoid; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; page-break-inside: avoid; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            /* UPDATED: Full width images, handle page breaks better */
            img {{ width: 100%; height: auto; border: 1px solid #ddd; margin: 20px 0; display: block; page-break-inside: avoid; }}
            code {{ background-color: #f8f9fa; padding: 2px 4px; border-radius: 4px; white-space: pre-wrap; word-wrap: break-word; }}
            pre {{ background-color: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto; white-space: pre-wrap; word-wrap: break-word; }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    # Write HTML file to disk so relative paths (assets/...) resolve correctly
    file_path = os.path.abspath(html_file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Intermediate HTML saved to: {file_path}")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Open the local HTML file using file protocol
        url = f"file:///{file_path.replace(os.sep, '/')}"
        print(f"Navigating to: {url}")
        await page.goto(url)
        
        # Wait for network idle to ensure images load
        await page.wait_for_load_state("networkidle")
        
        await page.pdf(path=output_file, format="A4", print_background=True, margin={"top": "2cm", "right": "2cm", "bottom": "2cm", "left": "2cm"})
        await browser.close()
        print(f"PDF generated: {output_file}")
    
    # Optional: cleanup
    if os.path.exists(html_file):
        os.remove(html_file)

if __name__ == "__main__":
    asyncio.run(generate_pdf())
