# Hardcoded safe defaults used ONLY if we cannot introspect the trained OneHotEncoder.
# These MUST be values that actually existed during training.
FALLBACK_CATEGORY = {
    "CarName": "toyota corolla",
    "fueltype": "gas",
    "aspiration": "std",
    "doornumber": "four",
    "carbody": "sedan",
    "drivewheel": "fwd",
    "enginelocation": "front",
    "enginetype": "ohc",
    "cylindernumber": "four",
    "fuelsystem": "mpfi",
}
