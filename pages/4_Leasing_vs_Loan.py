import streamlit as st
from auth import require_login, show_logout_button, admin_badge
import math

# =========================
# Page Config (ΜΟΝΟ ΜΙΑ ΦΟΡΑ!)
# =========================
st.set_page_config(
    page_title="Leasing Analyzer",
    layout="wide"
)

require_login("Finance Suite")
admin_badge()
show_logout_button(key="logout_leasing")



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


st.title("🚗 Leasing vs Loan Analyzer (ΙΧ/Εταιρικό – 5ετία)")
st.markdown("""
Υπολογίζει αν σε συμφέρει **Leasing ή Δάνειο** για απόκτηση οχήματος,
λαμβάνοντας υπόψη:
- ✅ Φορολογικά οφέλη leasing (προσαύξηση 50%/25% για ηλεκτρικά)
- ✅ Φορολογικά οφέλη δανείου (απόσβεση + τόκοι)
- ✅ Σύγκριση καθαρού κόστους

**Νέα:** Υποστήριξη ηλεκτρικών οχημάτων μηδενικών ρύπων (BEV) με προσαύξηση εξόδων!
""")

st.divider()

# =========================
# VEHICLE TYPE SELECTION
# =========================
st.header("🚙 Τύπος Οχήματος & Χρήσης")

vcol1, vcol2, vcol3 = st.columns(3)

with vcol1:
    vehicle_type = st.selectbox(
        "Τύπος Οχήματος",
        ["Συμβατικό (Βενζίνη/Πετρέλαιο)", "Υβριδικό (HEV)", "Plug-in Hybrid (PHEV)", "Ηλεκτρικό BEV (Μηδενικών Ρύπων)"],
        help="Για BEV ισχύει προσαύξηση 50% έως €40.000 και 25% για το υπερβάλλον"
    )

with vcol2:
    usage_type = st.selectbox(
        "Τύπος Χρήσης",
        ["ΙΧ Επιχείρησης", "Εταιρικό Όχημα (Pool)"],
        help="ΙΧ: εκπίπτει όλο το μίσθωμα με ΦΠΑ. Εταιρικό: εκπίπτει η καθαρή αξία"
    )

with vcol3:
    ltvp_vehicle = st.number_input(
        "ΛΤΠΦ Οχήματος (€)", 
        value=71693.55, 
        step=1000.0, 
        min_value=0.0,
        help="Λιανική Τιμή Προ Φόρων - για υπολογισμό προσαύξησης (π.χ. 88.900 / 1.24 = 71.693,55)"
    )

# Determine vehicle type
is_electric = vehicle_type == "Ηλεκτρικό BEV (Μηδενικών Ρύπων)"
is_phev = vehicle_type == "Plug-in Hybrid (PHEV)"

# Calculate enhancement rates based on LTVP
enhancement_50_pct = 0
enhancement_25_pct = 0

if is_electric and ltvp_vehicle > 0:
    if ltvp_vehicle <= 40000:
        enhancement_50_pct = 1.0  # 100% of payment gets 50% enhancement
        enhancement_25_pct = 0.0
    else:
        enhancement_50_pct = 40000 / ltvp_vehicle  # portion up to 40k
        enhancement_25_pct = 1 - enhancement_50_pct  # remaining portion

st.divider()

# =========================
# INPUTS - LEASING
# =========================
st.header("📌 Στοιχεία Leasing")

col1, col2, col3 = st.columns(3)

with col1:
    monthly_payment = st.number_input("Μηνιαίο Μίσθωμα (€)", value=770.0, step=10.0)

with col2:
    duration_months = st.number_input("Διάρκεια (μήνες)", value=60, step=1, min_value=1)

with col3:
    down_payment = st.number_input("Προκαταβολή (€)", value=30000.0, step=500.0, min_value=0.0)

# VAT calculation
vat_rate = 0.24
if usage_type == "ΙΧ Επιχείρησης":
    # Full amount including VAT is deductible
    monthly_payment_net = monthly_payment
    vat_amount = monthly_payment - (monthly_payment / (1 + vat_rate))
