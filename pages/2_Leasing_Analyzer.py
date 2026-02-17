import streamlit as st
import math

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


st.set_page_config(page_title="Leasing Buyout Analyzer", layout="wide")

st.title("🚗 Leasing Buyout Analyzer (ΙΧ – 5ετία)")
st.markdown("""
Υπολογίζει αν σε συμφέρει η **τιμή εξαγοράς** στο τέλος της μίσθωσης,
λαμβάνοντας υπόψη το φορολογικό όφελος στην Ελλάδα.

✅ Ατομική επιχείρηση (default)  
✅ Φόρος 22% (editable)  
✅ Εκπιπτόμενα έξοδα leasing (editable)
""")

st.divider()

# =========================
# INPUTS
# =========================
st.header("📌 Στοιχεία Leasing")

col1, col2, col3 = st.columns(3)

with col1:
    monthly_payment = st.number_input("Μηνιαίο Μίσθωμα (€)", value=800.0, step=10.0)

with col2:
    duration_months = st.number_input("Διάρκεια (μήνες)", value=60, step=1, min_value=1)

with col3:
    down_payment = st.number_input("Προκαταβολή (€)", value=0.0, step=500.0, min_value=0.0)

st.divider()

# =========================
# BUYOUT + RESIDUAL MODEL
# =========================
st.subheader("📉 Αναμενόμενη Αξία Αγοράς (Residual %)")

col4, col5, col6 = st.columns(3)

with col4:
    buyout_price = st.number_input("Τιμή Εξαγοράς στο Τέλος (€)", value=20000.0, step=500.0, min_value=0.0)

with col5:
    purchase_price = st.number_input("Τιμή Αγοράς Σήμερα (€)", value=50000.0, step=1000.0, min_value=0.0)

with col6:
    residual_pct = st.slider("Residual % σε 5 χρόνια", min_value=20, max_value=60, value=40)

expected_market_value = purchase_price * (residual_pct / 100)

st.info(f"📌 Αναμενόμενη Αξία Αγοράς σε 5 χρόνια (auto): **{euro(expected_market_value)}**")

st.divider()

# =========================
# TAX SETTINGS
# =========================
st.header("🏛️ Φορολογικά (ρυθμίσεις)")

t1, t2, t3 = st.columns(3)

with t1:
    tax_rate = st.slider("Φορολογικός συντελεστής", 0.0, 0.5, 0.22, step=0.01)

with t2:
    deductibility = st.slider("Έκπτωση εξόδων leasing", 0, 100, 100, help="Πόσο % των εξόδων leasing εκπίπτει φορολογικά.")
    deductibility = deductibility / 100.0

with t3:
    verdict_threshold_pct = st.slider("Ζώνη “Οριακό” (% της αξίας)", 1, 15, 5, help="Πόσο κοντά στο market value θεωρείται οριακό.")

st.caption(f"Tax benefit = Total leasing paid × {pct(tax_rate*100)} × {pct(deductibility*100)}")

# =========================
# CALCULATIONS
# =========================
total_leasing_cost = monthly_payment * duration_months + down_payment
tax_benefit = total_leasing_cost * tax_rate * deductibility
net_cost = total_leasing_cost - tax_benefit

difference = expected_market_value - buyout_price
threshold = expected_market_value * (verdict_threshold_pct / 100.0)

# =========================
# RESULTS
# =========================
st.divider()
st.header("📊 Αποτελέσματα")

r1, r2, r3, r4 = st.columns(4)

r1.metric("Συνολικό Κόστος Leasing", euro(total_leasing_cost))
r2.metric("Φορολογικό Όφελος", euro(tax_benefit))
r3.metric("Καθαρό Κόστος μετά Φόρου", euro(net_cost))
r4.metric("Equity στην Εξαγορά", euro(difference), help="Expected Market Value - Buyout Price")

st.divider()

# Verdict
st.subheader("💡 Απόφαση Εξαγοράς")

if expected_market_value <= 0:
    st.warning("Βάλε τιμή αγοράς σήμερα > 0 για να υπολογιστεί σωστά η αναμενόμενη αξία.")
