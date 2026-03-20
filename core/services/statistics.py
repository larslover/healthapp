from django.db.models import Count, Case, When, IntegerField, Value, Q, F
from django.db.models.functions import ExtractYear
from datetime import date

from core.models import Screening, ScreeningCheck


def get_screening_statistics(
    *,
    academic_year,
    school_id=None,
    class_section=None,
):
    """
    Centralized statistics engine for dashboard & reports.
    Combines Screening and ScreeningCheck data.
    """

    # ---- BASE QUERYSET ----
    qs = Screening.objects.filter(academic_year=academic_year)

    if school_id:
        qs = qs.filter(student__school_id=school_id)

    if class_section:
        qs = qs.filter(class_section=class_section)

    qs = qs.select_related("student", "student__school")

    # =====================================
    # ✅ DYNAMIC AGE (FROM DOB)
    # =====================================
    today = date.today()

    qs = qs.annotate(
        age_years=ExtractYear(Value(today)) - ExtractYear(F("student__date_of_birth"))
    )

    # ---- HEADLINE NUMBERS ----
    total_screenings = qs.count()
    total_students = qs.values("student_id").distinct().count()
    total_schools = qs.values("student__school_id").distinct().count()

    # =====================================
    # ✅ AGE KPIs (FIXED)
    # =====================================
    age_2_5 = qs.filter(age_years__gte=2, age_years__lt=5).count()
    age_5_19 = qs.filter(age_years__gte=5, age_years__lte=19).count()

    # ---- BMI ----
    bmi_order = Case(
        When(bmi_category="severe underweight", then=Value(1)),
        When(bmi_category="underweight", then=Value(2)),
        When(bmi_category="mild underweight", then=Value(3)),
        When(bmi_category="normal", then=Value(4)),
        When(bmi_category="overweight", then=Value(5)),
        When(bmi_category="obese", then=Value(6)),
        default=Value(99),
        output_field=IntegerField(),
    )

    bmi_counts = (
        qs.exclude(bmi_category="N/A")
        .values("bmi_category")
        .annotate(count=Count("id"), sort_order=bmi_order)
        .order_by("sort_order")
    )

    # ---- MUAC ----
    muac_counts = qs.values("muac_sam").annotate(count=Count("id"))

    muac_total = qs.filter(
        muac_sam__iexact="severe acute malnutrition"
    ).count()

    # ---- WEIGHT FOR HEIGHT ----
    weight_height_order = Case(
        When(weight_height="Severe Acute Malnutrition", then=Value(1)),
        When(weight_height="Moderate Acute Malnutrition", then=Value(2)),
        When(weight_height="Normal", then=Value(3)),
        When(weight_height="Overweight", then=Value(4)),
        When(weight_height="Obese", then=Value(5)),
        default=Value(99),
        output_field=IntegerField(),
    )

    weight_height_counts = (
        qs.exclude(weight_height="N/A")
        .values("weight_height")
        .annotate(count=Count("id"), sort_order=weight_height_order)
        .order_by("sort_order")
    )

    # ---- VISION ----
    vision_total = qs.filter(vision_problem__iexact="Yes").count()

    # ---- AGE SEGMENTS (LEGACY FIELD) ----
    age_groups = qs.values("age_screening").annotate(count=Count("id"))

    # ---- SCREENING CHECKS ----
    checklist_qs = ScreeningCheck.objects.filter(screening__in=qs)

    # =====================================
    # VACCINATION
    # =====================================
    vaccination_yes = checklist_qs.filter(vaccination__iexact="yes").count()

    vaccination_no = checklist_qs.filter(vaccination__iexact="no").count()

    vaccination_unknown = checklist_qs.filter(
        Q(vaccination__iexact="unknown") |
        Q(vaccination__isnull=True) |
        Q(vaccination="") |
        (~Q(vaccination__iexact="yes") & ~Q(vaccination__iexact="no"))
    ).count()

    # =====================================
    # DEWORMING
    # =====================================
    deworming_yes = checklist_qs.filter(deworming__iexact="yes").count()

    deworming_no = checklist_qs.filter(deworming__iexact="no").count()

    deworming_unknown = checklist_qs.filter(
        Q(deworming__iexact="unknown") |
        Q(deworming__isnull=True) |
        Q(deworming="") |
        (~Q(deworming__iexact="yes") & ~Q(deworming__iexact="no"))
    ).count()

    # ---- CHECKLIST BOOLEAN STATS ----
    checklist_fields = [
        f.name
        for f in ScreeningCheck._meta.get_fields()
        if f.get_internal_type() == "BooleanField"
    ]

    checklist_stats = {
        field: checklist_qs.filter(**{field: True}).count()
        for field in checklist_fields
    }

    # =====================================
    # FINAL RESPONSE
    # =====================================
    return {
        "totals": {
            "screenings": total_screenings,
            "students": total_students,
            "schools": total_schools,
        },
        "bmi": list(bmi_counts),
        "muac": list(muac_counts),
        "muac_total": muac_total,
        "weight_height": list(weight_height_counts),
        "vision": vision_total,
        "age_groups": list(age_groups),
        "checklist": checklist_stats,

        "vaccination": {
            "yes": vaccination_yes,
            "no": vaccination_no,
            "unknown": vaccination_unknown,
        },
        "deworming": {
            "yes": deworming_yes,
            "no": deworming_no,
            "unknown": deworming_unknown,
        },

        # ✅ THIS MUST MATCH TEMPLATE
       "age_groups_summary": {
        "age_2_5": age_2_5,
        "age_5_19": age_5_19,
}
    }