import os
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from ...party import PartyImporter
from ...member import MemberImporter
from ...minutes import MinutesImporter
from ...vote import VoteImporter
from ...seat import SeatImporter
from ...funding import FundingImporter
from ...doc import DocImporter
from utils.http import HttpFetcher

class Command(BaseCommand):
    #args = '<poll_id poll_id ...>'
    help = 'Import data from the Finnish parliament'
    option_list = BaseCommand.option_list + (
        make_option('--party', action='store_true', dest='party',
                    default=False, help='Import parties'),
        make_option('--member', action='store_true', dest='member',
                    default=False, help='Import MPs'),
        make_option('--seat', action='store_true', dest='seat',
                    default=False, help='Import MP seatings'),
        make_option('--minutes', action='store_true', dest='minutes',
                    default=False, help='Import plenary session minutes'),
        make_option('--docs', action='store_true', dest='docs',
                    default=False, help='Import parliament documents'),
        make_option('--vote', action='store_true', dest='vote',
                    default=False, help='Import plenary session votes'),
        make_option('--funding', action='store_true', dest='funding',
                    default=False, help='Import election funding'),
        make_option('--update', action='store_true', dest='update',
                    default=False, help='Update values of existing objects'),
        make_option('--cache', action='store', dest='cache',
                    help='Use cache in supplied director')
    )

    def handle(self, *args, **options):
        http = HttpFetcher()
        if options['cache']:
            http.set_cache_dir(options['cache'])
        min_importer = MinutesImporter(http_fetcher=http)
        min_importer.replace = options['update']
        min_importer.import_terms()

        if options['party']:
            importer = PartyImporter(http_fetcher=http)
            importer.replace = options['update']
            importer.import_parties()
        if options['member']:
            importer = MemberImporter(http_fetcher=http)
            importer.replace = options['update']
            importer.import_districts()
            importer.import_members()
        if options['seat']:
            importer = SeatImporter(http_fetcher=http)
            importer.replace = options['update']
            importer.import_seats()
        if options['minutes']:
            min_importer.import_minutes()
        if options['docs']:
            importer = DocImporter(http_fetcher=http)
            importer.replace = options['update']
            importer.import_docs()
        if options['vote']:
            importer = VoteImporter(http_fetcher=http)
            importer.replace = options['update']
            importer.import_votes()
        if options['funding']:
            importer = FundingImporter(http_fetcher=http)
            importer.replace = options['update']
            importer.import_funding()