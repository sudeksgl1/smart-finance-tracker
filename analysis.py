def analyze(data):
    total_income = 0
    total_expense = 0

    income_categories = {}
    expense_categories = {}
    fixed_income_categories = {}
    fixed_expense_categories = {}

    for t in data:
        tur = t[1]
        tutar = float(t[2])
        kategori = t[3]

        if tur == "Gelir":
            total_income += tutar
            income_categories[kategori] = income_categories.get(kategori, 0) + tutar

        elif tur == "Gider":
            total_expense += tutar
            expense_categories[kategori] = expense_categories.get(kategori, 0) + tutar

        elif tur == "Sabit Gelir":
            total_income += tutar
            fixed_income_categories[kategori] = fixed_income_categories.get(kategori, 0) + tutar

        elif tur == "Sabit Gider":
            total_expense += tutar
            fixed_expense_categories[kategori] = fixed_expense_categories.get(kategori, 0) + tutar

    return total_income, total_expense, income_categories, expense_categories, fixed_income_categories, fixed_expense_categories


def get_warnings(total_income, total_expense, expense_categories):
    warnings = []

    if total_expense > total_income:
        warnings.append("⚠️ Gelirinden fazla harcama yaptın!")

    if expense_categories:
        max_cat = max(expense_categories, key=expense_categories.get)
        max_amount = expense_categories[max_cat]

        warnings.append(f"📊 En çok değişken harcama yaptığın kategori: {max_cat} ({max_amount} TL)")

        if max_amount >= total_expense * 0.4:
            warnings.append(f"⚠️ {max_cat} kategorisinde fazla harcama yaptın!")

        for cat, amount in expense_categories.items():
            if amount > 5000:
                warnings.append(f"⚠️ {cat} için yüksek harcama yaptın ({amount} TL)")

    return warnings