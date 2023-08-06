import typing as tp
import warnings

import pandas as pd


def quantizer(score):
    """
    Quantizes scores with desired range

    Run with:
        df[col] = df[col].apply(lambda x: quantizer(x))
            to transform column into quantized values (or set to new column)

    Args:
        score: float

    Returns:
        category string
    """
    if score >= 0.99:
        return "very_high"
    elif score >= 0.9:
        return "high"
    elif score >= 0.7:
        return "moderate"
    elif score >= 0.5:
        return "low"
    else:
        return "very_low"


def create_aggregations(annotations: tp.Sequence[tp.Dict]) -> tp.Dict:
    """Given a sequence of annotation dicts, create aggregations for them.

    Args:
        annotations (tp.Sequence[tp.Dict]): The sequence of annotations to aggregate.

    Raises:
        ValueError:

    Returns:
        tp.Dict: The aggregated output.
    """
    df_annotations = pd.DataFrame(annotations)
    # Take score_id (score for concept_id) and convert to category string
    df_annotations["concept_score_category"] = df_annotations["score_id"].apply(lambda x: quantizer(x))
    # Take score_type (score for concept_type) and convert to category string
    df_annotations["type_score_category"] = df_annotations["score_type"].apply(lambda x: quantizer(x))
    # Convert concept types names to be more API friendly, lowercase and without spaces
    df_annotations["concept_type"] = df_annotations["concept_type"].str.lower().str.replace(' ', '_')

    agg_concepts = aggregate_concept(df_annotations)
    agg_types = aggregate_concept_type(df_annotations)
    agg_scores = aggregate_concept_score_category(df_annotations)

    aggregations = {
        "concepts": shape_aggregation(
            agg=agg_concepts,
            orient='records'
        ),
        "concept_types": shape_aggregation(
            agg=agg_types,
            orient='index',
            index='concept_type'
        ),
        "concept_score_categories": shape_aggregation(
            agg=agg_scores,
            orient='keyval',
            keyval=('concept_score_category', 'count_annotations')
        )
    }

    return aggregations


def aggregate_concept(annotations: pd.DataFrame) -> pd.DataFrame:
    """Aggregate concept information.

    This function aggregates all necessary information related
    to a concept. The rows in the agg dataframe are sorted by
    the count of annotations for each concept.

    Args:
        annotations: pd.DataFrame with annotations/spans from KEPLER

    Returns:
        pd.DataFrame:
            concept_name: str
            concept_id: str
            count_annotations: int
            concept_score_average: float
            texts: list(str)
            concept_scores: list(float)
            concept_type: list(str)
    """
    # Get count of annotations and average score per concept
    counts = annotations.groupby(['concept_name', 'concept_id'], as_index=False) \
        .agg({'text': 'count', 'score_type': 'mean'}) \
        .rename(columns={'text': 'count_annotations', 'score_type': 'concept_score_average'}) \
        .sort_values(['count_annotations', 'concept_score_average'], ascending=False) \
        .reset_index(drop=True)

    # get list of concept_types per concept
    #    note we apply set and then list to get list of unique values
    types = annotations.groupby(['concept_id', 'concept_name']) \
        ['concept_type'].apply(set).apply(list) \
        .reset_index(name='concept_type')

    # get list of texts per concept
    #    note we apply set and then list to get list of unique values
    texts = annotations.groupby(['concept_id', 'concept_name']) \
        ['text'].apply(set).apply(list) \
        .reset_index(name='texts')

    # get list of concept_scores per concept
    scores = annotations.groupby(['concept_id', 'concept_name']) \
        ['score_type'].apply(list) \
        .reset_index(name='concept_scores')

    # now merge all the dataframes to form the aggregation
    agg = counts
    for df_ in [texts, scores, types]:
        agg = agg.merge(df_, on=['concept_name', 'concept_id'])

    return agg


