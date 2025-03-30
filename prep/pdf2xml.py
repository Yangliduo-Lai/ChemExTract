import pdfplumber
import xml.etree.ElementTree as ET


def pdf_to_xml_pdfplumber(pdf_path, xml_path):
    root = ET.Element("PDFDocument")

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_element = ET.SubElement(root, "Page", number=str(page_number))

            # 提取文本
            text = page.extract_text()
            text_element = ET.SubElement(page_element, "Text")
            text_element.text = text.strip() if text else "No text found"

    tree = ET.ElementTree(root)
    tree.write(xml_path, encoding="utf-8", xml_declaration=True)
    print(f"转换完成: {xml_path}")
