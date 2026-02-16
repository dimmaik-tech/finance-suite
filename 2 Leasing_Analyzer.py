import streamlit as st

st.set_page_config(page_title="Leasing Buyout Analyzer", layout="wide")

st.title("🚗 Leasing Buyout Analyzer (ΙΧ – 5ετία)")
st.markdown("""
Υπολογίζει αν σε συμφέρει η **τιμή εξαγοράς** στο τέλος της μίσθωσης,
λαμβάνοντας υπόψη το φορολογικό όφελος στην Ελλάδα:

✅ Ατομική επιχείρηση  
✅ Φόρος 22%  
✅ 100% εκπιπτόμενα έξοδα leasing  
""")

st.divider()

# =========================
# INPUTS
# =========================

st.header("📌 Στοιχεία Leasing")

col1, col2, col3 = st.columns(3)

with col1:
    monthly_payment = st.number_input("Μηνιαίο Μίσθωμα (€)", value=800.0)

with col2:
    duration_months = st.number_input("Διάρκεια (μήνες)", value=60)

with col3:
    down_payment = st.number_input("Προκαταβολή (€)", value=0.0)

col4, col5 = st.columns(2)

with col4:
    buyout_price = st.number_input("Τιμή Εξαγοράς στο Τέλος (€)", value=20000.0)

with col5:
    expected_market_value = st.number_input(
        "Αναμενόμενη Αξία Αγοράς σε 5 χρόνια (€)",
        value=23000.0
    )

st.divider()

# =========================
# TAX SETTINGS
# =========================

st.header("🏛️ Φορολογικά")

tax_rate = 0.22
deductibility = 1.0

st.info(f"""
Φορολογικός συντελεστής: **{int(tax_rate*100)}%**  
Έξοδα leasing εκπίπτουν: **100%**
""")

# =========================
# CALCULATIONS
# =========================

total_leasing_cost = monthly_payment * duration_months + down_payment
tax_benefit = total_leasing_cost * tax_rate * deductibility
net_cost = total_leasing_cost - tax_benefit

difference = expected_market_value - buyout_price

# =========================
# RESULTS
# =========================

st.header("📊 Αποτελέσματα")

r1, r2, r3 = st.columns(3)

r1.metric("Συνολικό Κόστος Leasing", f"€{total_leasing_cost:,.2f}")
r2.metric("Φορολογικό Όφελος", f"€{tax_benefit:,.2f}")
r3.metric("Καθαρό Κόστος μετά Φόρου", f"€{net_cost:,.2f}")

st.divider()

# Verdict
st.subheader("💡 Απόφαση Εξαγοράς")

if difference > 2000:
    st.success(f"""
🟢 Συμφέρει η εξαγορά!

Η τιμή εξαγοράς είναι **€{difference:,.0f} κάτω**
από την εκτιμώμενη αγοραία αξία.
""")
elif -2000 <= difference <= 2000:
    st.warning(f"""
🟡 Οριακή περίπτωση.

Η τιμή εξαγοράς είναι πολύ κοντά στην αγορά.
Διαφορά: €{difference:,.0f}
""")
else:
    st.error(f"""
🔴 Δεν συμφέρει η εξαγορά.

Η εταιρεία ζητάει **€{-difference:,.0f} πάνω**
από την εκτιμώμενη αξία αγοράς.
""")

st.divider()

# =========================
# EMAIL GENERATOR
# =========================

st.header("✉️ Email προς Leasing Εταιρεία")

company_name = st.text_input("Όνομα Leasing Εταιρείας", value="(εταιρεία leasing)")
client_name = st.text_input("Το όνομά σου", value="Panagiotis ...")

email_text = f"""
Θέμα: Αναθεώρηση Τιμής Εξαγοράς στο τέλος μίσθωσης

Αξιότιμοι κύριοι/κυρίες της {company_name},

θα ήθελα να ζητήσω διευκρίνιση και πιθανή αναθεώρηση σχετικά με την τιμή εξαγοράς
του οχήματος στο τέλος της σύμβασης leasing.

Σύμφωνα με την προσφορά σας, η τιμή εξαγοράς ανέρχεται σε:

• €{buyout_price:,.0f}

Ωστόσο, με βάση την εκτιμώμενη αγοραία αξία του οχήματος κατά το τέλος της μίσθωσης,
η οποία υπολογίζεται περίπου σε:

• €{expected_market_value:,.0f}

η διαφορά ανέρχεται σε περίπου:

• €{abs(difference):,.0f}

Παρακαλώ όπως εξετάσετε τη δυνατότητα αναπροσαρμογής της τιμής εξαγοράς
σε επίπεδα πιο κοντά στην πραγματική αξία αγοράς και μου αποστείλετε
επικαιροποιημένη πρόταση.

Με εκτίμηση,  
{client_name}
"""

st.text_area("📩 Έτοιμο Email", email_text, height=250)

st.download_button(
    "📄 Κατέβασε Email σε TXT",
    email_text,
    file_name="leasing_buyout_email.txt"
)
