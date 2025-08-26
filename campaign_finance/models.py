from django.db import models
from django.db.models import Sum, Count, Max

import decimal


# information about the actual committee
class Committee(models.Model):

    # 4 fields from ocpf.us
    committee_name = models.CharField(max_length=200)
    treasurer = models.CharField(max_length=200)
    treasurer_salutation = models.CharField(max_length=200)
    committee_address = models.CharField(max_length=200)


# do we want to duplicate some of the candidate and office information?


# this is a type of report available on ocpf.us
# blame them for all column names (kept identical for comparison's sake)
class RawBankReport(models.Model):

    # identifying the report in ocpf's system
    # ocpf_id == report_id in all examples
    ocpf_id = models.IntegerField()  # "id" in ocpf.us
    report_id = models.IntegerField()
    report_type_id = models.IntegerField()
    report_type_description = models.CharField(max_length=200)

    # who this report is tied to
    cpf_id = models.IntegerField(db_index=True)
    full_name_reverse = models.CharField(max_length=200)
    report_candidate_first_name = models.CharField(max_length=200)

    # report dates
    report_year = models.IntegerField()
    ending_date_display = models.DateField(null=True, blank=True)
    beginning_date_display = models.DateField(null=True, blank=True)
    reporting_period = models.CharField(max_length=200)

    # filing
    filing_id = models.IntegerField()
    filing_date = models.DateTimeField(null=True, blank=True)
    filing_date_display = models.DateField(null=True, blank=True)
    filing_date_short_display = models.DateField(null=True, blank=True)
    filing_mechanism = models.CharField(max_length=200)

    # amendments
    is_amended = models.BooleanField(default=0)
    is_amendment = models.BooleanField(default=0)
    amendment_reason = models.CharField(max_length=200)

    # i have no idea what this is
    category = models.CharField(max_length=20)

    # moneymoneymoneymoneyMONEY
    beginning_balance_display = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_total = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_total_display = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_unitemized_total_display = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_itemized_total_display = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    expenditure_unitemized_total_display = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    expenditure_itemized_total_display = models.DecimalField(
        max_digits=10, decimal_places=2, null=True
    )
    expenditure_total_display = models.DecimalField(max_digits=10, decimal_places=2)
    ending_balance_display = models.DecimalField(max_digits=10, decimal_places=2)
    inkind_total_display = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    liability_total_display = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payments_display = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    savings_total_display = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    # these always seemed null
    ui = models.CharField(max_length=20)
    reimbursee = models.CharField(max_length=200)

    # /end bank report ocpf.us columns. phew!


# this is information from ocpf.us' "export to text"
# because ocpf.us hates us, PDF, excel, and text have different data.
# we went with text because it was the longest
class RawCampaignReceipt(models.Model):

    # who gets the money
    recipient_cpf_id = models.IntegerField()
    recipient_full_name = models.CharField(max_length=200)

    # when the money was given
    date = models.DateField(null=True, blank=True)

    # who gave the money
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=20)
    occupation = models.CharField(max_length=200)
    employer = models.CharField(max_length=200)

    # other ocpf.us stuff
    principal_officer = models.CharField(max_length=200)
    contributor_id = models.IntegerField()
    is_inkind = models.IntegerField()

    # the money
    amount = models.DecimalField(max_digits=10, decimal_places=2)


# humans entering data never goes well.
# this is the above data, but with effort on our part to, ex.,
# change "athena health" and "Athenahealth" into all the same "Athenahealth, Inc.";
# fix zipcodes that don't exist, etc.
class CleanCampaignReceipt(models.Model):

    # who gets the money
    recipient_cpf_id = models.IntegerField()
    recipient_full_name = models.CharField(max_length=200)

    # when the money was given
    date = models.DateField(null=True, blank=True)

    # who gave the money
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=20)
    occupation = models.CharField(max_length=200)
    employer = models.CharField(max_length=200)

    # other ocpf.us stuff
    principal_officer = models.CharField(max_length=200)
    contributor_id = models.IntegerField()
    is_inkind = models.IntegerField()

    # the money
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # our stuff
    occupation_type = models.CharField(max_length=200)


# potential table: cleaning operation/note


# returns either 0 if they had no 2019-1-1 report, or the # from that report
def get_candidate_money_at_start_of_2019(candidate_cpf_id):
    # jan 1 2019 report for this candidate
    try:
        bank_report = RawBankReport.objects.filter(
            cpf_id=candidate_cpf_id,
            beginning_date_display__year=2019,
            beginning_date_display__month=1,
            beginning_date_display__day=1,
        ).latest("filing_date")
    except RawBankReport.DoesNotExist:
        return 0

    return bank_report.beginning_balance_display


