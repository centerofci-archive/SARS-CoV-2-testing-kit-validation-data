import hashlib
import os
import re
import requests
import sys
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + "/..")

from common import (
    get_fda_eua_parsed_data,
    filter_for_urls,
    get_FDA_EUA_pdf_file_id_from_FDA_url,
    get_FDA_EUA_pdf_file_path_from_FDA_url,
    DATA_DIRECTORY_EUA_PDFs,
)


DELAY_SECONDS_BETWEEN_REQUESTS = 2


def check_urls_are_unique(urls):
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
    ]
    unique_urls = set()
    for url in urls:
        if url in unique_urls and url not in known_duplicate_urls:
            duplicated_urls.append(url)
        else:
            unique_urls.add(url)

    if duplicated_urls:
        raise Exception("ERROR: not all urls are unique: ", duplicated_urls)


def get_map_of_existing_versions ():
    map_of_existing_versions = dict()

    for file_path in os.listdir(DATA_DIRECTORY_EUA_PDFs):
        if os.path.isdir(file_path):
            continue

        root_file_id = file_path.split("_")[-1].replace(".pdf", "")
        if root_file_id not in map_of_existing_versions:
            map_of_existing_versions[root_file_id] = []

        map_of_existing_versions[root_file_id].append(file_path)

    return map_of_existing_versions


def download_urls (urls, map_of_existing_versions, shallow_check=True):
    for url in urls:

        file_id = get_FDA_EUA_pdf_file_id_from_FDA_url(url)
        existing_versions = map_of_existing_versions[file_id]

        if existing_versions and shallow_check:
            print("Skipping: " + url)
            continue
        elif existing_versions:
            print("Checking for newer version of: " + url)

        print("Downloading: " + url)
        request = requests.get(url)
        time.sleep(DELAY_SECONDS_BETWEEN_REQUESTS)

        if not shallow_check:
            match = hash_matches_existing_versions(request.content, existing_versions)
            if match:
                print("x - Same as existing version: " + match)
                continue
            else:
                print("y - Saving a new version.")

        file_path_with_date = get_FDA_EUA_pdf_file_path_from_FDA_url(url, add_datetime=True)
        with open(file_path_with_date, "wb") as f:
            f.write(request.content)


def hash_matches_existing_versions(new_contents, existing_versions):
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


def deprecated_main():
    fda_eua_parsed_data = deprecated_get_fda_eua_parsed_data(merged=False)
    urls = filter_for_urls(fda_eua_parsed_data["fda_eua_iv_parsed_data"])
    urls += filter_for_urls(fda_eua_parsed_data["fda_eua_high_complexity_parsed_data"])
    print("Extracted {} urls to download".format(len(urls)))
    check_urls_are_unique(urls)
    download_urls(urls)


def main():
    fda_eua_parsed_data = get_fda_eua_parsed_data()
    urls = filter_for_urls(fda_eua_parsed_data)
    print("Extracted {} urls to download".format(len(urls)))
    check_urls_are_unique(urls)
    map_of_existing_versions = get_map_of_existing_versions()
    download_urls(urls, map_of_existing_versions, shallow_check=False)


main()
