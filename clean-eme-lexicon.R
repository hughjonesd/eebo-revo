library(dplyr)
library(readr)

args <- commandArgs(trailingOnly = TRUE)
lexicon_file <- args[1]

l <- read_tsv(lexicon_file, col_names = c("word", "lexeme", 
                                                    "pos"))

counts <- l |> 
        group_by(word, lexeme) |> 
        count() |> 
        group_by(word) |> 
        dplyr::filter(n == max(n)) 

write_tsv(counts, lexicon_file, col_names = FALSE)