# all the money the candidate has spent in 2019
#
# note: if a candidate has two bank accounts, they have two bank reports...
# and transferring money from one to the other counts as a receipt/expenditure.
#
# these two functions attempt to deal with that -
# if there are are two bank reports for the same period, checks for a pair:
#   - receipt = expenditure
#   - receipt from = expenditure to
#
def get_candidate_2019_spent(candidate_cpf_id):
    agg = RawBankReport.objects.filter(
        cpf_id=candidate_cpf_id, beginning_date_display__year=2019
    ).aggregate(Sum("expenditure_total_display"))

    # check if there are 2 bank accounts during the same period ever, to try
    # to flush out bank transfers
    max_num_reports = (
        RawBankReport.objects.filter(cpf_id=candidate_cpf_id, beginning_date_display__year=2019)
        .values("beginning_date_display")
        .annotate(Count("beginning_date_display"))
        .aggregate(Max("beginning_date_display__count"))["beginning_date_display__count__max"]
        or 0
    )

    if max_num_reports > 1:
        # we might need candidate-specific hacks here, if they transfer bank accounts (ex., like Jan did in 2017)
        # this is such a hack.
        # transfer from closing bank account: $13,472.25, 4/6/2019   # http://www.ocpf.us/Reports/DisplayReport?menuHidden=true&id=606891#schedule-a
        # account closed: $13,472.25     # http://www.ocpf.us/Reports/DisplayReport?menuHidden=true&id=607350#schedule-b
        if candidate_cpf_id == 16062:
            return agg["expenditure_total_display__sum"] - decimal.Decimal("13472.25")
        else:
            print("two bank reports found for the same period! investigate! fix!")
            return None

    return agg["expenditure_total_display__sum"]


# all the money the candidate has raised in 2019
# (doesn't include money candidate started 2019 with)
def get_candidate_2019_raised(candidate_cpf_id):
    agg = RawBankReport.objects.filter(
        cpf_id=candidate_cpf_id, beginning_date_display__year=2019
    ).aggregate(Sum("receipt_total_display"))

    # check if there are 2 bank accounts during the same period ever, to try
    # to flush out bank transfers
    max_num_reports = (
        RawBankReport.objects.filter(cpf_id=candidate_cpf_id, beginning_date_display__year=2019)
        .values("beginning_date_display")
        .annotate(Count("beginning_date_display"))
        .aggregate(Max("beginning_date_display__count"))["beginning_date_display__count__max"]
        or 0
    )

    if max_num_reports > 1:
        # we might need candidate-specific hacks here, if they transfer bank accounts (ex., like Jan did in 2017)
        # this is such a hack.
        # transfer from closing bank account: $13,472.25, 4/6/2017   # http://www.ocpf.us/Reports/DisplayReport?menuHidden=true&id=606891#schedule-a
        # account closed: $13,472.25     # http://www.ocpf.us/Reports/DisplayReport?menuHidden=true&id=607350#schedule-b
        if candidate_cpf_id == 16062:
            return agg["receipt_total_display__sum"] - decimal.Decimal("13472.25")
        else:
            print("two bank reports found for the same period! investigate! fix!")
            return None

    return agg["receipt_total_display__sum"]


# yes these all need to be updated/ functionifixed


# returns either 0 if they had no 2021-1-1 report, or the # from that report
def get_candidate_money_at_start_of_2021(candidate_cpf_id):
    # jan 1 2021 report for this candidate
    try:
        bank_report = RawBankReport.objects.filter(
            cpf_id=candidate_cpf_id,
            beginning_date_display__year=2021,
            beginning_date_display__month=1,
            beginning_date_display__day=1,
        ).latest("filing_date")
    except RawBankReport.DoesNotExist:
        return 0

    return bank_report.beginning_balance_display


# all the money the candidate has spent in 2021
#
# note: if a candidate has two bank accounts, they have two bank reports...
# and transferring money from one to the other counts as a receipt/expenditure.
#
# these two functions attempt to deal with that -
# if there are are two bank reports for the same period, checks for a pair:
#   - receipt = expenditure
#   - receipt from = expenditure to
#
def get_candidate_2021_spent(candidate_cpf_id):
    agg = RawBankReport.objects.filter(
        cpf_id=candidate_cpf_id, beginning_date_display__year=2021
    ).aggregate(Sum("expenditure_total_display"))

    # check if there are 2 bank accounts during the same period ever, to try
    # to flush out bank transfers
    max_num_reports = (
        RawBankReport.objects.filter(cpf_id=candidate_cpf_id, beginning_date_display__year=2021)
        .values("beginning_date_display")
        .annotate(Count("beginning_date_display"))
        .aggregate(Max("beginning_date_display__count"))["beginning_date_display__count__max"]
        or 0
    )

    if max_num_reports > 1:
        # we might need candidate-specific hacks here, if they transfer bank accounts (ex., like Jan did in 2017)
        # this is such a hack.
        # transfer from closing bank account: $13,472.25, 4/6/2021   # http://www.ocpf.us/Reports/DisplayReport?menuHidden=true&id=606891#schedule-a
        # account closed: $13,472.25     # http://www.ocpf.us/Reports/DisplayReport?menuHidden=true&id=607350#schedule-b
        if candidate_cpf_id == 16062:
            return agg["expenditure_total_display__sum"] - decimal.Decimal("13472.25")
        else:
            print("two bank reports found for the same period! investigate! fix!")
            return None

    return agg["expenditure_total_display__sum"]


