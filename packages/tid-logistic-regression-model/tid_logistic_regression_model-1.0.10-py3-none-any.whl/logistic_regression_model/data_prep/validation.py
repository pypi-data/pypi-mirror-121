# this file is used to validate the features for the make_prediction function in predict.py

from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """ Validate features and returns  validated testing dataset and any errors"""
    validated_data = input_data
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleHeadlinesInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class HeadlinesInputSchema(BaseModel):
    Headline: Optional[str]


class MultipleHeadlinesInputs(BaseModel):
    inputs: List[HeadlinesInputSchema]
