from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/documents']
SERVICE_ACCOUNT_FILE = '../../data/credentials.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('docs', 'v1', credentials=credentials)


def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_strucutural_elements(elements):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
    """
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
    return text


def main():
    """Uses the Docs API to print out the text of a document."""

    doc = service.documents().get(documentId='1IYILfA3gYmBdxEbdoZah68e9BrP_EtAx_jjrbDhPgM8').execute()
    doc_content = doc.get('body').get('content')
    print(read_strucutural_elements(doc_content))
main()
# paragraphs = res.get('body').get('content')
# headers = []
# for paragraph in paragraphs:
#     if paragraph.get('paragraph',{}).get('paragraphStyle',{}).get('namedStyleType') == 'HEADING_1':
#         for element in paragraph['paragraph']['elements']:
#             headers.append(element['textRun']['content'].replace('\n',''))
# print(*headers, sep='\n')
# print(len(headers))