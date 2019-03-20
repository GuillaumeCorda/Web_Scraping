# Project for Information Retrieval

In this repository can be found the code used to crawl www.huurda.nl/, a dutch apartment renting website.

## Notebooks

The first notebook scraper_apartments.ipynb allows the user to crawl data from Amsterdam, Den Haag, Eindhoven, Groningen, Rotterdam and Utrecht and store it as a csv file after few cleaning steps.

The second notebook text_analysis.ipynb is used to tokenize, clean and stem the description of the apartments, in dutch, english or french. You can also build a distributed index from the vocabularies (the multithread option is available while building the index).

## Data

All the output from the notebooks are stored in this folder. The raw data extracted is crawled_data.csv. The file containing the text analysis is data_processed.csv. The other files have explicit names.


