
# Data, tools etc.



## Historical data

* Google ngrams

* https://github.com/aparrish/gutenberg-dammit
  Corpus of every file in Project Gutenberg, with metadata
  Metadata includes author, subject, title, author birth/death date, language,
  library of congress class, maybe other stuff?
  And the corpus is a big zip file.

* British Newspaper Project - at British Library

* COHA Corpora

* Voices of the Revolution - pamphlets from the French rev
  - 1780-1810
  - digitized by Newberry library
  - sample available at https://archive.org/details/newberryfrenchpamphlets?&sort=-downloads&page=4
  - variable quality

* archive.org - tons of metadata, an API, a python library ("internetarchive") and a command line tool. Some large "collections". Goes back centuries.

* Database of Early English Playbooks - http://deep.sas.upenn.edu/
  - has date, imprint of location, genre
  - up to 1660
  - strength of plays is they are publicly put out there and popular with the groundlings....

* Word frequencies per day in US newspapers:
  - https://datadryad.org/stash/dataset/doi:10.5061/dryad.nh775
  - good for a more "disciplined" version of google ngrams
  - comes from Chronicling America
  

* Chronicling America 
  - bulk data https://chroniclingamerica.loc.gov/about/api/#bulk-data
  - it seems to be xml, within the xml is info of OCR recognition, very bulky!
  - presumably there's a standard library to turn this into text chunks....
  - text chunks already exist, as you can see the text of newspapers
  - quality *very* variable:
    - good: https://chroniclingamerica.loc.gov/lccn/sn92051283/1921-02-25/ed-1/seq-1/ocr/
    - bad: https://chroniclingamerica.loc.gov/lccn/sn85025905/1865-04-19/ed-1/seq-1/ocr/
    - sometimes it looks like one could do better using own OCR....
  - 17 million pages available
  - Coverage details: https://www.loc.gov/ndnp/data-visualizations/
  - Huge increase from 1840 to 1920, cutoff at 1920 ish (copyright) but still some data till 
    60s
  - Includes ethnic presses - many kinds! Most important are African American, German,
    French, Polish, Lat American. And some are in the relevant languages, esp Spanish, German,
    Polish. Even for smaller ones there are many pages, though not always many newspapers.


* List of historical corpora: https://www.clarin.eu/resource-families/historical-corpora
  - Including: hansard, English letters, Scottish letters, pamphlets, Royal Society articles
    from 1665; Lampeter corpus of Tracts 1640-1740; and many others including e.g. DDR 
    newspapers! Also many languages.


* Oxford Text Archive: https://ota.bodleian.ox.ac.uk/repository/xmlui/
  - Has collections including broadsides and sermons
  - Strong on C17 especially (and C16 and C18)
  - includes EEBO, see below

* Early English Books Online aims to get one copy of every "monographic" English text 1473-1700
    - useful because representative. Based on a bibliography of Eng lit.
    - available from OTA
    - See also https://quod.lib.umich.edu/e/eebogroup/ 
    - There are numerous github accounts using or working with this stuff
      - https://github.com/textcreationpartnership/Texts is a CSV with titles and subjects
        - the "terms" field of the CSV seems to be a loose library classification of sorts, e.g.
          "Church of England -- Government -- Early works to 1800.; Ecclesiastical law -- Great 
          Britain -- Early works to 1800."
      - the same guys also provide all the XMLs in separate github accounts, and there's a script
        to download em all. XML is pretty simple-looking. They have place of publication, date.

* Accessing EEBO: https://hfroehli.ch/2015/10/29/ways-of-accessing-eebotcp/
  - This actually has *many* other resources including English Short Title Catalogue, Universal STC,
    and others.

* Database of early printers
  - https://github.com/Early-Modern-OCR/ImprintDB
  - related to EEBO/ECCO
  - links printer names to places and dates

* Broadside Ballads - http://ebba.english.ucsb.edu/
  - also http://ballads.bodleian.ox.ac.uk/