else:
    # Only net amount is deductible (VAT is offset)
    monthly_payment_net = monthly_payment / (1 + vat_rate)
    vat_amount = monthly_payment - monthly_payment_net

col4, col5 = st.columns(2)
with col4:
    buyout_price = st.number_input("Τιμή Εξαγοράς (€)", value=36000.0, step=500.0, min_value=0.0)

with col5:
    buyout_vat_included = st.checkbox("Η εξαγορά περιλαμβάνει ΦΠΑ", value=True)

st.divider()

# =========================
# INPUTS - LOAN COMPARISON
# =========================
st.header("🏦 Στοιχεία Δανείου (για σύγκριση)")

# Auto-calculate loan amount based on vehicle price
auto_loan = ltvp_vehicle * 1.24 - down_payment  # Full price with VAT minus down payment

lcol1, lcol2, lcol3 = st.columns(3)

with lcol1:
    loan_amount = st.number_input("Ποσό Δανείου (€)", value=auto_loan, step=1000.0, 
                                  help=f"Προτεινόμενο: {euro(auto_loan)} (Τιμή με ΦΠΑ - Προκαταβολή)")

with lcol2:
    loan_interest_rate = st.slider("Επιτόκιο Δανείου (%)", 0.0, 15.0, 6.5, step=0.1)

with lcol3:
    loan_duration = st.number_input("Διάρκεια Δανείου (μήνες)", value=60, step=12, min_value=12)

# Depreciation settings
st.subheader("📉 Αποσβέσεις")
dcol1, dcol2 = st.columns(2)

with dcol1:
    depreciation_rate = st.slider("Συντελεστής Απόσβεσης (%)", 0, 50, 25, help="Συνήθως 25% για ΙΧ")

with dcol2:
    residual_for_depreciation = st.number_input("Υπολειμματική Αξία (€)", value=0.0, step=1000.0, help="Αξία μετά την απόσβεση")

st.divider()

# =========================
# TAX SETTINGS
# =========================
st.header("🏛️ Φορολογικά (ρυθμίσεις)")

t1, t2 = st.columns(2)

with t1:
    tax_rate = st.slider("Φορολογικός συντελεστής", 0.0, 0.5, 0.22, step=0.01)

with t2:
    deductibility = st.slider("Έκπτωση εξόδων leasing (%)", 0, 100, 100, help="Πόσο % των εξόδων leasing εκπίπτει φορολογικά.")
    deductibility = deductibility / 100.0

st.caption(f"Tax benefit = Eligible amount × {pct(tax_rate*100)} × {pct(deductibility*100)}")

st.divider()

# =========================
# CALCULATIONS - LEASING
# =========================

# Annual leasing amounts
annual_payment = monthly_payment * 12
annual_payment_net = monthly_payment_net * 12
total_leasing_payments = monthly_payment * duration_months
total_leasing_cost = total_leasing_payments + down_payment

# Calculate enhancement for electric vehicles
annual_enhancement_50 = 0
annual_enhancement_25 = 0

if is_electric:
    # Portion subject to 50% enhancement
    annual_enhancement_50 = annual_payment_net * enhancement_50_pct * 0.50
    # Portion subject to 25% enhancement  
    annual_enhancement_25 = annual_payment_net * enhancement_25_pct * 0.25

# Total annual deduction for leasing
annual_leasing_deduction = annual_payment_net + annual_enhancement_50 + annual_enhancement_25
total_leasing_deduction = annual_leasing_deduction * (duration_months / 12)

# Tax benefit from leasing
tax_benefit_leasing = total_leasing_deduction * tax_rate * deductibility
net_cost_leasing = total_leasing_cost - tax_benefit_leasing

# =========================
# CALCULATIONS - LOAN
# =========================

# Monthly loan payment calculation
monthly_rate = (loan_interest_rate / 100) / 12
if monthly_rate > 0:
    monthly_loan_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**loan_duration) / ((1 + monthly_rate)**loan_duration - 1)
else:
    monthly_loan_payment = loan_amount / loan_duration

total_loan_payments = monthly_loan_payment * loan_duration
total_interest_paid = total_loan_payments - loan_amount

