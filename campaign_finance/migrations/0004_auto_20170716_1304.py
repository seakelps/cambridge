# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-16 17:04
from __future__ import unicode_literals

from django.db import migrations
from django.utils import timezone
import csv
import datetime


# don't even talk to me
def unstupify_ocpfus_money_column(col):
    temp = col.replace("$", "").replace(",", "")
    if temp.startswith("(") and temp.endswith(")"):
        temp = temp.strip("()")
        temp = "-" + temp
    return temp


# get 'em up
def load_initial_bank_reports(apps, schema_editor):
    rcr = apps.get_model('campaign_finance.RawBankReport')

    fp = open('campaign_finance/migrations/cambridge_bank_reports_2017-07-16.csv', 'r')
    bank_reports_csv = csv.DictReader(fp)

    for row in bank_reports_csv:

        d = datetime.datetime.strptime(row["ReportYear"], "%Y")

        # ocpf.us has a formatting problem
        try:
            fdate = timezone.make_aware(datetime.datetime.strptime(row["FilingDate"], "%Y-%m-%dT%H:%M:%S.%f"))
        except ValueError:
            fdate = timezone.make_aware(datetime.datetime.strptime(row["FilingDate"], "%Y-%m-%dT%H:%M:%S"))

        if d.year > 2014:

            try:
                rcr.objects.create(
                    ocpf_id=row["Id"],
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
                )
            except:
                import pdb
                pdb.set_trace()
                print("what")


# if we make a mistake, we can delete everything
def unload_initial_bank_reports(apps, schema_editor):
    rcr = apps.get_model('campaign_finance.RawBankReport')

    rcr.objects.all().delete()


# django migration config
class Migration(migrations.Migration):

    dependencies = [
        ('campaign_finance', '0003_rawbankreport'),
    ]

    operations = [
        migrations.RunPython(load_initial_bank_reports, reverse_code=unload_initial_bank_reports)
    ]
