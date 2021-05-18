from utils.google_api.api_credentials import service as s1
from utils.google_api.gdocs import service as s2


def parse_documents():
    result = s1.files().list(q="mimeType = 'application/vnd.google-apps.document'",
                                  pageSize=10, fields="nextPageToken, files(id,name, parents)").execute()
    items = result.get('files', [])
    for item in items:
        doc = s2.documents().get(documentId=item['id']).execute()
        doc_content = doc.get('body').get('content')
        shorts = {}
        for paragraph in doc_content:
            if paragraph.get('paragraph', {}).get('elements',[{}])[0].get('textRun',{})\
                    .get('content', 'null').replace('\n','null').lstrip()[0] == '#':
                shcut = paragraph['paragraph']['elements'][0]['textRun']['content']
                shtext = []
                while paragraph.get('paragraph', {}).get('paragraphStyle', {}).get('headingId') is None or \
                        paragraph.get('paragraph', {}).get('elements', [{}])[0].get('textRun', {}) \
                                .get('content') != '':
                    shtext.append(paragraph.get('paragraph', {}).get('elements',[{}])[0].get('textRun',{})\
                    .get('content'))
                print(shtext)

                # head_id = paragraph['paragraph']['paragraphStyle']['headingId']
                # for element in paragraph['paragraph']['elements']:
                #     shorts.update({element['textRun']['content'].replace('\n', ''): head_id})

parse_documents()