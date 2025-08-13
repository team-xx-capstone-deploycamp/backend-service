FEATURE_COLUMNS = [
    "car_ID","symboling","CarName","fueltype","aspiration","doornumber","carbody",
    "drivewheel","enginelocation","wheelbase","carlength","carwidth","carheight",
    "curbweight","enginetype","cylindernumber","enginesize","fuelsystem",
    "boreratio","stroke","compressionratio","horsepower","peakrpm","citympg","highwaympg"
]

CATEGORICAL_COLUMNS = [
    "CarName","fueltype","aspiration","doornumber","carbody","drivewheel",
    "enginelocation","enginetype","cylindernumber","fuelsystem"
]

NUMERIC_COLUMNS = [c for c in FEATURE_COLUMNS if c not in CATEGORICAL_COLUMNS]
