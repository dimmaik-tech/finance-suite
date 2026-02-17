import streamlit as st

# =========================
# Helper: Euro Formatting
# =========================
def euro(x):
    return "€{:,.0f}".format(x).replace(",", ".")


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

col1, col2, col3 = st.columns(3)

with col1:
    car_price = st.number_input("Τιμή Αγοράς Αυτοκινήτου (€)", value=45000.0, step=1000.0)

with col2:
    residual_pct = st.slider("Residual % σε 5 χρόνια", 20, 60, 40)

with col3:
    tax_rate = st.number_input("Φορολογικός Συντελεστής", value=0.22)

expected_resale = car_price * (residual_pct / 100)

st.info(f"📌 Αξία Μεταπώλησης σε 5 χρόνια (auto): **{euro(expected_resale)}**")

st.divider()

# =========================
# LOAN SETTINGS
# =========================
st.header("🏦 Αγορά με Δάνειο")

l1, l2, l3 = st.columns(3)

with l1:
    loan_interest = st.number_input("Επιτόκιο Δανείου (%)", value=6.0)

with l2:
    loan_years = st.number_input("Διάρκεια Δανείου (έτη)", value=5)

with l3:
    down_payment_buy = st.number_input("Προκαταβολή Αγοράς (€)", value=0.0)

st.divider()

# =========================
# LEASING INPUTS
# =========================
st.header("🚗 Στοιχεία Leasing")

c1, c2, c3, c4 = st.columns(4)

with c1:
    monthly_payment = st.number_input("Μηνιαίο Μίσθωμα (€)", value=800.0)

with c2:
    duration_months = st.number_input("Διάρκεια Leasing (μήνες)", value=60)

with c3:
    buyout_price = st.number_input("Τιμή Εξαγοράς στο Τέλος (€)", value=20000.0)

with c4:
    down_payment_leasing = st.number_input("Προκαταβολή Leasing (€)", value=0.0)

include_buyout = st.toggle("Υπολόγισε Leasing + Εξαγορά", value=True)

st.divider()

# =========================
# CALCULATIONS
# =========================

# Leasing
total_leasing_paid = monthly_payment * duration_months + down_payment_leasing
tax_benefit_leasing = total_leasing_paid * tax_rate
net_leasing_cost = total_leasing_paid - tax_benefit_leasing

leasing_total = net_leasing_cost + (buyout_price if include_buyout else 0)

# Loan Purchase
loan_amount = max(0, car_price - down_payment_buy)
monthly_rate = (loan_interest / 100) / 12
n_payments = loan_years * 12

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

r1, r2, r3 = st.columns(3)

r1.metric("Leasing Total", euro(leasing_total))
r2.metric("Αγορά με Δάνειο (Net)", euro(buy_cost))
r3.metric("Μηνιαία Δόση Δανείου", euro(loan_monthly_payment))

st.divider()

# Verdict
st.subheader("🏁 Verdict")

diff = buy_cost - leasing_total

if diff > 0:
    st.success(f"🟢 Συμφέρει το Leasing! Φθηνότερο κατά **{euro(diff)}**.")
elif diff < 0:
    st.error(f"🔴 Συμφέρει η Αγορά! Το Leasing κοστίζει περισσότερο κατά **{euro(-diff)}**.")
else:
    st.warning("🟡 Είναι σχεδόν ίδια.")

st.divider()

# Breakdown
st.markdown("### 📌 Breakdown")

st.write(f"""
## Leasing
- Συνολικά μισθώματα: {euro(total_leasing_paid)}
- Φορολογικό όφελος: {euro(tax_benefit_leasing)}
- Καθαρό κόστος leasing: {euro(net_leasing_cost)}
- Τιμή εξαγοράς: {euro(buyout_price)}
➡️ **Leasing Total:** {euro(leasing_total)}

---

## Αγορά με Δάνειο
- Ποσό δανείου: {euro(loan_amount)}
- Συνολικοί τόκοι: {euro(total_interest)}
- Συνολικό ποσό πληρωμών: {euro(total_loan_paid)}
- Μεταπώληση σε 5 χρόνια (Residual {residual_pct}%): {euro(expected_resale)}
➡️ **Net Cost αγοράς:** {euro(buy_cost)}
""")
