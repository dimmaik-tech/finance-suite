import streamlit as st
from auth import require_login, show_logout_button, admin_badge
require_login("Finance Suite")
admin_badge()
show_logout_button(key="logout_fin_page_1")  # unique key

from auth import require_login, show_logout
require_login("Finance Suite")
show_logout()

import streamlit as st

# =========================
# Helper: Euro Formatting (GR)
# =========================
def euro(x):
    try:
        return "€{:,.0f}".format(float(x)).replace(",", ".")
    except Exception:
        return "€0"

def pct(x):
    return f"{x:.0f}%"


st.set_page_config(page_title="Leasing vs Buy + Loan", layout="wide")

st.title("⚖️ Leasing vs Αγορά + Δάνειο (5ετής Σύγκριση)")
st.markdown("""
Σύγκριση:

✅ Leasing (με φορολογικό όφελος)  
vs  
✅ Αγορά με δάνειο (τόκοι + μεταπώληση)

και σου δείχνει ποιο είναι οικονομικά καλύτερο.
""")

st.divider()

# =========================
# CAR INPUTS
# =========================
st.header("📌 Στοιχεία Αυτοκινήτου")

col1, col2, col3, col4 = st.columns(4)

with col1:
    car_price = st.number_input("Τιμή Αγοράς Αυτοκινήτου (€)", value=45000.0, step=1000.0, min_value=0.0)

with col2:
    residual_pct = st.slider("Residual % σε 5 χρόνια", 20, 60, 40)

with col3:
    tax_rate = st.slider("Φορολογικός συντελεστής", 0.0, 0.5, 0.22, step=0.01)

with col4:
    deductibility = st.slider("Έκπτωση εξόδων leasing (%)", 0, 100, 100)
    deductibility = deductibility / 100.0

expected_resale = car_price * (residual_pct / 100.0)
st.info(f"📌 Αξία Μεταπώλησης σε 5 χρόνια (auto): **{euro(expected_resale)}**")

st.divider()

# =========================
# LOAN SETTINGS
# =========================
st.header("🏦 Αγορά με Δάνειο")

l1, l2, l3 = st.columns(3)

with l1:
    loan_interest = st.number_input("Επιτόκιο Δανείου (%)", value=6.0, step=0.1, min_value=0.0)

with l2:
    loan_years = st.number_input("Διάρκεια Δανείου (έτη)", value=5, step=1, min_value=1)

with l3:
    down_payment_buy = st.number_input("Προκαταβολή Αγοράς (€)", value=0.0, step=1000.0, min_value=0.0)

st.divider()

# =========================
# LEASING INPUTS
# =========================
st.header("🚗 Στοιχεία Leasing")

c1, c2, c3, c4 = st.columns(4)

with c1:
    monthly_payment = st.number_input("Μηνιαίο Μίσθωμα (€)", value=800.0, step=10.0, min_value=0.0)

with c2:
    duration_months = st.number_input("Διάρκεια Leasing (μήνες)", value=60, step=1, min_value=1)

with c3:
    buyout_price = st.number_input("Τιμή Εξαγοράς στο Τέλος (€)", value=20000.0, step=500.0, min_value=0.0)

with c4:
    down_payment_leasing = st.number_input("Προκαταβολή Leasing (€)", value=0.0, step=500.0, min_value=0.0)

include_buyout = st.toggle("Υπολόγισε Leasing + Εξαγορά", value=True)

st.divider()

# =========================
# CALCULATIONS
# =========================

# Leasing
total_leasing_paid = monthly_payment * duration_months + down_payment_leasing
tax_benefit_leasing = total_leasing_paid * tax_rate * deductibility
net_leasing_cost = total_leasing_paid - tax_benefit_leasing
leasing_total = net_leasing_cost + (buyout_price if include_buyout else 0.0)

# Loan Purchase
loan_amount = max(0.0, car_price - down_payment_buy)
monthly_rate = (loan_interest / 100.0) / 12.0
n_payments = int(loan_years * 12)

if n_payments <= 0:
    loan_monthly_payment = 0.0
    total_loan_paid = 0.0
    total_interest = 0.0
else:
    if monthly_rate > 0:
        loan_monthly_payment = loan_amount * (
            monthly_rate * (1 + monthly_rate) ** n_payments
        ) / ((1 + monthly_rate) ** n_payments - 1)
    else:
        loan_monthly_payment = loan_amount / n_payments

    total_loan_paid = loan_monthly_payment * n_payments
    total_interest = total_loan_paid - loan_amount

buy_cost = down_payment_buy + total_loan_paid - expected_resale

# =========================
# RESULTS
# =========================
st.header("📊 Σύγκριση Κόστους 5ετίας")

r1, r2, r3, r4 = st.columns(4)

r1.metric("Leasing (Net)", euro(net_leasing_cost))
r2.metric("Leasing Total", euro(leasing_total), help="Με/χωρίς εξαγορά ανάλογα με το toggle.")
r3.metric("Αγορά με Δάνειο (Net)", euro(buy_cost))
r4.metric("Μηνιαία Δόση Δανείου", euro(loan_monthly_payment))

