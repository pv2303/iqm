## ODS 2.1 - Obesidade infantil (%)
## Percentual de crianças entre 0 e 5 anos classificadas com obesidade (relação peso x altura)

# Libraries --------
library(httr)
library(tidyverse)
library(jsonlite)

api <- 'https://apidadosabertos.saude.gov.br/sisvan/estado-nutricional'

# parameters
params <- list(
  idade_minima = 0,
  idade_maxima = 5,
  ano_mes_competencia = '201801',
  limit = 100,
  offset = 0
)

df <- list()

# loop through pages

while (TRUE) {
  # request API
  response <- httr::GET(api, query = params)

  # Check response status
  if (status_code(response) == 200) {
  # Parse JSON content
  content_json <- content(response, as = "text")
  content_df <- fromJSON(content_json, flatten = TRUE)

  # check if data is empty 
  if (length(content_df) == 0) break

  # append df
  df <- append(df, list(content_df))

  # increment offset for the next page
  params$offset <- params$offset + params$limit
    
  } else {
  print(paste("Error:", status_code(response)))
  }
}

df_final <- dplyr::bind_rows(df) %>% 
  as_tibble()
