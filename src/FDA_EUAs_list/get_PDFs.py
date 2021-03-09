from datetime import datetime
import hashlib
import os
import re
import requests
import sys
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + "/..")

from common import (
    filter_for_urls,
    get_FDA_file_id_from_FDA_url,
    DATA_DIRECTORY_EUA_PDFs,
    DATA_DIRECTORY_EUAs,
)

from FDA_EUAs_list.FDA_EUAs_parsed_data import get_latest_fda_eua_parsed_data


DELAY_SECONDS_BETWEEN_REQUESTS = 2


def check_urls_are_unique (urls):
    duplicated_urls = []
    known_duplicate_urls = [
        "https://www.fda.gov/media/137741/download",  # error?
        "https://www.fda.gov/media/140715/download",  # error?
        "https://www.fda.gov/media/137181/download",  # ok?
        "https://www.fda.gov/media/137355/download",  # error - QIAstat Letter Granting EUA Amendments (April 23, 2020) points to one for NeuMoDx Molecular, Inc.
        "https://www.fda.gov/media/136599/download",  # ok - points to generic info
        "https://www.fda.gov/media/136600/download",  # ok - points to generic info
        "https://www.fda.gov/media/142307/download",  # error - Should be GK Accu-Right HCP doc but is their letter of authorization
        "https://www.fda.gov/media/142421/download",  # error - Orawell IgM/IgG Rapid Test has this for HCP and Recipient
        "https://www.fda.gov/media/137782/download",  # ok
        "https://www.fda.gov/media/141670/download",  # error? - listed under Fluidigm Corporation, Advanta Dx SARS-CoV-2 RT-PCR Assay but is for DxTerity
    ]
    unique_urls = set()
    for url in urls:
        if url in unique_urls and url not in known_duplicate_urls:
            duplicated_urls.append(url)
        else:
            unique_urls.add(url)

    if duplicated_urls:
        print("\n\n#####################\n\nERROR: not all urls are unique:\n\n{}\n\nCheck the latest html file for these urls and see if there are reasonable duplication, mistakes from FDA, or bugs in our parsing code.\n\n#####################\n\n".format(duplicated_urls))

        raise Exception("ERROR: see message above for suggested fix.")



def get_FDA_file_id_to_versioned_file_paths_map ():
    FDA_file_id_to_versioned_file_paths_map = dict()

    for file_path in os.listdir(DATA_DIRECTORY_EUA_PDFs):
        if os.path.isdir(file_path):
            continue

        FDA_file_id = file_path.split("_")[-1].replace(".pdf", "")
        if FDA_file_id not in FDA_file_id_to_versioned_file_paths_map:
            FDA_file_id_to_versioned_file_paths_map[FDA_file_id] = []

        FDA_file_id_to_versioned_file_paths_map[FDA_file_id].append(file_path)

    return FDA_file_id_to_versioned_file_paths_map



def download_urls (urls, FDA_file_id_to_versioned_file_paths_map, shallow_check=True):
    for url in urls:

        FDA_file_id = get_FDA_file_id_from_FDA_url(url)
        existing_versions = FDA_file_id_to_versioned_file_paths_map.get(FDA_file_id, [])

        if existing_versions and shallow_check:
            print("Skipping: " + url)
            continue
        elif existing_versions:
            print("Checking for newer version of: " + url)

        print("Downloading: " + url)
        request = requests.get(url)
        print("Downloaded: {}   Sleeping for {}".format(url, DELAY_SECONDS_BETWEEN_REQUESTS))
        time.sleep(DELAY_SECONDS_BETWEEN_REQUESTS)

        if not shallow_check:
            match = hash_matches_existing_versions(request.content, existing_versions)
            if match:
                print("x - Same as existing version: " + match)
                continue
            else:
                print("y - Saving a new version.")

        versioned_absolute_file_path = get_FDA_url_to_FDA_PDF_versioned_absolute_file_path(url)
        with open(versioned_absolute_file_path, "wb") as f:
            f.write(request.content)



def hash_matches_existing_versions (new_contents, existing_versions):
    match = None

    new_contents_hash = sha1_hash_string(new_contents)

    for existing_version in existing_versions:
        with open(DATA_DIRECTORY_EUA_PDFs + existing_version, "rb") as f:
            existing_contents_hash = sha1_hash_file(f)

        if existing_contents_hash == new_contents_hash:
            match = existing_version
            break

    return match



def sha1_hash_string (file_contents):
    sha_1 = hashlib.sha1()
    sha_1.update(file_contents)
    return sha_1.hexdigest()



# Adapted from: https://stackoverflow.com/a/22058673/539490
# Duplicated from annotator script
def sha1_hash_file (file_descriptor):
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    sha1 = hashlib.sha1()

    while True:
        data = file_descriptor.read(BUF_SIZE)
        if not data:
            break
        sha1.update(data)

    return sha1.hexdigest()



def get_FDA_url_to_FDA_PDF_versioned_absolute_file_path (FDA_url):
    FDA_file_id = get_FDA_file_id_from_FDA_url(FDA_url)

    datetime_version = datetime.now().strftime("%Y-%m-%d__%H-%M")

    versioned_absolute_file_path = DATA_DIRECTORY_EUAs + "PDFs/{}__{}.pdf".format(datetime_version, FDA_file_id)

    return versioned_absolute_file_path



def make_urls_unique (urls):
    seen_urls = set()
    unique_urls = []
    for url in urls:
        if url in seen_urls:
            continue
        unique_urls.append(url)
        seen_urls.add(url)

    return unique_urls



def get_PDFs (shallow_check, restart_from_url = ""):
    fda_eua_parsed_data = get_latest_fda_eua_parsed_data()
    urls = filter_for_urls(fda_eua_parsed_data)
    check_urls_are_unique(urls)
    urls_unique = make_urls_unique(urls)
    print("Extracted {} urls, {} unique".format(len(urls), len(urls_unique)))

    urls_to_download = urls_unique
    if restart_from_url:
        start_from_index = None
        for index, url in enumerate(urls_to_download):
            if url == restart_from_url:
                start_from_index = index
                break
        if start_from_index is None:
            raise Exception("Could not find url to restart from: " + restart_from_url)
        urls_to_download = urls_to_download[start_from_index:]
    print("Will download {} urls".format(len(urls_to_download)))

    FDA_file_id_to_versioned_file_paths_map = get_FDA_file_id_to_versioned_file_paths_map()
    download_urls(urls_to_download, FDA_file_id_to_versioned_file_paths_map, shallow_check=shallow_check)

    print("\nFinished downloading {} urls".format(len(urls_to_download)))



if __name__ == "__main__":
    get_PDFs(shallow_check = False, restart_from_url="")
