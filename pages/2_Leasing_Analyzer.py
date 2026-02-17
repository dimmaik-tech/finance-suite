import streamlit as st

# =========================
# Helper: Euro Formatting
# =========================
def euro(x):
    return "€{:,.0f}".format(x).replace(",", ".")


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

st.divider()

# =========================
# BUYOUT + RESIDUAL MODEL
# =========================
st.subheader("📉 Αναμενόμενη Αξία Αγοράς (Residual %)")

col4, col5, col6 = st.columns(3)

with col4:
    buyout_price = st.number_input("Τιμή Εξαγοράς στο Τέλος (€)", value=20000.0)

with col5:
    purchase_price = st.number_input(
        "Τιμή Αγοράς Σήμερα (€)",
        value=50000.0,
        step=1000.0
    )

with col6:
    residual_pct = st.slider(
        "Residual % σε 5 χρόνια",
        min_value=20,
        max_value=60,
        value=40
    )

expected_market_value = purchase_price * (residual_pct / 100)

st.info(
    f"📌 Αναμενόμενη Αξία Αγοράς σε 5 χρόνια (auto): "
    f"**{euro(expected_market_value)}**"
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

# Dynamic threshold (5%)
threshold = expected_market_value * 0.05

# =========================
# RESULTS
# =========================
st.header("📊 Αποτελέσματα")

r1, r2, r3 = st.columns(3)

r1.metric("Συνολικό Κόστος Leasing", euro(total_leasing_cost))
r2.metric("Φορολογικό Όφελος", euro(tax_benefit))
r3.metric("Καθαρό Κόστος μετά Φόρου", euro(net_cost))

st.divider()

# Verdict
st.subheader("💡 Απόφαση Εξαγοράς")

if difference > threshold:
    st.success(f"""
🟢 Συμφέρει η εξαγορά!

Η τιμή εξαγοράς είναι **{euro(difference)} κάτω**
από την αναμενόμενη αγοραία αξία.

(Expected Value: {euro(expected_market_value)})
""")

elif -threshold <= difference <= threshold:
    st.warning(f"""
🟡 Οριακή περίπτωση.

Η τιμή εξαγοράς είναι πολύ κοντά στην αγορά.

Διαφορά: {euro(difference)}
""")

else:
    st.error(f"""
🔴 Δεν συμφέρει η εξαγορά.

Η εταιρεία ζητάει **{euro(-difference)} πάνω**
από την αναμενόμενη αξία αγοράς.

(Expected Value: {euro(expected_market_value)})
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

• {euro(buyout_price)}

Με βάση την εκτιμώμενη αγοραία αξία του οχήματος σε 5 χρόνια,
η οποία προκύπτει από residual rate {residual_pct}% επί της σημερινής αξίας αγοράς,
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

st.text_area("📩 Έτοιμο Email", email_text, height=250)

st.download_button(
    "📄 Κατέβασε Email σε TXT",
    email_text,
    file_name="leasing_buyout_email.txt"
)