def aggregate_concept_type(annotations: pd.DataFrame, sort_by: str=None) -> pd.DataFrame:
    """Aggregate count of annotations and concepts per concept type.

    This function counts the number of annotations and unique concepts
    for each concept_type in the annotations response. If desired,
    one can use 'sort_by' to specify a field to sort by, either
    'count_annotations' or 'count_concepts'.

    Args:
        annotations: pd.DataFrame with annotations/spans from KEPLER
        sort_by:     field to sort by ('count_annotations' or 'count_concepts')

    Returns:
        pd.DataFrame:
            concept_type: str
            count_annotations: int
            count_concepts: int
    """
    # groupby concept_type
    #     aggregate by 'text' for count_annotations, 'concept_id' for count_concepts
    #    rename columns for response
    agg = annotations.groupby(['concept_type'], as_index=False) \
        .agg({'text': 'count', 'concept_id': 'count'}) \
        .rename(columns={'text': 'count_annotations', 'concept_id': 'count_concepts'})

    # if sorting, sort by 'sort_by'
    if sort_by:
        agg = agg.sort_values(sort_by, ascending=False).reset_index(drop=True)

    return agg


def aggregate_concept_score_category(annotations: pd.DataFrame) -> pd.DataFrame:
    """ Count the number of annotations per concept score category.

    This function counts the number of annotations belong
    to each category of concept_score. If certain categories
    are not in the annotations, they are added here with
    a zero value, so they can be included in a 'keyval'
    aggregation shape.

    Args:
        annotations: pd.DataFrame with annotations/spans from KEPLER

    Returns:
        pd.DataFrame:
            concept_score_category: str
            count_annotations: int
    """
    # groupby concept_score_category
    #    aggregate by 'text' to count annotations
    #    rename columns for response
    agg = annotations.groupby('concept_score_category', as_index=False) \
        .agg({'text': 'count'}) \
        .rename(columns={'text': 'count_annotations'}) \
        .sort_values(by='count_annotations', ascending=False)

    # if a key is missing, add with count=0
    for csc in ['very_high', 'high', 'moderate', 'low', 'very_low']:
        if csc not in agg['concept_score_category'].values:
            agg = agg.append({'concept_score_category': csc, 'count_annotations': 0}, ignore_index=True)

    return agg


def shape_aggregation(agg: pd.DataFrame, orient: str = 'dict', index: str = None,
                        keyval: tuple = None) -> dict:
    """Take an agg and shape it into the appropriate dict.

    This function is a monad that should be able to take any aggregation,
    shape it as a dictionary, and provide it to the class.
    It follows the style of pd.DataFrame.to_dict with two exceptions:
    1. We add the custom 'keyval' orient which lets you specify
    two columns in the agg dataframe to generate a simple key-value dict.
    2. If using orient='index' or orient='keyval', additional args
    can be used to specify the index or key-value columns. Else, the
    function will use defaults, as described in the if/else flow below.

    Args:
        agg:    pd.DataFrame that is an aggregation of annotations
        orient: desired orientation for the response (from pd.DataFrame.to_dict)
                if 'index', must include 'how' or will assume to use first_col
                can also use 'keyval' which returns a dict(zip(...)) of two columns
        index:  the name of column to use as index for orient='index'
        keyval: the names of columns to use as key and value for orient='keyval'

    Returns:
        A dict of the aggregation in the proper shape.

    Raises:
        ValueError: orient not properly specified.
    """
    # check that orient is valid
    valid_orientations = ['dict', 'list', 'series', 'split', 'records', 'index', 'keyval']
    if orient not in valid_orientations:
        raise ValueError(f"Invalid orient variable '{orient}'. Use one of: {valid_orientations}")

    # handle the complex 'index' case
    if orient == 'index':
        # if not specified, assume first column BUT inform the developer
        if not index:
            index = agg.columns[0]
            warnings.warn(
                f"""WARNING: Index not specified. Using first column: '{index}'.
                Specify the column to use as an index with `index='x'`"""
            )
        return agg.set_index(index).to_dict('index')

    # if using custom 'keyval' orient
    elif orient == 'keyval':
        if not keyval:
            keyval = (agg.columns[0], agg.columns[1])
            warnings.warn(
                f"""WARNING: Key and value not specified.
                Using first column '{keyval[0]}' as key and second column '{keyval[1]}' as value.
                Specify the column to use as an index with `keyval=('x','y')`"""
            )
        return dict(zip(agg[keyval[0]], agg[keyval[1]]))

    # else simply use to_dict()
    else:
        return agg.to_dict(orient)
