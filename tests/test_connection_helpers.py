import pandas as pd
import pytest
from connection import get_latest_value, filter_by_category


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'observation_date': pd.to_datetime([
            '2023-01-01', '2023-06-01', '2023-12-01', '2023-01-01'
        ]),
        'series_id': ['MORTGAGE30US', 'MORTGAGE30US', 'MORTGAGE30US', 'DRSFRMACBS'],
        'indicator_name': ['30Y Rate', '30Y Rate', '30Y Rate', 'SF Delinquency'],
        'indicator_category': [
            'Mortgage Rates', 'Mortgage Rates', 'Mortgage Rates', 'Delinquency Rates'
        ],
        'unit': ['Percent', 'Percent', 'Percent', 'Percent'],
        'value': [6.5, 7.0, 7.5, 2.1],
    })


def test_get_latest_value_returns_most_recent(sample_df):
    result = get_latest_value(sample_df, 'MORTGAGE30US')
    assert result == 7.5


def test_get_latest_value_unknown_series_returns_none(sample_df):
    result = get_latest_value(sample_df, 'NONEXISTENT')
    assert result is None


def test_filter_by_category_returns_matching_rows(sample_df):
    result = filter_by_category(sample_df, 'Mortgage Rates')
    assert len(result) == 3
    assert all(result['indicator_category'] == 'Mortgage Rates')


def test_filter_by_category_no_match_returns_empty(sample_df):
    result = filter_by_category(sample_df, 'Nonexistent')
    assert result.empty
