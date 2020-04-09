# This is placeholder for licensing text to be added.
from numpy import nan
from sagemaker_sklearn_extension.externals import Header
from sagemaker_sklearn_extension.feature_extraction.text import MultiColumnTfidfVectorizer
from sagemaker_sklearn_extension.impute import RobustImputer
from sagemaker_sklearn_extension.preprocessing import NALabelEncoder
from sagemaker_sklearn_extension.preprocessing import RobustStandardScaler
from sagemaker_sklearn_extension.preprocessing import ThresholdOneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Given a list of column names and target column name, Header can return the index
# for given column name
HEADER = Header(
    column_names=[
        "slug", "menu", "slug.1", "categories", "distance", "name",
        "price_level", "rating", "review_count", "url", "lat", "lng", "Sp1",
        "type", "homeurl", "resource_id1", "resource_id2", "lat2", "lng2"
    ],
    target_column_name="rating"
)


def build_feature_transform():
    """ Returns the model definition representing feature processing."""

    # These features can be parsed as numeric.
    numeric = HEADER.as_feature_indices(
        ["review_count", "lat", "lng", "lat2", "lng2"]
    )

    # These features contain a relatively small number of unique items.
    categorical = HEADER.as_feature_indices(
        ["distance", "price_level", "review_count", "Sp1", "type"]
    )

    # These features can be parsed as natural language.
    text = HEADER.as_feature_indices(
        [
            "slug", "menu", "slug.1", "categories", "name", "url", "homeurl",
            "resource_id1", "resource_id2"
        ]
    )

    numeric_processors = Pipeline(
        steps=[
            (
                "robustimputer",
                RobustImputer(strategy="constant", fill_values=nan)
            )
        ]
    )

    categorical_processors = Pipeline(
        steps=[("thresholdonehotencoder", ThresholdOneHotEncoder(threshold=8))]
    )

    text_processors = Pipeline(
        steps=[
            (
                "multicolumntfidfvectorizer",
                MultiColumnTfidfVectorizer(
                    max_df=0.9622,
                    min_df=0.0023,
                    analyzer="word",
                    max_features=10000
                )
            )
        ]
    )

    column_transformer = ColumnTransformer(
        transformers=[
            ("numeric_processing", numeric_processors, numeric
            ), ("categorical_processing", categorical_processors,
                categorical), ("text_processing", text_processors, text)
        ]
    )

    return Pipeline(
        steps=[
            ("column_transformer", column_transformer
            ), ("robuststandardscaler", RobustStandardScaler())
        ]
    )


def build_label_transform():
    """Returns the model definition representing feature processing."""

    return NALabelEncoder()
