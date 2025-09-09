library(clusterProfiler)
library(org.Hs.eg.db)
library(org.Mm.eg.db)
library(tidyverse)

commandArgs(trailingOnly = TRUE)[1] -> job_id

setwd(paste0("../WebFrontEnd/",job_id))

read_tsv("species.txt", col_names="species") |> pull(species) -> species

read_tsv("query_genes.txt",col_names="query") |>
    pull(query) -> query

read_tsv("background_genes.txt",col_names="background") |>
    pull(background) -> background

org_db <- NULL

if (str_detect("Human",species)) {
    org_db = org.Hs.eg.db
}

if (str_detect("Mouse",species)) {
    org_db = org.Mm.eg.db
}

if (len(background) == 0) {
    enrichGO(
        query,
        OrgDb = org.Mm.eg.db,
        keyType = "SYMBOL",
        ont = "BP",
        minGSSize = 10,
        maxGSSize = 200,
        readable = TRUE
) -> enrichgo_results

}
else {
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
}

enrichgo_results@result |>
    as_tibble() |>
    filter(p.adjust < 0.05) |>
    filter(FoldEnrichment > 1) |>
    arrange(p.adjust) -> enrichgo_results

enrichgo_results |>
    write_tsv("cluster_profiler_result.tsv")

enrichgo_results |>
    select(ID) |>
    write_tsv("go_ids.txt")



