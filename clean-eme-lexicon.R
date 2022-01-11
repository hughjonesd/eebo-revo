library(dplyr)
library(readr)

args <- commandArgs(trailingOnly = TRUE)
lexicon_file <- args[1]

l <- read_tsv(lexicon_file, col_names = c("word", "lexeme", 
                                                    "pos"))

counts <- l |> 
        group_by(word, lexeme) |> 
        count() 

first_choice <- counts |> 
        group_by(word) |> 
        dplyr::filter(n == max(n)) |>
        select(word, lexeme) |>
        arrange(lexeme)

write_tsv(first_choice, lexicon_file, col_names = FALSE)