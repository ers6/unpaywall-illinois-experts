# unpaywall-illinois-experts
unpaywall program created for UIUC's Research Information Management System (Illinois Experts)

## Why did we make this? 
This program was created by my (Elizabeth) in order to differentiate open access definitions of journal articles in UIUC's RIM system (Illinois Experts) against their definitions in unpaywall.
The program is designed to ingest an excel file of journal articles with DOIs, grab the DOIs, and for each DOI check the OA status in Illinois Experts and unpaywall. If these statuses are conflicting, it prints the DOI to a results csv file for manual review. 

## How could we use this? 
The SCDPs is working on a project to determine how much WashU faculty are paying in article processing fees for publishing OA content. As the first step of this project, librarians are working to generate a complete list of WashU faculty published OA content. 
Most of this program will be unhelpful for this use case. However, the function, make_unpaywall_request() could be useful if we are able to generate a list of DOIs to feed to it. To get this list of DOIs, we could search databases for researcher affiliation fields in which WashU appears and export a list of publicatitons in BibTex. From there, converting to JSON and parsing DOIs could be pretty feasible. 
