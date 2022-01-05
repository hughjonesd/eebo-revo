
# Ideas

## Implicit and explicit levels in text

Try and distinguish levels: "implicit" and "explicit" associations. E.g. implicit associations might
measure associations of ethnic group or gender with professions, via distance in a word 
embedding model.

Explicit associations would be what texts explicitly say about e.g. "black people" or "women".

One research question: do explicit associations *cause* implicit associations to change?
* Problem: how do we know that a particular explicit statement is causal?
  - Look for very influential statements? (State of Union addresses?)
  - Maybe mapping neo-ngrams would help. E.g. if there is a neo-ngram which starts in book X,
    then appears elsewhere, I can create an "influence graph". If there are enough neongrams,
    I can maybe have a tree (X influenced Y, evidenced by neongram N; Y influenced Z, evidenced by M). 
    - Key problem: how do I know the "first text" was truly the first? Could I validate by    
      looking for explicit citations? 

* Actually the citation network seems like a useful source of "ground truth" for 
  influence, within academia
    - though, is it *real* influence in the sense that "without X, Y would have been different?"
    - Anyway, one approach is to start by showing that in academic papers, you can predict the
    "ground truth" of citation networks by using neongrams
    - Then you can use neongrams to map out influences in history.
    - But you still have the "first text" issue except for a few really famous quotations ("It
    is a truth universally acknowledged...", "Once more unto the breach....", "Here stand I...")
    So in a way, all you can say is that if X and Y share a neongram, then they have a common
    ancestor, and if you can date the neongram you may be able to say they have a recent common
    ancestor.

Another: are explicit and implicit associations different (in a substantively important way)?
Another: what causes implicit associations?
* Two candidates: past associations; and reality.
* E.g. does something like the crack epidemic change associations between ethnicity and crime
  in the US? Claim needs to be that "crack epidemic" or whatever is an exogenous shock which
  isn't itself caused by cultural associations.
* It seems likely that *some* real world changes cause *some* shift in associations, but can
  we say how big or primary that effect is?


## Venues

* Are there substantial differences between media in terms of associations?
* If so, which affect which? 
  - See above on neongrams


## The Disruption

* Did the Great Disruption have a cultural aspect?
  - Across e.g. countries, or US states, does cultural change predict crime, family  
    breakdown, drug abuse?
    - Look at something like "want" vs "ought", or changes in valence to e.g. marriage
  - If it does predict that, how can we identify causality?
    - Just showing that we can predict the changes before they happen (e.g. in the 1950s?)
      would be interesting, but causality would be better

## The Industrious Revolution

* Was there a change in the valence of labour before the C18? If so, when?
* Alt hypoth: a change in the valence of cooperation?

Can look at valence of words, frequency of words, and associations of words.
Need corpuses from relevant time periods - maybe from 1400s onwards
And from relevant places. Germany, Switzerland, Holland, UK, Sweden; comparisons btw Lutheran/Cath/Calvinist?
Comparisons with eg France, Italy, Spain? 

* Do we make a link with economic outcomes? 
  - What would be the instrument? Printing presses?
  - Protestant printers?
  - Could we find which individuals had what texts? Then you also need to know who the individuals were
    - E.g. via inventories
  


Outcomes: size of towns in e.g. Germany? Look at whatsisface. Time use? But how link to books?
* We could at least do time-series analysis.
* Or, the answer is go to the C19 America and use newspapers.
  - US censuses have details of employment, esp in IPUMS, from 1850 on.
  - Whaples 1990 looked at employment hours in C19. He gives estimates for 100 industries and 300 cities. "Eastern Europeans worked longer hours while foreign-born worked shorter".
Time use, see Voth, H.J., 1998. Time and work in eighteenth-century London. Journal of Economic History, pp.29-58.
  - He uses court data. Presumably there are different courts. He focuses on London only.
For the US going back to 1900, see
Ramey, V.A. and Francis, N., 2009. A century of work and leisure. American Economic Journal: Macroeconomics, 1(2), pp.189-224.
  - Before WWII they use Kendrick "Productivity Trends in the United States"
  - 
