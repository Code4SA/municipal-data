
from ...profile_data import ApiData
from ...profile_data.indicators import (
    RepairsMaintenanceSpending,
)

from . import (
    import_data,
    _IndicatorTestCase,
)
from .resources import (
    GeographyResource,
    BsheetFactsV1Resource,
    FinancialPositionFactsV2Resource,
    CapitalFactsV1Resource,
    CapitalFactsV2Resource,
)


class TestRepairsMaintenanceSpending(_IndicatorTestCase):

    def test_result(self):
        # Load sample data
        import_data(
            GeographyResource,
            'repairs_maintenance_spending/scorecard_geography.csv'
        )
        import_data(
            BsheetFactsV1Resource,
            'repairs_maintenance_spending/bsheet_facts_v1.csv'
        )
        import_data(
            FinancialPositionFactsV2Resource,
            'repairs_maintenance_spending/financial_position_facts_v2.csv'
        )
        import_data(
            CapitalFactsV1Resource,
            'repairs_maintenance_spending/capital_facts_v1.csv'
        )
        import_data(
            CapitalFactsV2Resource,
            'repairs_maintenance_spending/capital_facts_v2.csv'
        )
        # Fetch data from API
        api_data = ApiData(self.api_client, "CPT", 2019, 2019, 2019, '2019q4')
        api_data.fetch_data([
            "repairs_maintenance_v1",
            "repairs_maintenance_v2",
            "property_plant_equipment_v1",
            "property_plant_equipment_v2",
            "investment_property_v1",
            "investment_property_v2",
        ])
        # Provide data to indicator
        result = RepairsMaintenanceSpending.get_muni_specifics(api_data)
        self.assertEqual(
            result,
            {
                "result_type": "%",
                "values": [
                    {
                        "date": 2019,
                        "result": 0.98,
                        "rating": "bad"
                    },
                    {
                        "date": 2018,
                        "result": 1.08,
                        "rating": "bad"
                    },
                    {
                        "date": 2017,
                        "result": 9.01,
                        "rating": "good"
                    },
                    {
                        "date": 2016,
                        "result": 8.78,
                        "rating": "good"
                    }
                ],
                "ref": {
                    "title": "Circular 71",
                    "url": "http://mfma.treasury.gov.za/Circulars/Pages/Circular71.aspx"
                }
            },
        )
