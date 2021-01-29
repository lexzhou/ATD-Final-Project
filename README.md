# ATD-DRAE_TWITTER-API (under-development version)

## Introduction
For the time being, billions of users use Twitter, generating more than 12 Terabytes of data daily since 2018. In recent years, many fields such as business, industries, governments, as well as scientists have been leveraging this vast amount of non-structured data producing intriguing investigations and helpful results to comprehend social interactions patterns.

## Objectives
Utilizing web scraping, API of Twitter, NLP (Natural Language Processing) technics, and Python library Flask to provide a prototype of API which comprises an amicable environment for users (primarily who speak English and/or Spanish) who are interested in analyzing social interactions patterns regarding distinct trending topics and social profile of whichever users in Twitter, regardless of the language. The output will be an object JSON or XML (using Python or Browser).

Another additional aim that we have is to provide another API with the functions and methods of DRAE (Dictionary of Spanish Real Academy) which currently does not exist in Python. For example, we can translate and acquire the words' definitions of different languages. With this API, we firstly seek to enrich the results obtained from Twitter information analysis (e.g. obtain the definitions, expressions of anagrams, etc.), adding as additional elements of the output (SON/XML objects). Moreovere, build a prototype of a multifunctional package with all feasible features of DRAE https://www.rae.es/.

## Results and the package’s methods.
For this work, we created two APIs: (1) API of DRAE, and (2) API of Twitter analysis. In the file `Twitter_Analysis_API.py` describes the codes of Twitter Analysis API and in the file `DRAE_API.py` describes the codes of DRAE API which internally use a RAE package `RAE.py` created by the authors. To see practical examples with Python codes, please view the tutorials `Twitter_Analysis.ipynb` and `DRAE_Tutorial.ipynb`.

## Limitations and possible future development
**Limitation in extracting Twitter between a specific time range**: due to the last update in the API of Twitter that occurred two months ago, which no longer allows extracting tweets from a trending topic within a specific time range. One possible solution might be extracting a large number of tweets and filter them by the publish date.

**Temporal limitation**: We recommend to use the multicore technique using more CPU threads and/or distributed computing approach to improve time efficiency.

**Expand the query options**: providing methods which allow the analysis of followers and the people who follow for a specific user, as well as other analyzes related to NLP and not only count the frequencies of words and bigrams (e.g. Network analysis, individual opinions regarding differences between different political parties, the evolution of opinions of Valencian citizens regarding COVID, etc).

**Non-existent/innovative API development**: Expand and provide API about DRAE and NLP analysis which comprise more complex and friendly methods that allow parsing the information stored in Twitter, not only for skilled people who use Python or other programming language but also citizens.

#### *This is only a prototype version of our APIs, still need many refinement. What's more, it will be interesting to expand more and publish not only API but also new Python packages such as DRAE and text mining packages in near future.*

## The descriptions of the available files:

`Twitter_Analysis_API.py` --> Codes of Tweeter Analysis (TA) API

`Twitter_Analysis.ipynb` --> Tutorial of parsing data from the TA API in Jupyter Notebook format

`RAE.py` --> RAE package created by the authors with similar methods and functions provided in https://www.rae.es/.

`DRAE_API.py` --> DRAE API which uses internally RAE.py package

`DRAE_Tutorial.ipynb` --> Tutorial of parsing data from DRAE API in Jupyter Notebook format

## Package' Status
- Version: 0.0.1
- Authors: Francisco Tomás García Ruiz (UPV), Lexin Zhou (UPV)
- Maintainer: Francisco Tomás García Ruiz (UPV), Lexin Zhou (UPV)
- Authorship: No competing interest between authors
