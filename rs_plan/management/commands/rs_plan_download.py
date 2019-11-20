# -*- coding: utf-8 -*-
#
# Author: Stanislav Glebov <glebofff@gmail.com> 
# Created: 19/11/19
from django.core.management.base import BaseCommand
from rs_plan.apps import RsPlanConfig
import csv
import codecs

from django.db import connection, transaction


class CustomDialect(csv.Dialect):
    """Describe the usual properties of Unix-generated CSV files."""
    delimiter = ';'
    quotechar = '"'
    doublequote = False
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_NONE


class Command(BaseCommand):
    dialect = CustomDialect()

    @transaction.atomic
    def populate_db(self, csvdata):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                create temporary table tmpnums (
                  "pfx" char(3),
                  "beg" char(7),
                  "end" char(7),
                  "capacity" integer,
                  "operator" text,
                  "operator_id" integer,
                  "region" text,
                  "region_id" integer         
                ) on commit drop
                """
            )

            for row in csvdata:
                cursor.execute(
                    'insert into tmpnums values(%s, %s, %s, %s, %s, null, %s, null); ', row[:6]
                )

            cursor.execute(
                """
                insert into rs_plan_operator(name)
                select distinct operator from tmpnums
                where not exists (
                  select id from rs_plan_operator where name=operator
                )
                """
            )

            cursor.execute(
                """
                insert into rs_plan_region(name)
                select distinct region from tmpnums
                where not exists (
                  select id from rs_plan_region where name=region
                )
                """
            )

            cursor.execute(
                """
                update tmpnums 
                set 
                  operator_id = (select id from rs_plan_operator where name=operator),
                  region_id = (select id from rs_plan_region where name=region)
                """
            )

            cursor.execute(
                """
                insert into rs_plan_plan (pfx, beg, "end", capacity, operator_id, region_id)
                select pfx, beg, "end", capacity, operator_id, region_id from tmpnums 
                on conflict on constraint plan_unique_constraint do 
                update set capacity=excluded.capacity, operator_id=excluded.operator_id, region_id=excluded.region_id
                """
            )



    def download_file(self, url: str):
        from urllib.request import urlopen
        from urllib.error import URLError

        self.stdout.write(
            f'Downloading file from {url}'
        )
        try:
            response = urlopen(
                url
            )
            csvfile = csv.reader(codecs.iterdecode(response, 'utf-8'), self.dialect)
            self.populate_db(csvfile)

        except URLError as e:
            self.stderr.write(
                f'Error downloading {url}: {e.reason}'
            )

    def handle(self, *args, **options):
        self.dialect.delimiter = options.get('delimiter', ";")
        for p in options['prefixes']:
            self.download_file(
                RsPlanConfig.get_file_url(url=options['url'], prefix=p)
            )

    def add_arguments(self, parser):
        parser.add_argument(
            '-u',
            '--url',
            type=str,
            default=RsPlanConfig.base_url
        )

        parser.add_argument(
            '-p',
            '--prefixes',
            type=list,
            default=RsPlanConfig.prefixes
        )

        parser.add_argument(
            '-d',
            '--delimiter',
            type=str,
            default=RsPlanConfig.delimiter
        )
