import streamlit as st

st.set_page_config(page_title="Leasing vs Buy + Loan", layout="wide")

st.title("⚖️ Leasing vs Αγορά + Δάνειο (5ετής Σύγκριση)")
st.markdown("""
Σύγκριση:

✅ Leasing (με φορολογικό όφελος)  
vs  
✅ Αγορά με δάνειο (κόστος τόκων + μεταπώληση)

και σου δείχνει ποιο είναι οικονομικά καλύτερο.
""")

st.divider()

# =========================
# CAR INPUTS
# =========================

st.header("📌 Στοιχεία Αυτοκινήτου")

col1, col2, col3, col4 = st.columns(4)

with col1:
    car_price = st.number_input("Τιμή Αγοράς Αυτοκινήτου (€)", value=45000.0, step=1000.0)

with col2:
    residual_pct = st.slider("Residual % σε 5 χρόνια", min_value=20, max_value=60, value=40)

with col3:
    tax_rate = st.number_input("Φορολογικός Συντελεστής", value=0.22, min_value=0.0, max_value=1.0, step=0.01)

with col4:
    deductibility = st.slider("Έκπτωση εξόδων leasing (%)", 0, 100, 100)

deductibility = deductibility / 100.0

# Auto expected resale
expected_resale = car_price * (residual_pct / 100.0)
st.info(f"📌 Αξία Μεταπώλησης σε 5 χρόνια (auto): **€{expected_resale:,.0f}**")

st.divider()

# =========================
# LOAN SETTINGS
# =========================

st.header("🏦 Αγορά με Δάνειο")

l1, l2, l3 = st.columns(3)

with l1:
    loan_interest = st.number_input("Επιτόκιο Δανείου (%)", value=6.0, step=0.1)

with l2:
    loan_years = st.number_input("Διάρκεια Δανείου (έτη)", value=5, step=1)

with l3:
    down_payment_buy = st.number_input("Προκαταβολή Αγοράς (€)", value=0.0, step=1000.0)

st.divider()

# =========================
# LEASING INPUTS
# =========================

st.header("🚗 Στοιχεία Leasing")

c1, c2, c3, c4 = st.columns(4)

with c1:
    monthly_payment = st.number_input("Μηνιαίο Μίσθωμα (€)", value=800.0, step=10.0)

with c2:
    duration_months = st.number_input("Διάρκεια Leasing (μήνες)", value=60, step=1)

with c3:
    buyout_price = st.number_input("Τιμή Εξαγοράς στο Τέλος (€)", value=20000.0, step=500.0)

with c4:
    down_payment_leasing = st.number_input("Προκαταβολή Leasing (€)", value=0.0, step=500.0)

include_buyout = st.toggle("Υπολόγισε Leasing + Εξαγορά", value=True)

st.divider()

# =========================
# CALCULATIONS
# =========================

# ---- Leasing ----
total_leasing_paid = monthly_payment * duration_months + down_payment_leasing
tax_benefit_leasing = total_leasing_paid * tax_rate * deductibility
net_leasing_cost = total_leasing_paid - tax_benefit_leasing

leasing_total = net_leasing_cost + (buyout_price if include_buyout else 0.0)

# ---- Loan Purchase ----
loan_amount = max(0.0, car_price - down_payment_buy)
monthly_rate = (loan_interest / 100.0) / 12.0
n_payments = int(loan_years * 12)

if n_payments == 0:
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

# Net cost of buying (no tax handling here by design)
buy_cost = down_payment_buy + total_loan_paid - expected_resale

# =========================
# RESULTS
# =========================

st.header("📊 Σύγκριση Κόστους 5ετίας")

r1, r2, r3, r4 = st.columns(4)

r1.metric("Leasing (Net)", f"€{net_leasing_cost:,.0f}")
r2.metric("Leasing Total", f"€{leasing_total:,.0f}", help="Με ή χωρίς εξαγορά, ανάλογα με το toggle.")
r3.metric("Αγορά με Δάνειο (Net)", f"€{buy_cost:,.0f}")
r4.metric("Μηνιαία Δόση Δανείου", f"€{loan_monthly_payment:,.0f}")

st.divider()

# Verdict
st.subheader("🏁 Verdict")

diff_vs_buy = buy_cost - leasing_total  # positive means leasing cheaper

if diff_vs_buy > 0:
    st.success(f"🟢 Συμφέρει το Leasing{' + Εξαγορά' if include_buyout else ''}! Φθηνότερο κατά **€{diff_vs_buy:,.0f}**.")
elif diff_vs_buy < 0:
    st.error(f"🔴 Συμφέρει η Αγορά με Δάνειο! Το Leasing κοστίζει περισσότερο κατά **€{-diff_vs_buy:,.0f}**.")
else:
    st.warning("🟡 Είναι σχεδόν ίδια. Παίζουν ρόλο λεπτομέρειες αγοράς.")

st.divider()

st.markdown("### 📌 Breakdown")

st.write(f"""
## Leasing
- Συνολικά μισθώματα: €{total_leasing_paid:,.0f}  
- Φορολογικό όφελος ({int(tax_rate*100)}% × {int(deductibility*100)}%): €{tax_benefit_leasing:,.0f}  
- Καθαρό κόστος leasing: €{net_leasing_cost:,.0f}  
- Τιμή εξαγοράς: €{buyout_price:,.0f}  
- Υπολογισμός εξαγοράς: {"Ναι" if include_buyout else "Όχι"}  
➡️ **Leasing Total:** €{leasing_total:,.0f}  

---

## Αγορά με Δάνειο
- Ποσό δανείου: €{loan_amount:,.0f}  
- Συνολικοί τόκοι: €{total_interest:,.0f}  
- Συνολικό ποσό πληρωμών: €{total_loan_paid:,.0f}  
- Μεταπώληση σε 5 χρόνια (Residual {residual_pct}%): €{expected_resale:,.0f}  
➡️ **Net Cost αγοράς:** €{buy_cost:,.0f}
""")
