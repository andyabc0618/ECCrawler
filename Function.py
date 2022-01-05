import os

def check_folder(website_name):
    current_position   = os.getcwd()
    current_position   = current_position.replace("\\","/")
    output_folder_path = current_position + "/"+website_name
    if not os.path.isdir(output_folder_path):
        os.makedirs(output_folder_path)

def check_csvname(csvname):
    csvname = csvname.replace('\\','')
    csvname = csvname.replace('/','')
    csvname = csvname.replace(':','')
    csvname = csvname.replace('*','')
    csvname = csvname.replace('?','')
    csvname = csvname.replace('<','')
    csvname = csvname.replace('>','')
    csvname = csvname.replace('~','')
    csvname = csvname.replace('|','')

    return csvname
