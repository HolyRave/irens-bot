from utils.google_api.api_credentials import service as s1
from utils.google_api.gdocs import service as s2
import json


def parse_documents():
    result = s1.files().list(q="mimeType = 'application/vnd.google-apps.document'",
                                  pageSize=10, fields="nextPageToken, files(id,name, parents)").execute()
    items = result.get('files', [])
    shorts = {}
    for item in items:
        doc = s2.documents().get(documentId=item['id']).execute()
        doc_content = doc.get('body').get('content')
        shcut = ''
        shtext = []
        text = []
        for paragraph in doc_content:
            if paragraph.get('paragraph', {}).get('paragraphStyle', {}).get('namedStyleType') == "HEADING_1":
                text.append("HED" + paragraph.get('paragraph', {}).get('elements',[{}])[0].get('textRun',{}) \
                            .get('content', ''))
            elif paragraph.get('paragraph', {}).get('elements',[{}])[0].get('textRun',{})\
                                     .get('content', 'nn')[0]=='#':
                text.append(
                    paragraph.get('paragraph', {}).get('elements', [{}])[0].get('textRun', {}).get('content', ''))
            else:
                text.append(paragraph.get('paragraph', {}).get('elements', [{}])[0].get('textRun', {}) \
                            .get('content', ''))
        text = list(filter(lambda x: x != '', text))
        switch = False
        for x in text:
            if x == '':
                continue
            elif switch is False:
                if x[0] == "#":
                    shcut = x[1::].strip().replace(' ','_')
                    if shorts.get(shcut) is None:
                        shorts[shcut] = []
                    switch = True
            else:
                if x[0:3] == "HED" and shcut == '':
                    continue
                elif x[0:3] == "HED":
                    switch = False
                    shorts[shcut].append(''.join(shtext))
                    shcut = ''
                    shtext = []
                else:
                    shtext.append(x)
        switch = False
        try:
            shorts[shcut].append(''.join(shtext))
        except KeyError:
            pass
    s1.close()
    s2.close()
    with open('short.json','w',encoding='utf-8') as f:
        f.write(json.dumps(shorts))
    return shorts
