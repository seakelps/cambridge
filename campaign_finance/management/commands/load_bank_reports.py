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

            d = datetime.datetime.strptime(row["reportYear"], "%Y")

            # ocpf.us has a formatting problem
            fdate = timezone.make_aware(datetime.datetime.strptime(row["dateFiled"], "%m/%d/%Y"))
            start_date = row['reportingPeriod'].split(' - ')[0]

            if d.year > 2014:
                _, created = RawBankReport.objects.get_or_create(
                    ocpf_id=row["id"],
                    defaults=dict(
                        report_id=row["reportId"],
                        report_type_id=row["reportTypeId"],
                        report_type_description=row["reportTypeDescription"],
                        cpf_id=row["cpfId"],
                        # full_name_reverse=row["fullNameReverse"],
                        # report_candidate_first_name=row["ReportCandidateFirstName"],
                        report_year=row["reportYear"],
                        # ending_date_display=datetime.datetime.strptime(row["EndingDateDisplay"], "%m/%d/%Y"),
                        beginning_date_display=datetime.datetime.strptime(start_date, "%m/%d/%Y"),
                        reporting_period=row["reportingPeriod"],
                        filing_id=row["id"],
                        filing_date=datetime.datetime.combine(fdate, datetime.time(0)),
                        filing_date_display=fdate,
                        # filing_date_short_display=datetime.datetime.strptime(row["FilingDateShortDisplay"], "%m/%d/%Y"),
                        filing_mechanism=row["filingMechanism"],
                        is_amended=row["isAmended"],
                        is_amendment=row["isAmendment"],
                        amendment_reason=row["amendmentReason"],
                        # category=row["category"],
                        receipt_total=unstupify_ocpfus_money_column(row["creditTotal"]),
                        # ui=row["Ui"],
                        # reimbursee=row["Reimbursee"],
                        # fun times were had
                        beginning_balance_display=unstupify_ocpfus_money_column(row["startBalance"]),
                        receipt_total_display=unstupify_ocpfus_money_column(row["creditTotal"]),
                        receipt_unitemized_total_display=unstupify_ocpfus_money_column(row["filerReportedDepositReceiptUnitemizedTotal"]),
                        # receipt_itemized_total_display=unstupify_ocpfus_money_column(row["filerReportedDepositReceiptItemizedTotal"]),  all zeros
                        # expenditure_unitemized_total_display=unstupify_ocpfus_money_column(row["filerReportedDepositExpenditureUnitemizedTotal"]),
                        # expenditure_itemized_total_display=unstupify_ocpfus_money_column(row["filerReportedDepositExpenditureItemizedTotal"]),
                        expenditure_total_display=unstupify_ocpfus_money_column(row["expenditureTotal"]),
                        ending_balance_display=unstupify_ocpfus_money_column(row["endBalance"]),

                        # inkind_total_display=unstupify_ocpfus_money_column(row["InkindTotalDisplay"]),
                        # liability_total_display=unstupify_ocpfus_money_column(row["LiabilityTotalDisplay"]),
                        # payments_display=unstupify_ocpfus_money_column(row["PaymentsDisplay"]),
                        # savings_total_display=unstupify_ocpfus_money_column(row["SavingsTotalDisplay"]),
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
