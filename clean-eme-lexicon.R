library(dplyr)
library(readr)

args <- commandArgs(trailingOnly = TRUE)
lexicon_file <- args[1]

lexicon <- read_tsv(lexicon_file, col_names = c("word", "lexeme", 
                    "pos"), show_col_types = FALSE)

counts <- lexicon |> 
          group_by(word, lexeme) |> 
          count() 

first_choice <- counts |> 
                group_by(word) |> 
                dplyr::filter(n == max(n)) |>
                select(word, lexeme) |>
                arrange(lexeme)

write_tsv(first_choice, lexicon_file, col_names = FALSE)