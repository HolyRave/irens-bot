from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/documents']
SERVICE_ACCOUNT_FILE = 'data/credentials.json'
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('docs', 'v1', credentials=credentials)


def content_by_header(elements: list, head_id: str):
    """Recurses through a list of Structural Elements to read a document's text where text may be
        in nested elements.

        Args:
            elements: a list of Structural Elements.
            head_id: id of the header
    """

    def read_text(element: dict):
        """

        :param element:
        :return:
        """
        text_run = element.get('textRun')
        if not text_run:
            return ''
        return text_run.get('content')

    text = ''
    for ind, value in enumerate(elements):
        if value.get('paragraph', {}).get('paragraphStyle', {}).get('headingId') == head_id:
            elements = elements[ind+1::]

    for ind, value in enumerate(elements):
        if value.get('paragraph', {}).get('elements',[{}])[0].get('textRun',{}).get('content','')[0] == '#':
            elements = elements[ind+1::]

    for ind, value in enumerate(elements):
        if value.get('paragraph', {}).get('paragraphStyle', {}).get('headingId') is not None and \
                value.get('paragraph', {}).get('paragraphStyle', {}).get('headingId') != head_id and \
                value.get('paragraph', {}).get('paragraphStyle', {}).get('namedStyleType') == "HEADING_1":
            elements = elements[:ind:]


    for value in elements:
        elements = value.get('paragraph').get('elements')
        for elem in elements:
            text += read_text(elem)

    return text


def get_headers(document_id: str):
    doc = service.documents().get(documentId=document_id).execute()
    doc_content = doc.get('body').get('content')
    headers = {}
    for paragraph in doc_content:
        if paragraph.get('paragraph', {}).get('paragraphStyle', {}).get('namedStyleType') == 'HEADING_1':
            head_id = paragraph['paragraph']['paragraphStyle']['headingId']
            for element in paragraph['paragraph']['elements']:
                headers.update({element['textRun']['content'].replace('\n', ''): head_id})
    service.close()
    return headers, doc_content