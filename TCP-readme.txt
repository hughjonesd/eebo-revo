All of the files created by (or in a few cases received and modified by) the Text Creation Partnership are, as of 1 August 2020, free of all restrictions on use, re-use, modification, or distribution. Though distribution via box.com is not a perfect or permanent solution, it will serve for the moment.  You do not require an invitation to download; having the link is sufficient.

 Evans bulk files : https://umich.box.com/s/vael0mzdioctraixuglh
 ECCO bulk files: https://umich.box.com/s/7dc9b3b0f859a6b36bc2
 EEBO bulk files: https://umich.box.com/s/f3mphvepm20akwloqna2

Box may require you to create an account before accessing the files, but if so, it can be a free account, easily created. Box also automatically zips up into a single file any attempt to do a batch download of several files. Since most of the TCP 'files' are in fact zipped folders (or in some cases gzipped tarballs) that may contain a few thousand files each, you may find it best to download the corpus in chunks rather than all at once.

All of the transcriptions are available in three forms (the transcriptions themselves do not differ between these three).

(1) The files marked "P3" or "SGML" are in the original SGML in which they were created, and validate against the TCP SGML dtd 'eebo2prf.dtd.' The character encoding of these files is pure ASCII, with all non-ASCII characters represented by mnemonic character entities ('eacute' and so on), as listed in eebochar.ent, or more usefully in charmap.sgm and charmap.htm (the latter for human eyes, the former for machines). The SGML files also use a few character-based markup kludges such as "^" to indicate that the following character is superscripted, "_" to indicate that the following character is a decorated or historiated initial, and "~" to indicate that the preceding character is topped by a horizontal stroke of some kind, most commonly a nasal suspension (not, technically, a macron, but usually displayed as such). These files contain the body of the transcription only, aside from a small group of ID numbers at the head of the file (in the element IDG); they do not contain bibliographic records or headers. Aside from the lack of headers, and some incremental changes to the schema adopted during the course of the project, this version may be thought of as at least resembling TEI P3, especially the original P3-based TEI-lite. P3-ish.

(2) The files marked "TCP XML" or "P4" are derived from the SGML files and represent essentially a straightforward translation of the SGML to XML, and therefore may be thought of as TEI "P4-ish"; the actual dtd is called eebo2prf.xml.dtd. The markup is slightly more sophisticated, in that the character-based kludges "^" "_" and "~" have been removed in favor of actual markup (e.g. a SUP element in place of the "^" character). More importantly, the character encoding of the XML is UTF8 Unicode. Character entities with unicode equivalents have been converted to the appropriate codepoint, rendered in UTF8; entities with no unicode equivalent have generally been rendered as text strings within curly braces, e.g. {quod} for the Latin brevigraph "quod"; in a few cases, a look-alike Unicode character has been substituted in the interest of providing text intelligible to the reader. The same is true in the case of entities whose Unicode equivalents are ill supported by fonts or browsers. In some cases, Unicode has caught up to the TCP and characters formerly not supported by Unicode now are; the files here will eventually reflect that fact, but will always and inevitably remain a bit behind. The intent of this variety of character transformations is to supply a text that will be readily displayable, and therefore human-readable. 

Unlike the SGML files, these XML files contain not only the transcription, but a basic TEI bibliographic header, derived almost entirely from a library catalogue record via a standard transformation of MARC to TEI via a MARCxml intermediary. As they stand, the XML files invoke an extremely crude CSS stylesheet sufficient to allow them to be displayed, albeit in a rather garish way, in a modern web browser. The CSS is actually that used internally for diagnostic purposes,but should suffice to provide a minimally displayable text. Those wishing for a more sophisticated display are very welcome to do their own styling or transformation.

(3) Most, but not quite all, of the files are currently also available in a version that conforms to TEI P5. These were created by friends at Oxford, an effort led by Sebastian Rahtz, the master of TEI style sheets. They were generated from the SGML (version 1 above), take account of the headers attached to the TCP XML (version 2 above), but validate against P5 TEI_all. Such few losses as occur in the transformation are the result in part of SGML remnants in the TCP files (e.g. the native TCP files allow multiple values for the @lang attribute, whereas the @xml:lang attribute does not and therefore all values are removed), and in part on divergence between the TCP and TEI schemas, especially with regard to milestones, the relatively loose treatment of attribute values in TCP, and some differences in the content models of figure, closer, and opener. 

The "Oxford P5" version is available for all of the Evans-TCP files, all of the released ECCO-TCP files (but not for a number of unedited files that are available here on Box but were never formally released because of quality issues), all of the EEBO phase 1 files, and most of the EEBO phase 2 files (but not yet for those released by TCP after the creation of the P5 instance.)  The native home for these P5 files is on gitHub, but copies are provided hereon Box for convenience' sake. In the case of Evans, ECCO, and EEBO-1, these are simply 'snapshots' (downloads)* of the gitHub texts (accomplished via a wget batch file, supplied
here as well); in the case of EEBO-2, the files were obtained from the Oxford Text Archive and have not yet (August 2020) been posted to a gitHub repository, though discussions are under way.

Please let us know (tcp-info@umich.edu) if you have any questions about or problems with the files.

For more about the project, its history, goals, policies, etc., visit
  
    https://textcreationpartnership.org/
    
To search the texts online, visit the TCP site at the Univ of Michigan Library:

   EEBO:  https://quod.lib.umich.edu/e/eebogroup/
   Evans:  https://quod.lib.umich.edu/e/evans/
   ECCO:  https://quod.lib.umich.edu/e/ecco/
   
The EEBO texts are also available for searching, for those with access,
on the JISC historical books portal (UK only) and the ProQuest EEBO site,
https://search.proquest.com/eebo


 * There is one exception: a single file has been added to the Box snapshot,
 but has not yet been given a gitHub repo, viz., A70386.P5.xml, a misnamed 
 and misheaded file,  has been relaced with B25542.P5.xml, the same text 
 with a new name and a new header)
 
 
    