# Depreciation calculation
depreciable_amount = ltvp_vehicle - residual_for_depreciation
annual_depreciation = depreciable_amount * (depreciation_rate / 100)
years_of_depreciation = min(5, math.ceil((ltvp_vehicle - residual_for_depreciation) / annual_depreciation)) if annual_depreciation > 0 else 0

# Total deductions for loan (depreciation + interest)
# For 5 years comparison
total_depreciation_5y = min(annual_depreciation * 5, depreciable_amount)
total_interest_5y = total_interest_paid  # Assuming loan duration <= 5 years

# Tax benefit from loan
tax_benefit_loan = (total_depreciation_5y + total_interest_5y) * tax_rate
net_cost_loan = down_payment + total_loan_payments - tax_benefit_loan + residual_for_depreciation

# Total vehicle cost for loan (to compare with leasing buyout)
total_vehicle_cost_loan = down_payment + total_loan_payments

# =========================
# COMPARISON RESULTS
# =========================
st.divider()
st.header("📊 Σύγκριση Leasing vs Δάνειο")

# Create comparison table
comparison_data = {
    "Στοιχείο": [
        "Συνολικό Κόστος (με εξαγορά)",
        "Φορολογικά Εκπιπτέα Ποσά",
        "Φορολογικό Όφελος",
        "Καθαρό Κόστος μετά Φόρου",
        "Κόστος ανά έτος"
    ],
    "Leasing": [
        euro(total_leasing_cost + buyout_price),
        euro(total_leasing_deduction),
        euro(tax_benefit_leasing),
        euro(net_cost_leasing + buyout_price),
        euro((net_cost_leasing + buyout_price) / 5)
    ],
    "Δάνειο": [
        euro(total_vehicle_cost_loan),
        euro(total_depreciation_5y + total_interest_5y),
        euro(tax_benefit_loan),
        euro(net_cost_loan),
        euro(net_cost_loan / 5)
    ]
}

st.table(comparison_data)

# Winner announcement
st.subheader("🏆 Αποτέλεσμα Σύγκρισης")

savings = (net_cost_loan) - (net_cost_leasing + buyout_price)

if savings > 1000:
    st.success(f"""
    🟢 **Το Leasing συμφέρει!**
    
    Καθαρό όφελος: **{euro(abs(savings))}** σε 5 χρόνια
    ({euro(abs(savings)/5)}/έτος)
    """)
elif savings < -1000:
    st.error(f"""
    🔴 **Το Δάνειο συμφέρει!**
    
    Καθαρό όφελος: **{euro(abs(savings))}** σε 5 χρόνια
    ({euro(abs(savings)/5)}/έτος)
    """)
else:
    st.warning(f"""
    🟡 **Οριακή διαφορά** μεταξύ Leasing και Δανείου
    
    Διαφορά: **{euro(abs(savings))}** σε 5 χρόνια
    """)

st.divider()

# =========================
# DETAILED LEASING BREAKDOWN
# =========================
st.header("📋 Αναλυτική Ανάλυση Leasing")

r1, r2, r3, r4 = st.columns(4)

r1.metric("Συνολικά Μισθώματα", euro(total_leasing_payments))
r2.metric("Συνολικό Κόστος Leasing", euro(total_leasing_cost))
r3.metric("Φορολογικό Όφελος", euro(tax_benefit_leasing))
r4.metric("Καθαρό Κόστος", euro(net_cost_leasing))

