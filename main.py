import requests
import json
import csv
import numpy as np
import pandas as pd
from experts_api_query import gets_pure_access_info


def get_unpaywall_data():
    # articles = csv_to_dict("/Users/elizabethschwartz/Documents/assistantships/scp/unpaywall_experiments/research-output-test.csv")
    df_articles  = pd.read_excel("/Users/elizabethschwartz/Documents/assistantships/scp/unpaywall_experiments/test_outputs.xls")
    articles_dois = df_articles['16.1 Electronic version(s) of this work > DOI (Digital Object Identifier)[1]']
    dois = []
    for index, value in articles_dois.items():
        # print('index:', index, '\t doi:', value)
        dois.append(value)
    dois = np.unique(dois)
    print(len(dois))
    print(len(dois))
    report = []
    for doi in dois:
        print(doi)
        # if unpaywall == false then we need to print
        try:
            report.append({
                'doi' : doi,
                'UNPAYWALL': make_unpaywall_request(doi),
                'PURE': gets_pure_access_info(doi)

            })
            print('UNPAYWALL:', make_unpaywall_request(doi))
            print('PURE:', gets_pure_access_info(doi))
            print()
        except TypeError:
            pass
    error_report = []
    for item in report:
        try:
            error_status = analyze_pure_and_unpaywall_diff(item['PURE'], item['UNPAYWALL'])
        except TypeError:
            error_status = None
        if error_status != None:
            error_report.append({
                'doi': item['doi'],
                'error_code' : error_status,
                'pure_OA_status': item['PURE']['access'],
                'unpaywall_OA_status': gets_unpaywall_access_status(item['UNPAYWALL']['is_OA']),
                'pure_version' : item['PURE']['version'],
                'unpaywall_version' : item['UNPAYWALL']['version'],
                'pure_url' : item['PURE']['portal_url'],
                'unpaywall_oa_url' : item['UNPAYWALL']['oa_url']
            })
    makes_results_csv(error_report, 'nov15_dec1_2022_error_report_from_2023-02-16.csv')
    with open('report2.txt', 'w') as outfile:
        for entry in report:
            print(entry['doi'], file=outfile)
            print('UNPAYWALL:', entry['UNPAYWALL'], file=outfile)
            print('PURE:', entry['PURE'], file=outfile)
            print('\n', file=outfile)



def gets_unpaywall_access_status(unpaywall_access):
    if unpaywall_access:
        return 'Open'
    else:
        return 'Closed'


def analyze_pure_and_unpaywall_diff(pure, unpaywall):
    if pure['access'] == 'Open' and unpaywall['is_OA'] == True:
        # print('both pure and unpaywall think this is open- checking what version')
        # print('unpaywall version:', unpaywall['version'])
        if pure['version'] == unpaywall['version']:
            pass
        else:
            print('WARNING VERSIONS DONT MATCH!!!!!!')
            print('pure version:', pure['version'])
            print('unpaywall version:', unpaywall['version'])
            return 'conflicting open version'
    elif pure['access'] == 'Open' and unpaywall['is_OA'] == False:
        print('WARNING!!!! CONFLICTING OA STATUS!!!')
        print(" pure says its open. unpaywall says closed. checking pure version and source")
        print(pure)
        return 'conflicting OA status'
        # check pure version and source
    elif pure['access'] != 'Open' and unpaywall['is_OA'] == True:
        print('WARNING!!!! CONFLICTING OA STATUS!!!')
        print('pure says its not open but unpaywall says it is. getting version')
        print(unpaywall['version'])
        return 'conflicting OA status'
    elif pure['access'] != 'Open' and unpaywall['is_OA'] == False:
        pass
        # print('both say its closed')
    else:
        print('weird one')


# this is probably the only function that will be helpful

def make_unpaywall_request(doi):
    # https://api.unpaywall.org/v2/10.1038/nature12373?email=YOUR_EMAIL
    this_url = "https://api.unpaywall.org/v2/"
    this_doi = doi
    email = "ers6@illinois.edu"

    the_request = requests.get(this_url + this_doi + "?email=" + email)
    if the_request.ok:
        the_request = the_request.json()
        print(the_request)
        # the_request = requests.get(this_url + this_doi + "?email=" + email)
        if the_request['best_oa_location'] != None:
            print(the_request['best_oa_location'])
            return {
                    'is_OA': the_request['is_oa'],
                    'oa_status' : the_request['oa_status'],
                    'oa_locations': the_request['oa_locations'],
                    'version' : gets_unpaywall_version(the_request['best_oa_location']['version']),
                    'oa_url': the_request['best_oa_location']['url']
                }
        else:
            return {
                'is_OA': the_request['is_oa'],
                'oa_status': the_request['oa_status'],
                'oa_locations': the_request['oa_locations'],
                'version': 'n/a',
                'oa_url': 'n/a'
            }
    else:
        print(the_request)
        print(the_request.reason)


def gets_unpaywall_version(unpaywall_version):
    if unpaywall_version == "submittedVersion":
        return 'submitted_version'
    elif unpaywall_version == "acceptedVersion":
        return 'accepted_version'
    elif unpaywall_version == "publishedVersion":
        return 'published_version'
    else:
        pass

def csv_to_dict(csv_file_name):
    prizes = []
    with open(csv_file_name, 'r', newline='', encoding='utf-8') as infile:
        csvin = csv.reader(infile)
        headers = next(csvin)
        headers = [header.strip().lower() for header in headers]
        for row in csvin:
            n = 0
            your_dict = {}
            for column in row:
                your_dict[headers[n]] = column
                n += 1
            prizes.append(your_dict)
    return prizes


def makes_results_csv(results, outfile_name):
    headers = results[0].keys()
    rows = results
    with open(outfile_name, 'w', encoding='UTF-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            try:
                writer.writerow(row)
            except AttributeError:
                pass


# get_unpaywall_data()
make_unpaywall_request('10.1111/ldrp.12272')
