"""
python manage.py etl --path_to_sqlite='db.sqlite3' --path_to_config='ETL/config.yaml'
"""
import yaml
from django.core.management.base import BaseCommand, CommandError
# from polls.models import Question as Poll

import logging
import sqlite3
from contextlib import closing
from typing import List, Any
from typing import Dict
from typing import Tuple

from ETL import data as mock_data


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class SQLiteETL:
    def __init__(self, mock_table_name: str, sqlite_table_name: str, fields_matching: Dict):
        self.mock_table_name = mock_table_name
        self.sqlite_table_name = sqlite_table_name
        self.fields_matching = fields_matching

        # поля в sqlite
        sqlite_fields_list = list(self.fields_matching.keys())

        # поля в мок данных
        self.mock_fields_list = []
        for sqlite_field in sqlite_fields_list:
            mock_field = self.fields_matching[sqlite_field]
            self.mock_fields_list.append(mock_field)

        # запрос для вставк данных в sqlite
        self.query_for_insert = self._get_query_to_insert(table_name=self.sqlite_table_name,
                                                          fields_list=sqlite_fields_list,
                                                          )

    @staticmethod
    def _get_query_to_insert(table_name: str, fields_list: List[str]) -> str:
        _raw_query_for_insert = """
            INSERT INTO {table} ({fields})
            VALUES ({fields_mask})
        """

        _fields_formatted = ",".join(fields_list)

        _field_mask_list = ['?'] * len(fields_list)
        _field_mask = ",".join(_field_mask_list)

        query_for_insert = _raw_query_for_insert.format(table=table_name,
                                                        fields=_fields_formatted,
                                                        fields_mask=_field_mask)

        return query_for_insert

    def extract(self, path_to_data) -> List[Dict]:
        """
        [
            {"id":1, "name": "name_1"},
        ]
        """

        # ОСТОРОЖНО не очевидное действие
        command_for_getting_data = f'mock_data.{self.mock_table_name}'
        data = eval(command_for_getting_data)

        return data

    def transform(self, extracted_data: List[Dict]) -> Tuple[Tuple[Any]]:
        """
        from:
            [..., {"id":1, "name": "name_1"}, ...]
        to:
            (..., (1, 'name_1'), ... )
        """
        data_to_send = []
        for line in extracted_data:
            transform_line = []
            for field in self.mock_fields_list:
                transform_line.append(line[field])
            transform_line = tuple(transform_line)
            data_to_send.append(transform_line)
        data_to_send = tuple(data_to_send)

        return data_to_send

    def load(self, sqlite_conn, data_to_send: Tuple[Tuple[Any]]) -> None:
        try:
            cur = sqlite_conn.cursor()
            cur.executemany(self.query_for_insert, data_to_send)
            sqlite_conn.commit()
        except Exception as e:
            sqlite_conn.close()
            raise e


class Command(BaseCommand):
    help = 'Migrate data from mock python file, to SQLite DB'

    def migration_config(self, path_to_conf: str):
        with open(path_to_conf, 'r') as f:
            config = yaml.safe_load(f)

        return config

    def add_arguments(self, parser):
        parser.add_argument(
            '--path_to_sqlite',
            dest='path_to_sqlite',
            help='path to sqlite DB',
            default='db.sqlite3',
            type=str,
        )
        parser.add_argument(
            '--path_to_config',
            dest='path_to_config',
            help='path to config with declare migration',
            type=str,
        )

    def handle(self, *args, **options):
        # print("Hello world")

        path_to_sqlite = options['path_to_sqlite']
        path_to_config = options['path_to_config']

        logger.info("open connection")
        with closing(sqlite3.connect(path_to_sqlite)) as con:
            config = self.migration_config(path_to_config)

            for table in config.keys():
                logger.info(f"start migration: {table}")

                logger.debug('read params from config')
                table_conf = config[table]
                sqlite_table_name = table_conf['table_matching']['sqlite']
                mock_data_name = table_conf['table_matching']['mock']
                fields_matching = table_conf['fields_matching']

                etl = SQLiteETL(mock_table_name=mock_data_name,
                                sqlite_table_name=sqlite_table_name,
                                fields_matching=fields_matching,
                                )
                logger.debug('extract')
                data = etl.extract(path_to_data='data.py')

                logging.debug('transform')
                transformed_data = etl.transform(extracted_data=data)

                logging.debug('load')
                etl.load(sqlite_conn=con, data_to_send=transformed_data)

                logger.info('migration done!\n')