from collections import namedtuple

HtmlSource = namedtuple('HtmlSource', ['id', 'Filename', 'Html', 'Dt'])

Fund = namedtuple('Fund', ['id', 'Code', 'Title', 'BankId', 'TypeId', 'CreatedOn'])
FundValue = namedtuple('FundValue', ['id', 'Code', 'Dt', 'FundId', 'Currency', 'UnitSharePrice','RiskLevel', 'DailyReturn', 'MonthlyReturn', 'ThreeMonthReturn', 'FromNewYear', 'Description'])
FundValueDuplicate = namedtuple('FundValue', ['Code', 'FundId', 'Dt', 'UnitSharePrice', 'Count'])

Bank = namedtuple('Bank', ['id', 'Title', 'EFTCode', 'Tel', 'Fax', 'Address', 'Web', 'Description', 'AddedOn', 'LastUpdated'])
