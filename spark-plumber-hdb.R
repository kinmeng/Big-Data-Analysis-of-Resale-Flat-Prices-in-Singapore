# spark-plumber.R

library(sparklyr); library(dplyr)

sc <- spark_connect(master = "local", version = "3.0.0")

spark_model <- ml_load(sc, path = "spark_model_hdb")

#* @post /predict
function(floor_area_sqm, remaining_lease_std, dist_to_central, dist_nearest_mall, dist_nearest_mrt, flat_model, storey_range){
  new_data <- data.frame(
    floor_area_sqm = as.double(floor_area_sqm),
    remaining_lease_std = as.integer(remaining_lease_std),
    dist_to_central = as.double(dist_to_central),
    dist_nearest_mall = as.double(dist_nearest_mall),
    dist_nearest_mrt = as.double(dist_nearest_mrt),
    flat_model = as.character(flat_model),
    storey_range = as.character(storey_range),
    resale_price = NA
  )
  
  new_data_r <- copy_to(sc, new_data, overwrite = TRUE)
  
  ml_transform(spark_model, new_data_r) |>
    pull(prediction)
}