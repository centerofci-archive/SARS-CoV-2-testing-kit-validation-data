from get_latest_csv import get_latest_csv
from parse_versions import parse_versions
from check_test_ids import check_test_ids



def get_and_parse_latest ():
    get_latest_csv()
    parse_versions()
    check_test_ids()



if __name__ == "__main__":
    get_and_parse_latest()
