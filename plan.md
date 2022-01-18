
## Plan for analysing "industrious revolution" in English text

* Use EEBO
* Research question: is there an "industrious revolution" or a "cooperative revolution"
  in culture in England? If so, when?
* Use tools:
  - Word counts of words related to industry and/or cooperation
  - Positiveness of words associated with these words
  - Run a glove-style analysis on EEBO, per year (or per-10 year?)


## About EEBO

EEBO texts are encoded in XML. A typical URL looks like:
https://raw.githubusercontent.com/textcreationpartnership/A00002/master/A00002.xml.
A01224
There is a list file of all URLs at
https://raw.githubusercontent.com/textcreationpartnership/Texts/master/graball.sh.

A CSV file with metadata and TCP identifiers (like A00002 above) is at:
https://raw.githubusercontent.com/textcreationpartnership/Texts/master/TCP.csv

Or you can get everything at once? at
https://www.dropbox.com/sh/pfx619wnjdck2lj/AAAeQjd_dv29oPymNoKJWfEYa?dl=0.
The "P5_XML" files for "EEBO phase 1" are 13 zip files, each about 300 Mb zipped.
In "EEBO phase 2", there's more like 100+ zip files, but only about 10Mb zipped.
Probably could download them all and then unzip one by one. Or even
"save to dropbox" and have them stored online. See the TCP-readme.txt. Note that
it says:

> In the case of Evans, ECCO, and EEBO-1, these are simply 'snapshots' (downloads)* 
> of the gitHub texts (accomplished via a wget batch file, supplied
> here as well); in the case of EEBO-2, the files were obtained from the 
> Oxford Text Archive and have not yet (August 2020) been posted to a gitHub 
> repository, though discussions are under way.


They have different encodings. There is TEI P4 and TEI P5, which are some kind of XML.
See https://tei-c.org for details: TEI seems to be one of those drowning-in-metadata
type standards.

An alphabetical list of tags is at https://textcreationpartnership.org/docs/dox/cheat.html.

Metadata for the texts is available at https://github.com/lb42/eebo-bib.

A sample chunk from an XML file:

<hi>Knowledge</hi> is like the talents which the <hi>Lord,</hi>
</l>
<l>When he went forth did to his seruants lend:</l>
<l>The first who his one talent vp did hoard,</l>
<l>Like him, that for his <hi>Knowledge</hi> doth contend;</l>
<l>But therewith not himselfe, nor others mend:</l>
<l>Hee that with talents two, gain'd other twaine;</l>
<l>Is he that doth his time and labour spend</l>
<l>To saue himselfe, and those with him remaine,</l>
<l>But he that gaind the fiue; seeks all mens soules to gaine.</l>

                    
And a sample metadata:

<bibl n="tcp2:A27147" ref="proquest:2248535329" xml:id="eebo:7571302" facs="eeboIs:40093" type="Book" xml:lang="eng">
<idno type="STC">Wing B155</idno>
<idno type="STC">ESTC R178</idno>
<series>Early English Books, 1641-1700 (Wing)</series>
<title>Adagia Scotica, or, A collection of Scotch proverbs and proverbial phrases collected by R.B. ...</title>
<author>R. B.</author>
<pubDate>1668</pubDate>
<publisher>Printed for Nath. Brooke ...</publisher>
<pubPlace>England</pubPlace>
<note type="keywords">Adages, aphorisms, emblem books, jests, proverbs</note>
<note type="sourceLibrary">The Huntington Library</note>
<note type="transcriptType">text image</note>
<note type="langNote">English</note>
<measure type="pp">31</measure>
</bibl>

# Lemmatizing

* There's VARD (unmaintained, doesn't work out of the box)
* And MorphAdorner (unmaintained, runs but errors out of the box)
* And a paper by 2 guys explaining what they did in papers/
* And there's LEME
* Simplest version might be just "create embeddings on the raw
  variants", if you get very close variants with very close
  spellings, lemmatize". Or even don't bother, perhaps it isn't
  relevant? (What if you did letter-based prediction?)
* LEME approach:
  - some of the 282 lexicons have been annotated like:
  <wordentry type="h"><form lang="en" lexeme="absurdity(n)">Absurditie,</form> 
  <xpln lang="en">a thing clean contrary (or at least wise irksom)
  too reason, suche a thing as it greeueth a man too heere it,
  irksomnesse, fondnesse.</xpln></wordentry>
  - We can convert this into something like: Absurditie  absurdity n

# The code will look like:

* For each item:
  - stem it (maybe replace u by v throughout?)
  - count words and add to totals: 
    - categories: work, savings, self-control, cooperation
    - and the total word count
    - all per year
  - calculate the valence of words near words in these categories
    - maybe we can create a valence score after doing the glove?
  - update embeddings
    - is there a way to create embeddings without downloading everything at once?

# How to run it

* Takes about 2 hrs? to make the texts on my laptop (53K texts)
  - will need about 17G of storage too
* Google compute is $3/hr for a GPU machine. NB my free trial is over...
  - A standard cheapo computer is more like 16 cents per hour
  - 
* Could sign up to the UEA one again...
* How fast is running spacy?
  - Uh, already at about 10/minute, so not really doable on your laptop
* For Google, you'd want scripts to download the raw data

# TODO
* fastText input probably should throw away more punctuation
  - and can it cope with weird characters, and what about u/v?
* Why so much Welsh??
* Are full stops relevant? Shouldn't they be replaced by a " " anyway?
* manually check some of your texts
  - Should &amp; be replaced by "and"? or just left as it is
    (if so after deleting punctuation it would be "amp")
    - Again maybe just replace it with & and let & through punctuation.
      (other entities will be killed one hopes!)
  - Deleting margin notes as they create a lot of joined words and put
    things out of place.
* do we need to prelemmatize? fT seems pretty good at realizing
  that similarly spelled words are the same. But not always, e.g.
  good/goode; perhaps there are spelling changes over time so
  we don't want this to mislead us.
* lemmatization plan (nice resource anyway):
  - for each modern English lexeme, find fastText
  nearest neighbours which are also near by levenshtein distance
  - maybe compare with the eme approach? Maybe combine?

# DONE
  - Deleting margin notes as they create a lot of joined words and put
    things out of place.
  - <g ref="char:cmbAbbrStroke"> is usually for a ~ instead of an n
    or similar (e.g. "cou~ted"). Not sure what to do with this.
    Replace with n? Take a look at a few examples. 
    - Maybe just replace with ~ and let ~ through the punctuation filter.
    - Yeah, it's almost always n or m.