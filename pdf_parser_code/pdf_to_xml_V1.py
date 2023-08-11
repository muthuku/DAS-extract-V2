import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from xml.etree.ElementTree import Element, SubElement, tostring

def extract_text(pdf_path):
    text = ""
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    laparams = LAParams()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=laparams)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as pdf_file:
        for page in PDFPage.get_pages(pdf_file, caching=True, check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    converter.close()
    fake_file_handle.close()
    return text

def create_xml_structure(text):
    root = Element('article')

    sections = text.split('\n\n\n')
    for section_text in sections:
        section_elem = SubElement(root, 'sec')

        if "Data availability" in section_text:
            section_elem.set("sec-type", "data-access")
        elif "supplementary-material" in section_text:
            section_elem.set("sec-type", "supplementary-material")
        else:
            section_elem.set("sec-type", "results")

        section_lines = section_text.split('\n')
        section_title = section_lines[0]
        title_elem = SubElement(section_elem, 'title')
        title_elem.text = section_title

        content = '\n'.join(section_lines[1:])
        content_elem = SubElement(section_elem, 'p')
        content_elem.text = content

    return root

def main(pdf_path, output_path):
    pdf_text = extract_text(pdf_path)
    xml_root = create_xml_structure(pdf_text)

    xml_string = tostring(xml_root, encoding='utf-8', method='xml')
    with open(output_path, 'wb') as xml_file:
        xml_file.write(xml_string)

if __name__ == "__main__":
    pdf_path = "/Users/muthuku/Desktop/Pragati_DAS_extract_all/pdfs/jcs258834.pdf"
    output_path = "output.xml"
    
    main(pdf_path, output_path)
