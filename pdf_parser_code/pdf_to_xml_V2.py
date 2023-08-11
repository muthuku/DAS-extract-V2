import io
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
from xml.etree.ElementTree import Element, SubElement, tostring
import re

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

def create_xml_structure(text, potential_titles):
    root = Element('article')

    sections = text.split('\n\n\n')
    for section_text in sections:
        section_elem = SubElement(root, 'sec')

        section_title, section_content = section_text.split('\n', 1)

        sec_type = "results"  # Default sec-type
        for title in potential_titles:
            if title in section_title:
                sec_type = title.lower().replace(" ", "-")
                break

        section_elem.set("sec-type", sec_type)
        title_elem = SubElement(section_elem, 'title')
        title_elem.text = section_title

        content_elem = SubElement(section_elem, 'p')
        content_elem.text = section_content

    return root

def main(pdf_path, output_path, potential_titles):
    pdf_text = extract_text(pdf_path)
    xml_root = create_xml_structure(pdf_text, potential_titles)

    xml_string = tostring(xml_root, encoding='utf-8', method='xml')
    with open(output_path, 'wb') as xml_file:
        xml_file.write(xml_string)


def extract_key_info_from_text(text):
    # Extract journal info-doesn't work yet
    journal_pattern = re.compile(r'© \d{4}\. Published by .*?(\d+\s\w+\s\(\d+\)\s\d+,.*?doi:\d+\.\d+/\S+)', re.DOTALL)
    journal_match = journal_pattern.search(text)
    journal_info = journal_match.group(1).strip() if journal_match else None

    # Extract data availability
    data_avail_pattern = re.compile(r'Data availability\n(.*?https://doi.org/\S+)', re.DOTALL)
    data_avail_match = data_avail_pattern.search(text)
    data_availability = data_avail_match.group(1).strip() if data_avail_match else None

    return {
        'journal_info': journal_info,
        'data_availability': data_availability
    }

if __name__ == "__main__":
    with open("output_3.xml", "r") as text_file:
        text = text_file.read()

    key_info = extract_key_info_from_text(text)

    #print("Journal Info:", key_info['journal_info'])
    print("Data Availability:", key_info['data_availability'])


# if __name__ == "__main__":
#     pdf_path = "/Users/muthuku/Desktop/Pragati_DAS_extract_all/pdfs/jcs258834.pdf"
#     output_path = "output_3.xml"
#     potential_titles = ["Code availability", "Data availability", "Data accessibility"]
    
#     main(pdf_path, output_path, potential_titles)