# Show enhancement details if electric
if is_electric:
    st.subheader("⚡ Προσαύξηση για Ηλεκτρικό (BEV)")
    
    enh_col1, enh_col2, enh_col3, enh_col4 = st.columns(4)
    
    with enh_col1:
        st.metric("Ποσοστό με 50%", pct(enhancement_50_pct * 100))
    with enh_col2:
        st.metric("Ποσοστό με 25%", pct(enhancement_25_pct * 100))
    with enh_col3:
        st.metric("Ετήσια Προσαύξη 50%", euro(annual_enhancement_50))
    with enh_col4:
        st.metric("Ετήσια Προσαύξη 25%", euro(annual_enhancement_25))
    
    st.info(f"""
    **Υπολογισμός Προσαύξησης:**
    - ΛΤΠΦ: {euro(ltvp_vehicle)}
    - Έως €40.000 ({pct(enhancement_50_pct * 100)}): {euro(annual_payment_net * enhancement_50_pct)} × 50% = **{euro(annual_enhancement_50)}/έτος**
    - Υπερβάλλον ({pct(enhancement_25_pct * 100)}): {euro(annual_payment_net * enhancement_25_pct)} × 25% = **{euro(annual_enhancement_25)}/έτος**
    - **Βασική έκπτωση**: {euro(annual_payment_net)}/έτος
    - **Σύνολο ετήσιας έκπτωσης**: **{euro(annual_leasing_deduction)}/έτος**
    - **Σύνολο 5ετίας**: **{euro(total_leasing_deduction)}**
    """)
else:
    st.info(f"""
    **Ετήσια Έκπτωση Leasing:** {euro(annual_leasing_deduction)}
    **Σύνολο 5ετίας:** {euro(total_leasing_deduction)}
    """)

st.divider()

# =========================
# DETAILED LOAN BREAKDOWN
# =========================
st.header("📋 Αναλυτική Ανάλυση Δανείου")

l1, l2, l3, l4 = st.columns(4)

l1.metric("Μηνιαία Δόση", euro(monthly_loan_payment))
l2.metric("Συνολικοί Τόκοι", euro(total_interest_paid))
l3.metric("Αποσβέσεις 5ετίας", euro(total_depreciation_5y))
l4.metric("Φορολογικό Όφελος", euro(tax_benefit_loan))

st.info(f"""
**Απόσβεση:** {euro(annual_depreciation)}/έτος ({depreciation_rate}% επί {euro(depreciable_amount)})
**Διάρκεια αποσβέσεων:** {years_of_depreciation} έτη
**Σύνολο εκπιπτέων (αποσβέσεις + τόκοι):** {euro(total_depreciation_5y + total_interest_5y)}
""")

st.divider()

# =========================
# BUYOUT ANALYSIS
# =========================
st.header("💡 Ανάλυση Εξαγοράς Leasing")

# Market value estimation
st.subheader("📉 Αναμενόμενη Αξία Αγοράς")
residual_pct = st.slider("Residual % σε 5 χρόνια", min_value=20, max_value=60, value=40)
expected_market_value = ltvp_vehicle * (residual_pct / 100)

st.info(f"📌 Αναμενόμενη Αξία Αγοράς σε 5 χρόνια: **{euro(expected_market_value)}**")

difference = expected_market_value - buyout_price
verdict_threshold_pct = 5
threshold = expected_market_value * (verdict_threshold_pct / 100.0)

if difference > threshold:
    st.success(f"""
    🟢 Συμφέρει η εξαγορά!
    
    - Buyout: **{euro(buyout_price)}**
    - Market (expected): **{euro(expected_market_value)}**
    - Κέρδος: **{euro(difference)}**
    """)
elif -threshold <= difference <= threshold:
    st.warning(f"""
    🟡 Οριακή περίπτωση εξαγοράς.
    
    - Buyout: **{euro(buyout_price)}**
    - Market (expected): **{euro(expected_market_value)}**
    - Διαφορά: **{euro(difference)}**
    """)
else:
    st.error(f"""
    🔴 Δεν συμφέρει η εξαγορά.
    
    - Buyout: **{euro(buyout_price)}**
    - Market (expected): **{euro(expected_market_value)}**
    - Ζημιά: **{euro(abs(difference))}**
    """)

st.divider()

# =========================
# SENSITIVITY ANALYSIS
# =========================
st.subheader("📈 Sensitivity: Residual % vs Απόφαση Εξαγοράς")

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
        mv = ltvp_vehicle * (rp / 100.0)
        diff = mv - buyout_price
        label = "🟢 Buy" if diff > threshold else ("🟡 Borderline" if -threshold <= diff <= threshold else "🔴 No")
        rows.append({"Residual %": f"{rp}%", "Expected Value": euro(mv), "Equity": euro(diff), "Verdict": label})
        rp += sens_step

    st.table(rows)

