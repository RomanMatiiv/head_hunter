import logging
from datetime import datetime
from typing import Dict, List

from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from data import mock_data
from junior_hunter.models import Company
from junior_hunter.models import Specialty
from junior_hunter.models import Vacancy


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Migrate data from mock python file, to SQLite DB'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip_company',
            dest='skip_company',
            help='bool param allow skip company migration',
            default=False,
            type=bool,
        )
        parser.add_argument(
            '--skip_specialty',
            dest='skip_specialty',
            help='bool param allow skip specialty migration',
            default=False,
            type=bool,
        )
        parser.add_argument(
            '--skip_vacancy',
            dest='skip_vacancy',
            help='bool param allow skip vacancy migration',
            default=False,
            type=bool,
        )

    def handle(self, *args, **options):
        # company
        if options['skip_company']:
            logger.info('etl company skipped')
        else:
            logger.info('etl company start')
            self.company_etl(data=mock_data.companies)

        # specialty
        if options['skip_specialty']:
            logger.info('elt specialty skipped')
        else:
            logger.info('elt specialty start')
            self.specialty_etl(data=mock_data.specialties)

        # vacancy
        if options['skip_vacancy']:
            logger.info('elt vacancy skipped')
        else:
            logger.info('etl vacancy start')
            self.vacancy_elt(data=mock_data.jobs)

    @staticmethod
    def company_etl(data: List[Dict]) -> None:
        company_to_save = []
        for company_mocked in data:
            pk = company_mocked['id']
            name = company_mocked['title']
            location = company_mocked['location']
            logo = company_mocked['logo']
            description = company_mocked['description']
            employee_count = company_mocked['employee_count']

            cur_company = Company(id=pk,
                                  name=name,
                                  location=location,
                                  logo=logo,
                                  description=description,
                                  employee_count=employee_count,
                                  )
            company_to_save.append(cur_company)

        Company.objects.bulk_create(company_to_save)

        return None

    @staticmethod
    def specialty_etl(data: List[Dict]) -> None:
        specialty_to_save = []
        for specialty_mocked in data:
            code = specialty_mocked['code']
            title = specialty_mocked['title']

            cur_speciality = Specialty(code=code,
                                       title=title,
                                       )
            specialty_to_save.append(cur_speciality)

        Specialty.objects.bulk_create(specialty_to_save)

        return None

    @staticmethod
    def vacancy_elt(data: List[Dict]) -> None:
        for job_mocked in data:
            pk = job_mocked['id']
            title = job_mocked['title']
            # specialty = job_mocked['specialty']
            # company = job_mocked['company']
            skills = job_mocked['skills']
            description = job_mocked['description']
            salary_min = job_mocked['salary_from']
            salary_max = job_mocked['salary_to']

            raw_posted = job_mocked['posted']
            raw_posted_mask = '%Y-%m-%d'
            posted = datetime.strptime(raw_posted, raw_posted_mask)
            posted_with_tz = make_aware(posted)
            published_at = posted_with_tz

            speciality_pk = job_mocked['specialty']
            speciality = Specialty.objects.get(code=speciality_pk)

            company_pk = int(job_mocked['company'])
            company = Company.objects.get(id=company_pk)

            vacancy = Vacancy(id=pk,
                              title=title,
                              specialty=speciality,
                              skills=skills,
                              description=description,
                              salary_min=salary_min,
                              salary_max=salary_max,
                              published_at=published_at,
                              )
            vacancy.save()

            vacancy.company.add(company)
            vacancy.save()

        return None