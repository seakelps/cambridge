import csv
import datetime
from argparse import FileType

from django.utils import timezone
from django.core.management.base import BaseCommand

from campaign_finance.models import RawBankReport


class Command(BaseCommand):
    help = """Load bank reports scraped with `python download_ocpfus.py --bankreports`"""

    def add_arguments(self, parser):
        parser.add_argument(metavar='<campaign_bank_reports.csv>', dest='report_csv', type=FileType('r'))

    def handle(self, report_csv, *args, **options):
        bank_reports_csv = csv.DictReader(report_csv)

        for row in bank_reports_csv:

            d = datetime.datetime.strptime(row["ReportYear"], "%Y")

            # ocpf.us has a formatting problem
            try:
                fdate = timezone.make_aware(datetime.datetime.strptime(row["FilingDate"], "%Y-%m-%dT%H:%M:%S.%f"))
            except ValueError:
                fdate = timezone.make_aware(datetime.datetime.strptime(row["FilingDate"], "%Y-%m-%dT%H:%M:%S"))

            if d.year > 2014:
                _, created = RawBankReport.objects.get_or_create(
                    ocpf_id=row["Id"],
                    defaults=dict(
                        report_id=row["ReportId"],
                        report_type_id=row["ReportTypeId"],
                        report_type_description=row["ReportTypeDescription"],
                        cpf_id=row["CpfId"],
                        full_name_reverse=row["FullNameReverse"],
                        report_candidate_first_name=row["ReportCandidateFirstName"],
                        report_year=row["ReportYear"],
                        ending_date_display=datetime.datetime.strptime(row["EndingDateDisplay"], "%m/%d/%Y"),
                        beginning_date_display=datetime.datetime.strptime(row["BeginningDateDisplay"], "%m/%d/%Y"),
                        reporting_period=row["ReportingPeriod"],
                        filing_id=row["FilingId"],
                        filing_date=fdate,
                        filing_date_display=datetime.datetime.strptime(row["FilingDateDisplay"], "%m/%d/%Y"),
                        filing_date_short_display=datetime.datetime.strptime(row["FilingDateShortDisplay"], "%m/%d/%Y"),
                        filing_mechanism=row["FilingMechanism"],
                        is_amended=row["IsAmended"],
                        is_amendment=row["IsAmendment"],
                        amendment_reason=row["AmendmentReason"],
                        category=row["Category"],
                        receipt_total=row["ReceiptTotal"],
                        ui=row["Ui"],
                        reimbursee=row["Reimbursee"],
                        # fun times were had
                        beginning_balance_display=unstupify_ocpfus_money_column(row["BeginningBalanceDisplay"]),
                        receipt_total_display=unstupify_ocpfus_money_column(row["ReceiptTotalDisplay"]),
                        receipt_unitemized_total_display=unstupify_ocpfus_money_column(row["ReceiptUnitemizedTotalDisplay"]),
                        receipt_itemized_total_display=unstupify_ocpfus_money_column(row["ReceiptItemizedTotalDisplay"]),
                        expenditure_unitemized_total_display=unstupify_ocpfus_money_column(row["ExpenditureUnitemizedTotalDisplay"]),
                        expenditure_itemized_total_display=unstupify_ocpfus_money_column(row["ExpenditureItemizedTotalDisplay"]),
                        expenditure_total_display=unstupify_ocpfus_money_column(row["ExpenditureTotalDisplay"]),
                        ending_balance_display=unstupify_ocpfus_money_column(row["EndingBalanceDisplay"]),
                        inkind_total_display=unstupify_ocpfus_money_column(row["InkindTotalDisplay"]),
                        liability_total_display=unstupify_ocpfus_money_column(row["LiabilityTotalDisplay"]),
                        payments_display=unstupify_ocpfus_money_column(row["PaymentsDisplay"]),
                        savings_total_display=unstupify_ocpfus_money_column(row["SavingsTotalDisplay"]),
                    ))
                if created:
                    print('created')


def unstupify_ocpfus_money_column(col):
    """ don't even talk to me - kelsey
    $(100) is how accountants denote negative numbers """
    temp = col.replace("$", "").replace(",", "")
    if temp.startswith("(") and temp.endswith(")"):
        temp = temp.strip("()")
        temp = "-" + temp
    return temp
