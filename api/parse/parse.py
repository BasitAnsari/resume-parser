import docx2txt
import spacy
import pickle
import random
import PyPDF2
import re
import pandas as pd
import pathlib
from django.conf import settings
from pdfminer.pdfpage import PDFPage
# from pdfminer.converter import TextConverter
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
#loading spacy model
base_dir =settings.MEDIA_ROOT
model_dir = base_dir + "/parse/nlp_ner_model"
nlp_model = spacy.load(model_dir)
parsed_data ={}
#removing all numerical values and lowercase all strings
def filter_list(lis):
    res = []
    for item in lis:
        try:
            float(item)
        except ValueError:
            item = item.lower()
            res.append(item)       
    return res
def l_to_s(list):
    string = ""
    for item in list:
        string += item + ', '
    return string

#PDF Miner
def onePdfToTxt(filepath):
        fp = open(filepath, 'rb')
        # outfp = open(outpath, 'w', encoding='utf-8')
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        text1 = ""
        if not doc.is_extractable:
            pass

        else:
            resource = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(resource, laparams=laparams)
            interpreter = PDFPageInterpreter(resource, device)
            for page in enumerate(PDFPage.create_pages(doc)):
                interpreter.process_page(page[1])
                layout = device.get_result()
                for out in layout:

                    if hasattr(out, "get_text"):
                        text = out.get_text()
                        text1 += text
                        # outfp.write(text+'\n')
            fp.close()
            return text1


# path = "2.pdf"

# t = onePdfToTxt(path)
# print(t)



#parse function
def Parse(file):
    # print(file)
    ext = pathlib.Path(file).suffix
    ext = ext.lower()
    if ext == '.pdf':
        text1 = ""
        text1 = onePdfToTxt(file)
        # pdfFileObj = open(file, 'rb')
        # pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        # number_of_pages = pdfReader.getNumPages()
        # for page_number in range(number_of_pages):
        #     page = pdfReader.getPage(page_number)
        #     text1 += page.extractText()
    elif ext == '.txt':
        text1 = open(file, 'r').read()
    elif ext == '.text':
        text1 = open(file, 'r').read()
    # elif ext == '.doc':
    elif ext == '.docx':
        text1 = docx2txt.process(file)
    text = text1
    # print(text)
    # print("text)")
    # #extracting email(s)   
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)

    #extracting phone number(s)
    phone = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
    
    #creating data for skills and designation
    skills_txt = base_dir + '/parse/skills.txt'
    skills_csv = base_dir + '/parse/csvskills.txt'

    skills = []
    ex1 = open(skills_txt,'r',encoding="UTF-8").read().splitlines()
    ex3 = open(skills_csv,'r',encoding="UTF-8").read().splitlines()


    # excel_dir = base_dir + '/parse/data.xlsx'
    # txt_dir = base_dir + '/parse/all_skills.txt'
    # # df = pd.read_excel(excel_dir,0)
    # # ex1 = df['skill_group_name'].to_list()
    # ex2 = open(txt_dir,'r',encoding="UTF-8").read().splitlines()
    final_skill = filter_list(list(set(ex1 + ex3)))
    skill_list = []
    for item in final_skill:
            item = item.lower()
            skill_list.append(item)
    # print(final_skill)
    # ex11 = df['CurrentJobTitleSelect'].to_list()
    # ex12 = df['Title'].to_list()
    # final_desig = filter_list(list(set(ex11 + ex12)))
    #printing skills and designation
    words = text.split()
    resume_desig=[]
    resume_skill=[]
    print(skill_list)
    for word in words:
        if word.lower() in skill_list:
            resume_skill.append(word)
            
        # if word in final_desig:
        #     resume_desig.append(word)
    # deleting duplicate entries
    # resume_desig = list(set(resume_desig))
    resume_skill = list(set(resume_skill))
    print(resume_skill)
    
    # nlp
    text = text.lower()
    text = text.replace('\n',' ')
    doc = nlp_model(text)
    name = []
    clg_name =[]
    desig = []
    deg = []
    exp = []
    for ent in doc.ents:
        if ent.label_.upper() == 'NAME':
            name.append(ent.text)
        elif ent.label_.upper() == 'COLLEGE NAME':
            clg_name.append(ent.text)
        elif ent.label_.upper() == 'DEGREE':
            deg.append(ent.text)
        elif ent.label_.upper() == 'YEARS OF EXPERIENCE':
            exp.append(ent.text)
        elif ent.label_.upper() == 'DESIGNATION':
            desig.append(ent.text)
    parsed_data = {
        "text" : text1,
        "phone" : l_to_s(phone),
        "email" : l_to_s(emails),
        "skills" : l_to_s(resume_skill),
        "designation": l_to_s(desig),
        "degree": l_to_s(deg),
        "college": l_to_s(clg_name),
        "experience": l_to_s(exp),
        "name":l_to_s(name),
        "is_parsed": True   
    }
    print(parsed_data)
    return parsed_data