from get_latest_html import get_latest_html
from get_PDFs import get_PDFs
from parse_html import parse_html



def get_latest_html_and_PDFs ():
    get_latest_html()
    parse_html()
    get_PDFs(shallow_check=False)



if __name__ == "__main__":
    get_latest_html_and_PDFs()
