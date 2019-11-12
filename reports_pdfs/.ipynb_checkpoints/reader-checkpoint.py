import PyPDF2

def pdf_reader(path):
    try:
        file_obj = open(path,'rb')
        reader_obj = PyPDF2.PdfFileReader(file_obj)
        return reader_obj
    except:
        return 'Unable to Read'

def pdf_page_count(path):
    try:
        reader_obj = pdf_reader(path) 
        page_count = reader_obj.numPages
        return page_count
    except:
        return 'Unable to Read'

def pdf_text(path):
    try:
        reader_obj = pdf_reader(path) 
        for i in range(pdf_page_count(path)):
            pdf_text=[]
            page_object = reader_obj.getPage(i)
            page_text = page_object.extractText()
            pdf_text.append(page_text)
        return pdf_text
    except:
        return 'Unable to Read'

                       
                       
                       
                       