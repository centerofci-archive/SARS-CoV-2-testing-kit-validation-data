from get_latest_html import get_latest_html
from get_PDFs import get_PDFs
from parse_html import parse_html
from merge_parsed_data import write_merged_data



def get_latest_html_and_PDFs ():
    get_latest_html()
    parse_html()
    write_merged_data()
    get_PDFs(shallow_check=False)



if __name__ == "__main__":
    get_latest_html_and_PDFs()
