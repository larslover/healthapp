from django.db.models import Count, Case, When, IntegerField, Value, Q
from core.models import Screening, ScreeningCheck


def get_screening_statistics(
    *,
    academic_year,
    school_id=None,
    class_section=None,
):
    """
    Centralized statistics engine for dashboard & reports.
    """

    # =====================================
    # BASE QUERYSET (DB)
    # =====================================
    base_qs = Screening.objects.filter(
    academic_year=academic_year,
    screening_type="full"   # ✅ EXCLUDE PARTIAL
)

    if school_id:
        base_qs = base_qs.filter(student__school_id=school_id)

    if class_section:
        base_qs = base_qs.filter(class_section=class_section)

    base_qs = base_qs.select_related("student", "student__school")

    # =====================================
    # PYTHON COPY (for accurate age calc)
    # =====================================
    rows = list(base_qs)

    # =====================================
    # HEADLINE TOTALS
    # =====================================
    total_screenings = len(rows)
    total_students = len({s.student_id for s in rows})
    total_schools = len({s.student.school_id for s in rows if s.student and s.student.school})


        # =====================================
    # AGE GROUPS (FIXED - MONTH BASED)
    # =====================================
    age_2_5 = 0
    age_5_19 = 0

    for s in rows:
        dob = s.student.date_of_birth
        screen_date = s.screen_date

        if not dob or not screen_date:
            continue

        age_months = (
            (screen_date.year - dob.year) * 12 +
            (screen_date.month - dob.month)
        )

        if 24 <= age_months <= 60:
            age_2_5 += 1
        elif 61 <= age_months <= 228:
            age_5_19 += 1
    # =====================================
    # BMI DISTRIBUTION
    # =====================================
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
        base_qs.exclude(bmi_category="N/A")
        .values("bmi_category")
        .annotate(count=Count("id"), sort_order=bmi_order)
        .order_by("sort_order")
    )

    # =====================================
    # MUAC
    # =====================================
    muac_counts = base_qs.values("muac_sam").annotate(count=Count("id"))

    muac_total = base_qs.filter(
        muac_sam__iexact="severe acute malnutrition"
    ).count()

    # =====================================
    # WEIGHT FOR HEIGHT
    # =====================================
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
        base_qs.exclude(weight_height="N/A")
        .values("weight_height")
        .annotate(count=Count("id"), sort_order=weight_height_order)
        .order_by("sort_order")
    )

    # =====================================
    # VISION
    # =====================================
    vision_total = base_qs.filter(vision_problem__iexact="Yes").count()

    # =====================================
    # CHECKLIST
    # =====================================
    checklist_qs = ScreeningCheck.objects.filter(screening__in=base_qs)

    vaccination_yes = checklist_qs.filter(vaccination__iexact="yes").count()
    vaccination_no = checklist_qs.filter(vaccination__iexact="no").count()
    vaccination_unknown = checklist_qs.filter(
        Q(vaccination__iexact="unknown") |
        Q(vaccination__isnull=True) |
        Q(vaccination="") |
        (~Q(vaccination__iexact="yes") & ~Q(vaccination__iexact="no"))
    ).count()

    deworming_yes = checklist_qs.filter(deworming__iexact="yes").count()
    deworming_no = checklist_qs.filter(deworming__iexact="no").count()
    deworming_unknown = checklist_qs.filter(
        Q(deworming__iexact="unknown") |
        Q(deworming__isnull=True) |
        Q(deworming="") |
        (~Q(deworming__iexact="yes") & ~Q(deworming__iexact="no"))
    ).count()

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
      "age_2_5": age_2_5,
"age_5_19": age_5_19,
    }