# all the money the candidate has raised in 2021
# (doesn't include money candidate started 2021 with)
def get_candidate_2021_raised(candidate_cpf_id):
    agg = RawBankReport.objects.filter(
        cpf_id=candidate_cpf_id, beginning_date_display__year=2021
    ).aggregate(Sum("receipt_total_display"))

    # check if there are 2 bank accounts during the same period ever, to try
    # to flush out bank transfers
    max_num_reports = (
        RawBankReport.objects.filter(cpf_id=candidate_cpf_id, beginning_date_display__year=2021)
        .values("beginning_date_display")
        .annotate(Count("beginning_date_display"))
        .aggregate(Max("beginning_date_display__count"))["beginning_date_display__count__max"]
        or 0
    )

    if max_num_reports > 1:
        # we might need candidate-specific hacks here, if they transfer bank accounts (ex., like Jan did in 2017)
        # this is such a hack.
        # transfer from closing bank account: $13,472.25, 4/6/2017   # http://www.ocpf.us/Reports/DisplayReport?menuHidden=true&id=606891#schedule-a
        # account closed: $13,472.25     # http://www.ocpf.us/Reports/DisplayReport?menuHidden=true&id=607350#schedule-b
        if candidate_cpf_id == 16062:
            return agg["receipt_total_display__sum"] - decimal.Decimal("13472.25")
        else:
            print("two bank reports found for the same period! investigate! fix!")
            return None

    return agg["receipt_total_display__sum"]


#
#
# Beginning of generic functions
#
#


# returns either 0 if they had no year-1-1 report, or the # from that report
def get_candidate_money_at_start_of_year(candidate_cpf_id, year=2023):
    # jan 1 2021 report for this candidate
    try:
        bank_report = RawBankReport.objects.filter(
            cpf_id=candidate_cpf_id,
            beginning_date_display__year=year,
            beginning_date_display__month=1,
            beginning_date_display__day=1,
        ).latest("filing_date")
    except RawBankReport.DoesNotExist:
        return 0

    return bank_report.beginning_balance_display


# all the money the candidate has spent in year
#
# note: if a candidate has two bank accounts, they have two bank reports...
# and transferring money from one to the other counts as a receipt/expenditure.
#
# these two functions attempt to deal with that -
# if there are are two bank reports for the same period, checks for a pair:
#   - receipt = expenditure
#   - receipt from = expenditure to
#
def get_candidate_spent_year(candidate_cpf_id, year=2023):
    agg = RawBankReport.objects.filter(
        cpf_id=candidate_cpf_id, beginning_date_display__year=year
    ).aggregate(Sum("expenditure_total_display"))

    # check if there are 2 bank accounts during the same period ever, to try
    # to flush out bank transfers
    max_num_reports = (
        RawBankReport.objects.filter(cpf_id=candidate_cpf_id, beginning_date_display__year=year)
        .values("beginning_date_display")
        .annotate(Count("beginning_date_display"))
        .aggregate(Max("beginning_date_display__count"))["beginning_date_display__count__max"]
        or 0
    )

    if max_num_reports > 1:
        # we might need candidate-specific hacks here, if they transfer bank accounts (ex., like Jan did in 2017)
        # this is such a hack.
        # transfer from closing bank account: $13,472.25, 4/6/2021   # http://www.ocpf.us/Reports/DisplayReport?menuHidden=true&id=606891#schedule-a
        # account closed: $13,472.25     # http://www.ocpf.us/Reports/DisplayReport?menuHidden=true&id=607350#schedule-b
        if candidate_cpf_id == 16062:
            return agg["expenditure_total_display__sum"] - decimal.Decimal("13472.25")
        else:
            print("two bank reports found for the same period! investigate! fix!")
            return None

    return agg["expenditure_total_display__sum"]


# all the money the candidate has raised in year
# (doesn't include money candidate started yeaer with)
def get_candidate_raised_year(candidate_cpf_id, year=2023):
    agg = RawBankReport.objects.filter(
        cpf_id=candidate_cpf_id, beginning_date_display__year=year
    ).aggregate(Sum("receipt_total_display"))

    # check if there are 2 bank accounts during the same period ever, to try
    # to flush out bank transfers
    max_num_reports = (
        RawBankReport.objects.filter(cpf_id=candidate_cpf_id, beginning_date_display__year=year)
        .values("beginning_date_display")
        .annotate(Count("beginning_date_display"))
        .aggregate(Max("beginning_date_display__count"))["beginning_date_display__count__max"]
        or 0
    )

    if max_num_reports > 1:
        # we might need candidate-specific hacks here, if they transfer bank accounts (ex., like Jan did in 2017)
        # this is such a hack.
        # transfer from closing bank account: $13,472.25, 4/6/2017   # http://www.ocpf.us/Reports/DisplayReport?menuHidden=true&id=606891#schedule-a
        # account closed: $13,472.25     # http://www.ocpf.us/Reports/DisplayReport?menuHidden=true&id=607350#schedule-b
        if candidate_cpf_id == 16062:
            return agg["receipt_total_display__sum"] - decimal.Decimal("13472.25")
        else:
            print("two bank reports found for the same period! investigate! fix!")
            return None

    return agg["receipt_total_display__sum"]
