library(clusterProfiler)
library(org.Hs.eg.db)
library(org.Mm.eg.db)
library(tidyverse)

commandArgs(trailingOnly = TRUE)[1] -> job_id

# setwd(paste0("../WebFrontEnd/",job_id))
job_folder <- commandArgs(trailingOnly = TRUE)[1]
setwd(job_folder)


read_tsv("species.txt", col_names="species") |> pull(species) -> species

read_tsv("query_genes.txt",col_names="query") |>
    pull(query) -> query

read_tsv("background_genes.txt",col_names="background") |>
    pull(background) -> background

case_when(
    str_detect("Human",species) ~ org.Hs.eg.db,
    str_detect("Mouse",species) ~ org.Mm.eg.db,
    TRUE ~ NULL
) -> org_db

enrichGO(
    query,
    OrgDb = org.Mm.eg.db,
    keyType = "SYMBOL",
    universe = background,
    ont = "BP",
    minGSSize = 10,
    maxGSSize = 200,
    readable = TRUE
) -> enrichgo_results