* Eighteenth Century Collections Online (ECCO)
  - https://www.gale.com/intl/primary-sources/eighteenth-century-collections-online
  - seems to complement EEBO.
  - "every significant English-language and foreign-language title printed in the United Kingdom   
    between the years 1701 and 1800."
  - online tools available
  - Proquest seems to be involved in this
  - also has non-English texts!
  - A helpful github dude: https://github.com/lofhm/ECCO-TCP, including everything in XML
  - probably better: https://github.com/Early-Modern-OCR/TCP-ECCO-texts 

* Early Modern OCR Project (EMOP) https://emop.tamu.edu/
  - https://github.com/Early-Modern-OCR has tools

* Clarin corpora https://www.clarin.eu/resource-families 
  - Includes historical (above), newspaper, literary, academic, parliamentary, reference....
  - "newspaper" includes Mannheim corpus (21 C18-19 German newspapers)
  - "reference" corpora means "broad enough to be used as a reference" so these are 
    especially interesting for you. But they tend to be modern.

* Zürich English Newspaper corpus
  - https://www.es.uzh.ch/en/Subsites/Projects/zencorpus.html
  - 1661-1791
  - just need to send them an email
  - millions of words

* Europeana https://www.europeana.eu/en
  - seems hugely waffly and "in-progress" (and maybe always will be?)
  - newspapers corpus at https://www.europeana.eu/en/collections/topic/18-newspapers
  - APIs at https://pro.europeana.eu/page/apis
    - You bet they use owl and dublincore and all that shite...
  - http://www.europeana-newspapers.eu/public-materials/tools/ is older, java-based tools
  - https://pro.europeana.eu/page/linked-open-data - has info on how to get to the actual
    data

* Europeana NER corpora
  - https://github.com/EuropeanaNewspapers/ner-corpora 
  - contains named entity recognition data
  - 19th century Dutch and French, German 1926

* Anthology of middle english texts
  - https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/1398
  - tiny!

* Many papers are out there training historical word embeddings
  - https://zenodo.org/record/3585027#.YdVtaCynz0o


## Other data

* List of where to get news sources: https://blog.newscatcherapi.com/an-ultimate-list-of-open-sourced-free-tools-to-collect-parse-online-news-articles/

* Various news datasets: https://components.one/datasets
  - news, reviews, cable news transcripts, mostly modern
  - sometimes might have been scraped, so stuff you'd not get from "official sources"
  - e.g. recent NYtimes front page
  - or TED talks on Kaggle

* Kaggle datasets
  - NLP topic
  - examples:
    - Wikibooks in 7 languages
    - many news headlines
    - movie plots
    - financial news for 6000 stocks
    - goodreads data for millions of books (title, rating distribution)
    - US state of the union speeches
    - Shakespeare
    - Sentences from philosophy texts

* htttps://reddit.com/r/datasets
  - many mostly amateur-provided datasets
  - e.g. Trump speeches

* Common Crawl 100: web crawl of 100 languages. Huowge.
  - http://data.statmt.org/cc-100/

* https://newsapi.org/ for getting news headlines.
  - R library: "newsanchor". Python: newsapi-python
  - Free accounts max 1000 articles/search
  - Includes e.g. BBC news so does have some serious stuff!

* Kaggle datasets: https://www.kaggle.com/datasets

* List of NLP datasets:
  - https://github.com/niderhoff/nlp-datasets
  - including some that are truly huge (common crawl)
  - movie dialog, corporate messaging, wikipedia, social media, scientific articles, enron
    emails, google web 5grams, HISTORICAL NEWSPAPERS
  - tons of modern stuff (twitter etc.), also a large Reuters dataset


## Tools

* List of python libraries, very complete: https://github.com/ml-tooling/best-of-ml-python
  - shows number of stars, lots of quality info
  - whole section on text

* https://macroscope.tech/ - Thomas Hills
  - Sentiment analysis over time including valence, arousal, concreteness
  - Also frequency
  - Synonyms
  - I think data comes from Google ngrams?