else:
    if difference > threshold:
        st.success(f"""
🟢 Συμφέρει η εξαγορά!

- Buyout: **{euro(buyout_price)}**
- Market (expected): **{euro(expected_market_value)}**
- Διαφορά: **{euro(difference)}**
""")
    elif -threshold <= difference <= threshold:
        st.warning(f"""
🟡 Οριακή περίπτωση.

- Buyout: **{euro(buyout_price)}**
- Market (expected): **{euro(expected_market_value)}**
- Διαφορά: **{euro(difference)}**
""")
    else:
        st.error(f"""
🔴 Δεν συμφέρει η εξαγορά.

- Buyout: **{euro(buyout_price)}**
- Market (expected): **{euro(expected_market_value)}**
- Διαφορά: **{euro(difference)}**
""")

# =========================
# PREMIUM: SENSITIVITY (Residual %)
# =========================
st.divider()
st.subheader("📈 Sensitivity: Residual % vs Απόφαση")

scol1, scol2 = st.columns([2, 1])

with scol2:
    sens_min = st.number_input("Min Residual %", value=30, step=1, min_value=10, max_value=90)
    sens_max = st.number_input("Max Residual %", value=55, step=1, min_value=10, max_value=90)
    sens_step = st.number_input("Step", value=5, step=1, min_value=1, max_value=20)

if sens_min >= sens_max:
    st.warning("Min πρέπει να είναι μικρότερο από Max.")
else:
    rows = []
    rp = sens_min
    while rp <= sens_max:
        mv = purchase_price * (rp / 100.0)
        diff = mv - buyout_price
        label = "🟢 Buy" if diff > threshold else ("🟡 Borderline" if -threshold <= diff <= threshold else "🔴 No")
        rows.append({"Residual %": f"{rp}%", "Expected Value": euro(mv), "Equity": euro(diff), "Verdict": label})
        rp += sens_step

    st.table(rows)

# =========================
# EMAIL GENERATOR
# =========================
st.divider()
st.header("✉️ Email προς Leasing Εταιρεία")

company_name = st.text_input("Όνομα Leasing Εταιρείας", value="(εταιρεία leasing)")
client_name = st.text_input("Το όνομά σου", value="Panagiotis ...")

email_text = f"""
Θέμα: Αναθεώρηση Τιμής Εξαγοράς στο τέλος μίσθωσης

Αξιότιμοι κύριοι/κυρίες της {company_name},

θα ήθελα να ζητήσω διευκρίνιση και πιθανή αναθεώρηση σχετικά με την τιμή εξαγοράς
του οχήματος στο τέλος της σύμβασης leasing.

Σύμφωνα με την προσφορά σας, η τιμή εξαγοράς ανέρχεται σε:
• {euro(buyout_price)}

Με βάση εκτίμηση αγοραίας αξίας σε 5 χρόνια (residual {residual_pct}% επί της σημερινής αξίας {euro(purchase_price)}),
η αναμενόμενη αξία διαμορφώνεται περίπου σε:
• {euro(expected_market_value)}

Η διαφορά ανέρχεται σε περίπου:
• {euro(abs(difference))}

Παρακαλώ όπως εξετάσετε τη δυνατότητα αναπροσαρμογής της τιμής εξαγοράς
σε επίπεδα πιο κοντά στην πραγματική αξία αγοράς και μου αποστείλετε
επικαιροποιημένη πρόταση.

Με εκτίμηση,
{client_name}
"""

st.text_area("📩 Έτοιμο Email", email_text, height=260)

# PREMIUM: Quick report export
report_text = f"""
Leasing Buyout Analyzer Report
-----------------------------
Monthly payment: {euro(monthly_payment)}
Duration months: {duration_months}
Down payment: {euro(down_payment)}
Total leasing paid: {euro(total_leasing_cost)}
Tax rate: {tax_rate:.2f}
Deductibility: {deductibility:.2f}
Tax benefit: {euro(tax_benefit)}
Net leasing cost: {euro(net_cost)}

Purchase price today: {euro(purchase_price)}
Residual %: {residual_pct}%
Expected market value (5y): {euro(expected_market_value)}
Buyout price: {euro(buyout_price)}
Equity (market - buyout): {euro(difference)}
"""

st.download_button("📄 Κατέβασε Report (TXT)", report_text, file_name="leasing_buyout_report.txt")
st.download_button("📄 Κατέβασε Email (TXT)", email_text, file_name="leasing_buyout_email.txt")
