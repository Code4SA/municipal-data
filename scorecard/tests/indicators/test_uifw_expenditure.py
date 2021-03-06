
from ...profile_data import ApiData
from ...profile_data.indicators import (
    UIFWExpenditure,
)

from . import (
    import_data,
    _IndicatorTestCase,
)
from .resources import (
    GeographyResource,
    IncexpFactsV2Resource,
    IncexpFactsV1Resource,
    UIFWExpenseFactsResource,
)


class TestUIFWExpenditure(_IndicatorTestCase):

    def test_result(self):
        # Load sample data
        import_data(
            GeographyResource,
            'uifw_expenditure/scorecard_geography.csv',
        )
        import_data(
            UIFWExpenseFactsResource,
            'uifw_expenditure/uifw_expenditure_facts.csv',
        )
        import_data(
            IncexpFactsV1Resource,
            'uifw_expenditure/income_expenditure_facts_v1.csv',
        )
        import_data(
            IncexpFactsV2Resource,
            'uifw_expenditure/income_expenditure_facts_v2.csv',
        )
        # Fetch data from API
        api_data = ApiData(self.api_client, "CPT", 2019, 2019, 2019, '2019q4')
        api_data.fetch_data([
            "uifw_expenditure",
            "operating_expenditure_actual_v1",
            "operating_expenditure_actual_v2",
        ])
        # Provide data to indicator
        result = UIFWExpenditure.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "result_type": "%",
                "values": [
                    {
                        "date": 2019,
                        "result": 2.68,
                        "rating": "bad"
                    },
                    {
                        "date": 2018,
                        "result": 0.71,
                        "rating": "bad"
                    },
                    {
                        "date": 2017,
                        "result": 0.14,
                        "rating": "bad"
                    },
                    {
                        "date": 2016,
                        "result": 0,
                        "rating": "good"
                    }
                ],
                "ref": {
                    "title": "Circular 71",
                    "url": "http://mfma.treasury.gov.za/Circulars/Pages/Circular71.aspx"
                }
            },
        )
