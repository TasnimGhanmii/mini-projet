from surveillance_api.models import Formula


def calculate_max_hours(row):
    formula_instance = Formula.objects.first()
    formula = formula_instance.formula if formula_instance else "(courses + td + tp * 0.75) * coef"
    try:
        max_hours = round(eval(formula, {"courses": row["Cours"], "td": row["TD"], "tp": row["TP"]}))
        return max_hours
    except Exception as e:
        print(f"Error evaluating formula: {e}")
        return 0