# Chart
st.markdown("### 📉 Chart: Residual % → Equity")
chart_data = {
    "Residual %": [],
    "Equity (€)": []
}
rp = sens_min
while rp <= sens_max:
    mv = ltvp_vehicle * (rp / 100.0)
    diff = mv - buyout_price
    chart_data["Residual %"].append(rp)
    chart_data["Equity (€)"].append(diff)
    rp += sens_step

st.line_chart(chart_data, x="Residual %", y="Equity (€)")

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

Με βάση εκτίμηση αγοραίας αξίας σε 5 χρόνια (residual {residual_pct}% επί της σημερινής αξίας {euro(ltvp_vehicle)}),
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

# Report export
from datetime import date
today = date.today().strftime("%d/%m/%Y")

report_text = f"""
Leasing vs Loan Analyzer Report
===============================
ΗΜΕΡΟΜΗΝΙΑ: {today}

--- ΣΤΟΙΧΕΙΑ ΟΧΗΜΑΤΟΣ ---
Τύπος: {vehicle_type}
Χρήση: {usage_type}
ΛΤΠΦ: {euro(ltvp_vehicle)}

--- LEASING ---
Μηνιαίο μίσθωμα: {euro(monthly_payment)}
Διάρκεια: {duration_months} μήνες
Προκαταβολή: {euro(down_payment)}
Τιμή εξαγοράς: {euro(buyout_price)}
Συνολικά μισθώματα: {euro(total_leasing_payments)}
Συνολικό κόστος leasing: {euro(total_leasing_cost)}

Φορολογικά οφέλη Leasing:
- Βασική έκπτωση: {euro(annual_payment_net * (duration_months/12))}
- Προσαύξηση 50%: {euro(annual_enhancement_50 * (duration_months/12)) if is_electric else "N/A"}
- Προσαύξηση 25%: {euro(annual_enhancement_25 * (duration_months/12)) if is_electric else "N/A"}
- Σύνολο εκπιπτέων: {euro(total_leasing_deduction)}
- Φορολογικό όφελος: {euro(tax_benefit_leasing)}
- Καθαρό κόστος leasing: {euro(net_cost_leasing)}
- Κόστος με εξαγορά: {euro(net_cost_leasing + buyout_price)}

--- ΔΑΝΕΙΟ ---
Ποσό δανείου: {euro(loan_amount)}
Επιτόκιο: {loan_interest_rate}%
Διάρκεια: {loan_duration} μήνες
Μηνιαία δόση: {euro(monthly_loan_payment)}
Συνολικοί τόκοι: {euro(total_interest_paid)}

Φορολογικά οφέλη Δανείου:
- Αποσβέσεις 5ετίας: {euro(total_depreciation_5y)}
- Τόκοι: {euro(total_interest_5y)}
- Σύνολο εκπιπτέων: {euro(total_depreciation_5y + total_interest_5y)}
- Φορολογικό όφελος: {euro(tax_benefit_loan)}
- Καθαρό κόστος: {euro(net_cost_loan)}

--- ΣΥΓΚΡΙΣΗ ---
Leasing (με εξαγορά): {euro(net_cost_leasing + buyout_price)}
Δάνειο: {euro(net_cost_loan)}
Διαφορά: {euro(abs(savings))}
Συνιστώμενη επιλογή: {"Leasing" if savings > 0 else "Δάνειο" if savings < 0 else "Οριακή"}

--- ΕΞΑΓΟΡΑ ---
Τιμή εξαγοράς: {euro(buyout_price)}
Αναμενόμενη αξία ({residual_pct}%): {euro(expected_market_value)}
Διαφορά: {euro(difference)}
Συνιστάται εξαγορά: {"ΝΑΙ" if difference > threshold else "ΟΡΙΑΚΑ" if -threshold <= difference <= threshold else "ΟΧΙ"}
"""

st.download_button("📄 Κατέβασε Report (TXT)", report_text, file_name="leasing_vs_loan_report.txt")
st.download_button("📄 Κατέβασε Email (TXT)", email_text, file_name="leasing_email.txt")   