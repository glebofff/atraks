# -*- coding: utf-8 -*-
#
# Author: Stanislav Glebov <glebofff@gmail.com> 
# Created: 19/11/19
from django.core.management.base import BaseCommand
from rs_plan.apps import RsPlanConfig


class Command(BaseCommand):
    def download_file(self, url: str):
        self.stdout.write(
            f'Downloading file from {url}'
        )

    def handle(self, *args, **options):
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