st.divider()

# Verdict
st.subheader("🏁 Verdict")
diff = buy_cost - leasing_total  # + means leasing cheaper

if diff > 0:
    st.success(f"🟢 Συμφέρει το Leasing{' + Εξαγορά' if include_buyout else ''}! Φθηνότερο κατά **{euro(diff)}**.")
elif diff < 0:
    st.error(f"🔴 Συμφέρει η Αγορά με Δάνειο! Το Leasing κοστίζει περισσότερο κατά **{euro(-diff)}**.")
else:
    st.warning("🟡 Είναι σχεδόν ίδια.")

st.divider()

# Breakdown
st.markdown("### 📌 Breakdown")

st.write(f"""
## Leasing
- Συνολικά μισθώματα: {euro(total_leasing_paid)}
- Φορολογικό όφελος ({pct(tax_rate*100)} × {pct(deductibility*100)}): {euro(tax_benefit_leasing)}
- Καθαρό κόστος leasing: {euro(net_leasing_cost)}
- Τιμή εξαγοράς: {euro(buyout_price)}
- Εξαγορά: {"Ναι" if include_buyout else "Όχι"}
➡️ **Leasing Total:** {euro(leasing_total)}

---

## Αγορά με Δάνειο
- Ποσό δανείου: {euro(loan_amount)}
- Συνολικοί τόκοι: {euro(total_interest)}
- Συνολικό ποσό πληρωμών: {euro(total_loan_paid)}
- Μεταπώληση σε 5 χρόνια (Residual {residual_pct}%): {euro(expected_resale)}
➡️ **Net Cost αγοράς:** {euro(buy_cost)}
""")

# =========================
# PREMIUM: SENSITIVITY (Residual %)
# =========================
st.divider()
st.subheader("📈 Sensitivity: Residual % → ποιο συμφέρει;")

s1, s2 = st.columns([2, 1])

with s2:
    sens_min = st.number_input("Min Residual %", value=30, step=1, min_value=10, max_value=90)
    sens_max = st.number_input("Max Residual %", value=55, step=1, min_value=10, max_value=90)
    sens_step = st.number_input("Step", value=5, step=1, min_value=1, max_value=20)

if sens_min >= sens_max:
    st.warning("Min πρέπει να είναι μικρότερο από Max.")
else:
    rows = []
    rp = sens_min
    while rp <= sens_max:
        resale = car_price * (rp / 100.0)
        buy_cost_s = down_payment_buy + total_loan_paid - resale
        diff_s = buy_cost_s - leasing_total
        verdict = "🟢 Leasing" if diff_s > 0 else ("🔴 Buy" if diff_s < 0 else "🟡 Same")
        rows.append({
            "Residual %": f"{rp}%",
            "Resale": euro(resale),
            "Buy Net": euro(buy_cost_s),
            "Diff (Buy - Leasing)": euro(diff_s),
            "Verdict": verdict
        })
        rp += sens_step

    st.table(rows)

# =========================
# CHART: Residual % vs Cost Difference
# =========================
st.markdown("### 📉 Chart: Residual % → Buy vs Leasing Difference")

chart_data = {
    "Residual %": [],
    "Diff (Buy - Leasing) €": []
}

rp = sens_min
while rp <= sens_max:
    resale = car_price * (rp / 100.0)
    buy_cost_s = down_payment_buy + total_loan_paid - resale
    diff_s = buy_cost_s - leasing_total

    chart_data["Residual %"].append(rp)
    chart_data["Diff (Buy - Leasing) €"].append(diff_s)

    rp += sens_step

st.line_chart(chart_data, x="Residual %", y="Diff (Buy - Leasing) €")


# PREMIUM: Export report
report_text = f"""
Leasing vs Buy + Loan Report
----------------------------
Car price: {euro(car_price)}
Residual %: {residual_pct}%
Expected resale (5y): {euro(expected_resale)}

Leasing:
Monthly: {euro(monthly_payment)}
Duration: {duration_months} months
Down payment (leasing): {euro(down_payment_leasing)}
Total paid: {euro(total_leasing_paid)}
Tax rate: {tax_rate:.2f}
Deductibility: {deductibility:.2f}
Tax benefit: {euro(tax_benefit_leasing)}
Net leasing cost: {euro(net_leasing_cost)}
Buyout: {euro(buyout_price)}
Include buyout: {include_buyout}
Leasing total: {euro(leasing_total)}

Loan purchase:
Down payment (buy): {euro(down_payment_buy)}
Loan amount: {euro(loan_amount)}
Interest: {loan_interest:.2f}%
Years: {loan_years}
Monthly payment: {euro(loan_monthly_payment)}
Total paid: {euro(total_loan_paid)}
Total interest: {euro(total_interest)}
Buy net cost (5y): {euro(buy_cost)}
Diff (Buy - Leasing): {euro(diff)}
"""

st.download_button("📄 Κατέβασε Report (TXT)", report_text, file_name="lease_vs_buy_report.txt")
