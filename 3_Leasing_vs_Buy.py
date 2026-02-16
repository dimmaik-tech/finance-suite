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

col1, col2, col3 = st.columns(3)

with col1:
    car_price = st.number_input("Τιμή Αγοράς Αυτοκινήτου (€)", value=45000.0)

with col2:
    expected_resale = st.number_input("Αξία Μεταπώλησης σε 5 χρόνια (€)", value=23000.0)

with col3:
    tax_rate = st.number_input("Φορολογικός Συντελεστής", value=0.22)

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

c1, c2, c3 = st.columns(3)

with c1:
    monthly_payment = st.number_input("Μηνιαίο Μίσθωμα (€)", value=800.0)

with c2:
    duration_months = st.number_input("Διάρκεια Leasing (μήνες)", value=60)

with c3:
    buyout_price = st.number_input("Τιμή Εξαγοράς στο Τέλος (€)", value=20000.0)

down_payment_leasing = st.number_input("Προκαταβολή Leasing (€)", value=0.0)

st.divider()

# =========================
# CALCULATIONS
# =========================

# ---- Leasing ----
total_leasing_paid = monthly_payment * duration_months + down_payment_leasing
tax_benefit = total_leasing_paid * tax_rate
net_leasing_cost = total_leasing_paid - tax_benefit
leasing_plus_buyout = net_leasing_cost + buyout_price

# ---- Loan Purchase ----
loan_amount = car_price - down_payment_buy
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

# Net cost of buying
buy_cost = down_payment_buy + total_loan_paid - expected_resale

# =========================
# RESULTS
# =========================

st.header("📊 Σύγκριση Κόστους 5ετίας")

r1, r2, r3 = st.columns(3)

r1.metric("Leasing + Εξαγορά (Net)", f"€{leasing_plus_buyout:,.0f}")
r2.metric("Αγορά με Δάνειο (Net)", f"€{buy_cost:,.0f}")
r3.metric("Μηνιαία Δόση Δανείου", f"€{loan_monthly_payment:,.0f}")

st.divider()

# Verdict
st.subheader("🏁 Verdict")

if leasing_plus_buyout < buy_cost:
    st.success(f"""
🟢 Συμφέρει το Leasing + Εξαγορά!

Φθηνότερο κατά:
**€{buy_cost - leasing_plus_buyout:,.0f}**
σε σχέση με αγορά μέσω δανείου.
""")
elif leasing_plus_buyout > buy_cost:
    st.error(f"""
🔴 Συμφέρει η Αγορά με Δάνειο!

Το Leasing κοστίζει περισσότερο κατά:
**€{leasing_plus_buyout - buy_cost:,.0f}**
""")
else:
    st.warning("🟡 Είναι σχεδόν ίδια. Παίζουν ρόλο λεπτομέρειες αγοράς.")

st.divider()

st.markdown("### 📌 Breakdown")

st.write(f"""
## Leasing
- Συνολικά μισθώματα: €{total_leasing_paid:,.0f}  
- Φορολογικό όφελος (22%): €{tax_benefit:,.0f}  
- Καθαρό κόστος leasing: €{net_leasing_cost:,.0f}  
- Τιμή εξαγοράς: €{buyout_price:,.0f}  
➡️ **Leasing + Buyout Total:** €{leasing_plus_buyout:,.0f}  

---

## Αγορά με Δάνειο
- Ποσό δανείου: €{loan_amount:,.0f}  
- Συνολικοί τόκοι: €{total_interest:,.0f}  
- Συνολικό ποσό πληρωμών: €{total_loan_paid:,.0f}  
- Μεταπώληση σε 5 χρόνια: €{expected_resale:,.0f}  
➡️ **Net Cost αγοράς:** €{buy_cost:,.0f}
""")
