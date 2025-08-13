import logging
import pickle
from functools import lru_cache
from typing import List, Dict, Any, Optional, Tuple

import numpy as np
import pandas as pd
from importlib.metadata import version as pkg_version

from app.core.config import settings
from app.services.columns import FEATURE_COLUMNS, CATEGORICAL_COLUMNS, NUMERIC_COLUMNS
from app.services.fallbacks import FALLBACK_CATEGORY

logger = logging.getLogger(__name__)

# ------------------------
# Model loading
# ------------------------
@lru_cache(maxsize=1)
def load_model():
    # WARNING: Only load trusted pickle files.
    logger.info("Loading model from %s", settings.model_path)
    try:
        logger.info(
            "Runtime versions: sklearn=%s, xgboost=%s, numpy=%s",
            _safe_version("scikit-learn"),
            _safe_version("xgboost"),
            _safe_version("numpy"),
        )
    except Exception:
        # ignore version logging errors
        pass

    with open(settings.model_path, "rb") as f:
        return pickle.load(f)

def _safe_version(pkg: str) -> str:
    try:
        return pkg_version(pkg)
    except Exception:
        return "not-installed"

# ------------------------
# Introspection helpers (to read OHE categories from your fitted pipeline)
# ------------------------
def _walk_estimators(obj):
    """Yield nested estimators (Pipeline, ColumnTransformer, etc.)."""
    try:
        from sklearn.pipeline import Pipeline
        from sklearn.compose import ColumnTransformer
    except Exception:
        yield obj
        return

    yield obj

    # Pipeline
    if hasattr(obj, "steps") and isinstance(getattr(obj, "steps"), list):
        for _, step in obj.steps:
            yield from _walk_estimators(step)

    # ColumnTransformer
    if hasattr(obj, "transformers_"):
        for _, trans, _cols in obj.transformers_:
            yield from _walk_estimators(trans)

def _find_ct_and_ohe(model) -> Optional[Tuple[object, object, List]]:
    """
    Return (column_transformer, one_hot_encoder, categorical_columns_used) if found.
    """
    try:
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
    except Exception:
        return None

    for est in _walk_estimators(model):
        # ColumnTransformer
        if hasattr(est, "transformers_"):
            for _, trans, cols in est.transformers_:
                if trans is None or trans == "drop":
                    continue
                # OHE directly
                if hasattr(trans, "categories_"):
                    return (est, trans, list(cols) if hasattr(cols, "__iter__") else [cols])
                # OHE inside a Pipeline
                if hasattr(trans, "steps"):
                    for _, step in trans.steps:
                        if hasattr(step, "categories_"):
                            return (est, step, list(cols) if hasattr(cols, "__iter__") else [cols])
    return None

@lru_cache(maxsize=1)
def _allowed_categories_map() -> Dict[str, List]:
    """
    Map {categorical_column_name: [allowed_values,...]} from the fitted OHE.
    Empty dict if we can’t introspect (we’ll fall back to hardcoded defaults).
    """
    model = load_model()
    found = _find_ct_and_ohe(model)
    if not found:
        return {}
    _, ohe, cols = found
    cats = getattr(ohe, "categories_", None)
    if cats is None:
        return {}
    col_names = [str(c) for c in cols]
    return {name: list(cat_list) for name, cat_list in zip(col_names, cats)}

# ------------------------
# DataFrame builders with coercion
# ------------------------
def _coerce_categoricals(row: Dict[str, Any]) -> None:
    allowed_map = _allowed_categories_map()
    for c in CATEGORICAL_COLUMNS:
        val = row.get(c, None)
        if c in allowed_map and len(allowed_map[c]) > 0:
            # If missing or unseen, coerce to FIRST known training category
            if (val is None) or (val not in set(allowed_map[c])):
                row[c] = allowed_map[c][0]
        else:
            # No introspection available → use hardcoded safe default if present
            if (val is None) or (val == ""):
                if c in FALLBACK_CATEGORY:
                    row[c] = FALLBACK_CATEGORY[c]

def _df_from_record(record: Dict[str, Any]) -> pd.DataFrame:
    row: Dict[str, Any] = {col: None for col in FEATURE_COLUMNS}
    for k, v in record.items():
        if k in row:
            row[k] = v

    # Coerce categoricals to known/seen categories
    _coerce_categoricals(row)

    # Numerics: leave as NaN (so a pipeline imputer can handle them). Coerce strings to numbers.
    for c in NUMERIC_COLUMNS:
        row[c] = pd.to_numeric(row[c], errors="coerce")

    return pd.DataFrame([row], columns=FEATURE_COLUMNS)

def _df_from_list(features: List[Any]) -> pd.DataFrame:
    if len(features) != len(FEATURE_COLUMNS):
        raise ValueError(f"Expected {len(FEATURE_COLUMNS)} features, got {len(features)}.")
    df = pd.DataFrame({col: [val] for col, val in zip(FEATURE_COLUMNS, features)}, columns=FEATURE_COLUMNS)
    # Apply same categorical coercion
    coerced = df.iloc[0].to_dict()
    _coerce_categoricals(coerced)
    for k, v in coerced.items():
        df.at[0, k] = v
    # Coerce numerics
    for c in NUMERIC_COLUMNS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

# ------------------------
# Public API
# ------------------------
def predict(features: Optional[List[Any]] = None, record: Optional[Dict[str, Any]] = None) -> List[float]:
    model = load_model()
    if record is not None:
        X = _df_from_record(record)
    elif features is not None:
        X = _df_from_list(features)
    else:
        raise ValueError("Provide either 'record' or 'features'.")

    try:
        y = model.predict(X)
    except AttributeError as e:
        # Make the sklearn/xgboost compatibility failure obvious
        if "__sklearn_tags__" in str(e):
            raise RuntimeError(
                "Estimator compatibility error (missing __sklearn_tags__). "
                f"Check your versions: sklearn={_safe_version('scikit-learn')}, "
                f"xgboost={_safe_version('xgboost')}. "
                "Pin them to match the training environment."
            ) from e
        raise
    return np.asarray(y).ravel().tolist()
