from utils.google_api.gdocs import service

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
    doc = service.documents().get(documentId='1T__NlWPSlWutjEqjWM9P643ari0iz130bffoLo4eezY').execute()
    doc_content = doc.get('body').get('content')
    id_s = read_strucutural_elements(doc_content)
    list_of_ids = [x.strip() for x in id_s.split(',')]
    return list_of_ids


def user_parse():
    """Uses the Docs API to print out the text of a document."""
    doc = service.documents().get(documentId='14T6U_Q5wsACuaW4Dm9filZ4dfIIbiEYynC2e-nCzabU').execute()
    doc_content = doc.get('body').get('content')
    id_s = read_strucutural_elements(doc_content)
    list_of_ids = [x.strip() for x in id_s.split(',')]
    return list_of_ids


if __name__ == '__main__':
    main()
