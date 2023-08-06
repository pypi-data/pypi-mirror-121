import pandas as pd

from poepp.data_processing import dump_processing


class TestDumpProcessing:
    def test_get_csv(self, data_fixtures):
        file_path = dump_processing.get_currency_file_paths(
            file_dirs=str(data_fixtures / "*.csv")
        )
        assert sorted([file.split("/")[-1] for file in file_path]) == sorted(
            [
                "test_league_currency_1.csv",
                "test_league_currency_2.csv",
            ]
        )

    def test_read_csv(self, data_fixtures):
        file_path = dump_processing.get_currency_file_paths(
            file_dirs=str(data_fixtures / "*.csv")
        )
        df = dump_processing.extract_df(file_path[0])
        assert all(df.columns == ["league", "date", "currency", "value"])
        assert df.shape == (5, 4)

    def test_get_all_data(self, data_fixtures):
        file_path = dump_processing.get_currency_file_paths(
            file_dirs=str(data_fixtures / "*.csv")
        )
        df = dump_processing.get_data(file_path)
        assert df.shape == (10, 3)
        assert df.index.equals(
            pd.to_datetime(
                [
                    "2021-01-01",
                    "2021-01-02",
                    "2021-01-03",
                    "2021-01-04",
                    "2021-01-05",
                    "2021-01-07",
                    "2021-01-08",
                    "2021-01-09",
                    "2021-01-10",
                    "2021-01-11",
                ]
            )
        )
