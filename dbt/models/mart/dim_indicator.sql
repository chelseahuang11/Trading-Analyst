select
    t.$1 as series_id,
    t.$2 as name,
    t.$3 as category,
    t.$4 as unit,
    t.$5 as frequency
from (values
    ('MORTGAGE30US', '30-Year Fixed Rate Mortgage Average',                     'Mortgage Rates',    'Percent',              'Weekly'),
    ('MORTGAGE15US', '15-Year Fixed Rate Mortgage Average',                     'Mortgage Rates',    'Percent',              'Weekly'),
    ('MORTGAGE5US',  '5/1-Year ARM Average',                                    'Mortgage Rates',    'Percent',              'Weekly'),
    ('DRSFRMACBS',   'Delinquency Rate on Single-Family Residential Mortgages', 'Delinquency Rates', 'Percent',              'Quarterly'),
    ('DRSREACBS',    'Delinquency Rate on Real Estate Loans',                   'Delinquency Rates', 'Percent',              'Quarterly'),
    ('HOUST',        'Housing Starts: Total New Privately-Owned Units',         'Housing Supply',    'Thousands of Units',   'Monthly'),
    ('PERMIT',       'New Private Housing Units Authorized by Building Permits','Housing Supply',    'Thousands of Units',   'Monthly'),
    ('CSUSHPISA',    'S&P/Case-Shiller U.S. National Home Price Index',         'Home Price Index',  'Index Jan 2000=100',   'Monthly'),
    ('USSTHPI',      'All-Transactions House Price Index for the United States', 'Home Price Index',  'Index 1980 Q1=100',    'Quarterly')
) t
