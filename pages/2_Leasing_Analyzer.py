import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Leasing vs Loan Analyzer",
    layout="wide"
)

HTML_CODE = """
<!DOCTYPE html>
<html lang="el">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Leasing vs Αγορά με Δάνειο - Πλήρης Σύγκριση</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
* {margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;max-width:1200px;margin:0 auto;padding:20px;background:#f5f5f5}
.container{background:white;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,0.3);overflow:hidden}
.header{background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:30px;text-align:center}
.header h1{font-size:2.5em;margin-bottom:10px}
.content{padding:30px}
.section{margin-bottom:30px;padding:20px;background:#f8f9fa;border-radius:15px;border-left:5px solid #667eea}
.section h2{color:#333;margin-bottom:20px;display:flex;align-items:center;gap:10px}
.section h3{color:#555;margin:20px 0 15px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px}
.form-group{margin-bottom:15px}
.form-group label{display:block;margin-bottom:5px;font-weight:600;color:#444}
.form-group input,.form-group select{width:100%;padding:12px;border:2px solid #ddd;border-radius:8px;font-size:16px}
.form-group input:focus,.form-group select:focus{outline:none;border-color:#667eea}
.form-group small{color:#888;font-size:0.85em}
.input-preview{color:#667eea;font-weight:bold;font-size:0.9em;margin-top:5px}
.checkbox-group{display:flex;align-items:center;gap:10px;margin:10px 0}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin:20px 0}
.metric-card{background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:20px;border-radius:12px;text-align:center}
.metric-card h4{font-size:0.9em;opacity:0.9;margin-bottom:10px}
.metric-card .value{font-size:1.8em;font-weight:bold}
.result-box{padding:25px;border-radius:12px;margin:20px 0;text-align:center}
.result-success{background:linear-gradient(135deg,#11998e,#38ef7d);color:white}
.result-error{background:linear-gradient(135deg,#eb3349,#f45c43);color:white}
.result-warning{background:linear-gradient(135deg,#f093fb,#f5576c);color:white}
.info-box{background:#e3f2fd;border-left:4px solid #2196f3;padding:15px;border-radius:8px;margin:15px 0}
.calculation-box{background:#fff3e0;border:2px solid #ff9800;border-radius:12px;padding:20px;margin:15px 0}
.calculation-box h4{color:#e65100;margin-bottom:15px;font-size:1.1em}
.calc-step{background:white;border-radius:8px;padding:15px;margin:10px 0;border-left:4px solid #ff9800}
.calc-step h5{color:#e65100;margin-bottom:10px;font-size:1em}
.calc-step p{margin:5px 0;font-family:'Courier New',monospace;font-size:0.95em}
.calc-step .result{background:#e8f5e9;padding:10px;border-radius:5px;margin-top:10px;font-weight:bold;color:#2e7d32}
.formula{background:#f5f5f5;padding:10px 15px;border-radius:5px;font-family:'Courier New',monospace;margin:10px 0;border-left:3px solid #667eea}
.comparison-table{width:100%;border-collapse:collapse;margin:20px 0}
.comparison-table th,.comparison-table td{padding:15px;text-align:left;border-bottom:1px solid #ddd}
.comparison-table th{background:#667eea;color:white}
.comparison-table tr:hover{background:#f5f5f5}
.btn{background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:15px 30px;border:none;border-radius:8px;cursor:pointer;font-size:16px;margin:5px}
.btn:hover{transform:translateY(-2px);box-shadow:0 5px 20px rgba(102,126,234,0.4)}
.btn-small{padding:8px 15px;font-size:0.9em}
.sensitivity-table{width:100%;border-collapse:collapse}
.sensitivity-table th,.sensitivity-table td{padding:12px;text-align:center;border:1px solid #ddd}
.badge{display:inline-block;padding:5px 12px;border-radius:20px;font-size:0.85em;font-weight:bold}
.badge-green{background:#28a745;color:white}
.badge-yellow{background:#ffc107;color:#333}
.badge-red{background:#dc3545;color:white}
.divider{height:2px;background:linear-gradient(90deg,transparent,#667eea,transparent);margin:30px 0}
.highlight{background:#fff59d;padding:2px 5px;border-radius:3px}
.note{background:#e8f5e9;border-left:4px solid #4caf50;padding:15px;border-radius:8px;margin:15px 0}
.warning-note{background:#ffebee;border-left:4px solid #f44336;padding:15px;border-radius:8px;margin:15px 0}
.auto-calc-box{background:#f3e5f5;border:2px solid #9c27b0;border-radius:12px;padding:20px;margin:15px 0}
.auto-calc-box h4{color:#7b1fa2;margin-bottom:15px}
.slider-container{margin:15px 0}
.slider-container input[type="range"]{width:100%;margin:10px 0}
.slider-labels{display:flex;justify-content:space-between;font-size:0.85em;color:#666}
.chart-container{background:white;padding:20px;border-radius:12px;margin:20px 0;box-shadow:0 2px 10px rgba(0,0,0,0.1)}
textarea{width:100%;min-height:200px;padding:15px;border:2px solid #ddd;border-radius:8px;font-family:monospace;resize:vertical}
</style>
</head>
<body>
<div class="container">
<div class="header">
<h1>🚗 Leasing vs Αγορά με Δάνειο</h1>
<p>Πλήρης σύγκριση με όλα τα έξοδα</p>
</div>

<div class="content">
<!-- Vehicle Type Section -->
<div class="section">
<h2>🚙 Τύπος Οχήματος & Χρήσης</h2>
<div class="grid">
<div class="form-group">
<label for="vehicleType">Τύπος Οχήματος</label>
<select id="vehicleType" onchange="calculateAll()">
<option value="conventional">Συμβατικό (Βενζίνη/Πετρέλαιο)</option>
<option value="hev">Υβριδικό (HEV)</option>
<option value="phev">Plug-in Hybrid (PHEV)</option>
<option value="bev" selected>Ηλεκτρικό BEV (Μηδενικών Ρύπων)</option>
</select>
</div>
<div class="form-group">
<label for="usageType">Τύπος Χρήσης</label>
<select id="usageType" onchange="calculateAll()">
<option value="ix" selected>ΙΧ Επιχείρησης</option>
<option value="corporate">Εταιρικό Όχημα (Pool)</option>
</select>
</div>
<div class="form-group">
<label for="ltvp">ΛΤΠΦ Οχήματος (€)</label>
<input type="number" id="ltvp" value="71693.55" step="1000" onchange="updateInputPreview('ltvp'); calculateAll()">
<div class="input-preview" id="ltvp-preview">€71.693,55</div>
</div>
</div>
</div>

<!-- AUTO CALCULATION RESIDUAL VALUE SECTION -->
<div class="section">
<h2>🔮 Αυτόματη Εκτίμηση Υπολειμματικής Αξίας</h2>
<div class="auto-calc-box">
<h4>📊 Εκτίμηση με βάση τον τύπο οχήματος και τα χρόνια</h4>
<div class="grid">
<div class="form-group">
<label for="residualYears">Χρόνια για εκτίμηση υπολειμματικής</label>
<input type="number" id="residualYears" value="8" min="1" max="20" onchange="updateInputPreview('residualYears'); calculateAll()">
<div class="input-preview" id="residualYears-preview">8 έτη</div>
</div>
<div class="form-group">
<label for="marketCondition">Κατάσταση Αγοράς</label>
<select id="marketCondition" onchange="calculateAll()">
<option value="optimistic">Αισιόδοξο σενάριο</option>
<option value="normal" selected>Κανονική αγορά</option>
<option value="pessimistic">Απαισιόδοξο σενάριο</option>
</select>
</div>
</div>
<div class="slider-container">
<label>Προσαρμογή ετήσιας απόσβεσης: <span id="depreciationRateDisplay">20%</span></label>
<input type="range" id="customDepreciation" min="10" max="35" value="20" oninput="updateDepreciationDisplay(this.value); calculateAll()">
<div class="slider-labels">
<span>10% (αργή)</span>
<span>22.5%</span>
<span>35% (γρήγορη)</span>
</div>
</div>
<div class="metrics" style="margin-top:20px">
<div class="metric-card" style="background:linear-gradient(135deg,#9c27b0,#e91e63)">
<h4>Εκτιμώμενη Υπολειμματική</h4>
<div class="value" id="estimatedResidual">-</div>
</div>
<div class="metric-card" style="background:linear-gradient(135deg,#009688,#4caf50)">
<h4>Ποσοστό Αξίας</h4>
<div class="value" id="residualPercentage">-</div>
</div>
<div class="metric-card" style="background:linear-gradient(135deg,#ff9800,#ff5722)">
<h4>Μέση Ετήσια Απόσβεση</h4>
<div class="value" id="avgAnnualDepreciation">-</div>
</div>
</div>
<div class="info-box" id="residualCalculationDetails"></div>
<button class="btn btn-small" onclick="applyEstimatedResidual()">✓ Χρήση αυτής της εκτίμησης στις αποσβέσεις</button>
</div>
</div>

<!-- Leasing Section -->
<div class="section">
<h2>📌 Στοιχεία Leasing</h2>
<div class="grid">
<div class="form-group">
<label for="monthlyPayment">Μηνιαίο Μίσθωμα (€)</label>
<input type="number" id="monthlyPayment" value="770" step="10" onchange="updateInputPreview('monthlyPayment'); calculateAll()">
<div class="input-preview" id="monthlyPayment-preview">€770</div>
</div>
<div class="form-group">
<label for="durationMonths">Διάρκεια (μήνες)</label>
<input type="number" id="durationMonths" value="60" step="1" min="1" onchange="updateInputPreview('durationMonths'); calculateAll()">
<div class="input-preview" id="durationMonths-preview">60 μήνες (5 έτη)</div>
</div>
<div class="form-group">
<label for="downPaymentLeasing">Προκαταβολή Leasing (€)</label>
<input type="number" id="downPaymentLeasing" value="30000" step="500" min="0" onchange="updateInputPreview('downPaymentLeasing'); calculateAll()">
<div class="input-preview" id="downPaymentLeasing-preview">€30.000</div>
</div>
<div class="form-group">
<label for="buyoutPrice">Τιμή Εξαγοράς (€)</label>
<input type="number" id="buyoutPrice" value="36000" step="500" min="0" onchange="updateInputPreview('buyoutPrice'); calculateAll()">
<div class="input-preview" id="buyoutPrice-preview">€36.000</div>
</div>
</div>
</div>

<!-- Loan Section -->
<div class="section">
<h2>🏦 Στοιχεία Αγοράς με Δάνειο</h2>
<div class="grid">
<div class="form-group">
<label for="downPaymentLoan">Προκαταβολή Αγοράς (€)</label>
<input type="number" id="downPaymentLoan" value="30000" step="500" min="0" onchange="updateInputPreview('downPaymentLoan'); calculateAll()">
<div class="input-preview" id="downPaymentLoan-preview">€30.000</div>
</div>
<div class="form-group">
<label for="loanAmount">Ποσό Δανείου (€)</label>
<input type="number" id="loanAmount" value="58818" step="1000" onchange="updateInputPreview('loanAmount'); calculateAll()">
<div class="input-preview" id="loanAmount-preview">€58.818</div>
</div>
<div class="form-group">
<label for="loanInterest">Επιτόκιο Δανείου (%)</label>
<input type="number" id="loanInterest" value="9.5" step="0.1" min="0" max="20" onchange="updateInputPreview('loanInterest'); calculateAll()">
<div class="input-preview" id="loanInterest-preview">9,5%</div>
</div>
<div class="form-group">
<label for="loanDuration">Διάρκεια Δανείου (μήνες)</label>
<input type="number" id="loanDuration" value="60" step="12" min="12" onchange="updateInputPreview('loanDuration'); calculateAll()">
<div class="input-preview" id="loanDuration-preview">60 μήνες (5 έτη)</div>
</div>
</div>
<h3>📉 Αποσβέσεις</h3>
<div class="grid">
<div class="form-group">
<label for="depreciationRate">Συντελεστής Απόσβεσης (%)</label>
<input type="number" id="depreciationRate" value="25" step="1" min="0" max="50" onchange="updateInputPreview('depreciationRate'); calculateAll()">
<div class="input-preview" id="depreciationRate-preview">25%</div>
</div>
<div class="form-group">
<label for="residualValue">Υπολειμματική Αξία Οχήματος (€)</label>
<input type="number" id="residualValue" value="0" step="1000" onchange="updateInputPreview('residualValue'); calculateAll()">
<div class="input-preview" id="residualValue-preview">€0</div>
</div>
</div>
<h3>🛡️ Επιπλέον Έξοδα Αγοράς (ετησίως)</h3>
<div class="grid">
<div class="form-group">
<label for="annualInsurance">Ασφάλεια (€/έτος)</label>
<input type="number" id="annualInsurance" value="800" step="50" onchange="updateInputPreview('annualInsurance'); calculateAll()">
<div class="input-preview" id="annualInsurance-preview">€800/έτος</div>
</div>
<div class="form-group">
<label for="annualService">Service/Sυντήρηση (€/έτος)</label>
<input type="number" id="annualService" value="600" step="50" onchange="updateInputPreview('annualService'); calculateAll()">
<div class="input-preview" id="annualService-preview">€600/έτος</div>
</div>
</div>
<div class="info-box">
<strong>Σημείωση:</strong> Τα έξοδα ασφάλειας και service προστίθενται μόνο στην αγορά με δάνειο. Στο leasing, αυτά τα έξοδα καλύπτονται από τη μισθωτική εταιρεία.
</div>
</div>

<!-- Tax Settings -->
<div class="section">
<h2>🏛️ Φορολογικά (ρυθμίσεις)</h2>
<div class="grid">
<div class="form-group">
<label for="taxRate">Φορολογικός συντελεστής</label>
<input type="number" id="taxRate" value="0.22" step="0.01" min="0" max="0.5" onchange="updateInputPreview('taxRate'); calculateAll()">
<div class="input-preview" id="taxRate-preview">22%</div>
</div>
<div class="form-group">
<label for="deductibility">Έκπτωση εξόδων leasing (%)</label>
<input type="number" id="deductibility" value="100" step="1" min="0" max="100" onchange="updateInputPreview('deductibility'); calculateAll()">
<div class="input-preview" id="deductibility-preview">100%</div>
</div>
</div>
</div>

<div class="divider"></div>

<!-- Comparison Results -->
<div class="section">
<h2>📊 Σύγκριση Leasing vs Αγορά με Δάνειο</h2>
<table class="comparison-table">
<thead>
<tr><th>Στοιχείο</th><th>Leasing</th><th>Αγορά με Δάνειο</th></tr>
</thead>
<tbody>
<tr><td>Συνολικό Κόστος Απόκτησης</td><td id="compLeasingTotal">-</td><td id="compLoanTotal">-</td></tr>
<tr><td>Έξοδα Ασφάλειας (5ετία)</td><td id="compLeasingInsurance">-</td><td id="compLoanInsurance">-</td></tr>
<tr><td>Έξοδα Service (5ετία)</td><td id="compLeasingService">-</td><td id="compLoanService">-</td></tr>
<tr><td>Σύνολο Εξόδων</td><td id="compLeasingAllCosts">-</td><td id="compLoanAllCosts">-</td></tr>
<tr><td>Φορολογικά Εκπιπτέα Ποσά</td><td id="compLeasingDeduction">-</td><td id="compLoanDeduction">-</td></tr>
<tr><td>Φορολογικό Όφελος</td><td id="compLeasingTaxBenefit">-</td><td id="compLoanTaxBenefit">-</td></tr>
<tr><td><strong>ΚΑΘΑΡΟ ΣΥΝΟΛΙΚΟ ΚΟΣΤΟΣ</strong></td><td id="compLeasingNet" style="font-weight:bold">-</td><td id="compLoanNet" style="font-weight:bold">-</td></tr>
<tr><td>Κόστος ανά έτος</td><td id="compLeasingAnnual">-</td><td id="compLoanAnnual">-</td></tr>
</tbody>
</table>
<div id="winnerResult" class="result-box"></div>
</div>

<div class="divider"></div>

<!-- DETAILED CALCULATIONS SECTION -->
<div class="section">
<h2>🔍 Αναλυτική Ανάλυση Υπολογισμών</h2>

<!-- Leasing Calculations -->
<div class="calculation-box">
<h4>📋 Υπολογισμός Leasing</h4>
<div class="calc-step">
<h5>Βήμα 1: Ετήσιο Μίσθωμα</h5>
<p id="calcLeasingStep1">-</p>
</div>
<div class="calc-step" id="calcLeasingVatStep">
<h5>Βήμα 2: Μεταχείριση ΦΠΑ</h5>
<p id="calcLeasingVatDetail">-</p>
</div>
<div class="calc-step" id="calcEnhancementStep" style="display:none">
<h5>Βήμα 3: Προσαύξηση BEV (50% + 25%)</h5>
<p id="calcEnhancementDetail">-</p>
</div>
<div class="calc-step">
<h5>Βήμα 4: Συνολική Ετήσια Έκπτωση</h5>
<p id="calcLeasingDeduction">-</p>
<div class="result" id="calcLeasingDeductionResult">-</div>
</div>
<div class="calc-step">
<h5>Βήμα 5: Συνολική Έκπτωση Περιόδου</h5>
<p id="calcLeasingPeriod">-</p>
</div>
<div class="calc-step">
<h5>Βήμα 6: Φορολογικό Όφελος Leasing</h5>
<p id="calcLeasingTaxBenefitDetail">-</p>
<div class="result" id="calcLeasingTaxBenefitResult">-</div>
</div>
<div class="calc-step">
<h5>Βήμα 7: Κόστος Απόκτησης Leasing</h5>
<p>(Συνολικά μισθώματα + Προκαταβολή + Εξαγορά)</p>
<p id="calcLeasingAcquisition">-</p>
</div>
<div class="calc-step">
<h5>Βήμα 8: Καθαρό Κόστος Leasing</h5>
<p>Κόστος απόκτησης - Φορολογικό όφελος</p>
<p id="calcLeasingNetDetail">-</p>
<div class="result" id="calcLeasingNetResult">-</div>
</div>
</div>

<!-- Loan Calculations -->
<div class="calculation-box">
<h4>🏦 Υπολογισμός Αγοράς με Δάνειο</h4>
<div class="calc-step">
<h5>Βήμα 1: Μηνιαία Δόση Δανείου</h5>
<div class="formula">M = P × [r(1+r)^n] / [(1+r)^n - 1]</div>
<p id="calcLoanStep1">-</p>
</div>
<div class="calc-step">
<h5>Βήμα 2: Συνολικοί Τόκοι Δανείου</h5>
<p id="calcLoanInterest">-</p>
<div class="result" id="calcLoanInterestResult">-</div>
</div>
<div class="calc-step">
<h5>Βήμα 3: Συνολικές Πληρωμές Δανείου</h5>
<p id="calcLoanTotalPaid">-</p>
</div>
<div class="calc-step">
<h5>Βήμα 4: Κόστος Απόκτησης (προκαταβολή + δόσεις)</h5>
<p id="calcLoanAcquisition">-</p>
</div>
<div class="calc-step">
<h5>Βήμα 5: Έξοδα Ασφάλειας (5ετία)</h5>
<p id="calcInsuranceDetail">-</p>
</div>
<div class="calc-step">
<h5>Βήμα 6: Έξοδα Service (5ετία)</h5>
<p id="calcServiceDetail">-</p>
</div>
<div class="calc-step">
<h5>Βήμα 7: Σύνολο Εξόδων Αγοράς</h5>
<p id="calcTotalExpenses">-</p>
<div class="result" id="calcTotalExpensesResult">-</div>
</div>
<div class="calc-step">
<h5>Βήμα 8: Ετήσια Απόσβεση</h5>
<p id="calcDepreciation">-</p>
</div>
<div class="calc-step">
<h5>Βήμα 9: Συνολικές Αποσβέσεις 5ετίας</h5>
<p id="calcDepreciation5y">-</p>
</div>
<div class="calc-step">
<h5>Βήμα 10: Συνολικά Εκπιπτέα Ποσά</h5>
<p>Αποσβέσεις + Τόκοι</p>
<p id="calcLoanDeduction">-</p>
<div class="result" id="calcLoanDeductionResult">-</div>
</div>
<div class="calc-step">
<h5>Βήμα 11: Φορολογικό Όφελος Αγοράς</h5>
<p id="calcLoanTaxBenefitDetail">-</p>
<div class="result" id="calcLoanTaxBenefitResult">-</div>
</div>
<div class="calc-step">
<h5>Βήμα 12: Καθαρό Κόστος Αγοράς</h5>
<p>Σύνολο εξόδων - Φορολογικό όφελος</p>
<p id="calcLoanNetDetail">-</p>
<div class="result" id="calcLoanNetResult">-</div>
</div>
</div>

<!-- Final Comparison -->
<div class="calculation-box" style="background:#e8f5e9;border-color:#4caf50">
<h4 style="color:#2e7d32">🏆 Τελική Σύγκριση</h4>
<div class="calc-step">
<h5>Υπολογισμός Διαφοράς</h5>
<p>Καθαρό κόστος Leasing - Καθαρό κόστος Αγοράς</p>
<p id="calcFinalComparison">-</p>
<div class="result" id="calcFinalResult" style="background:#c8e6c9;color:#1b5e20">-</div>
</div>
<div class="note">
<strong>💡 Ερμηνεία:</strong>
<ul style="margin:10px 0 0 20px">
<li><span class="highlight">Θετική διαφορά</span> = Το Leasing είναι ακριβότερο → <strong>Η Αγορά συμφέρει</strong></li>
<li><span class="highlight">Αρνητική διαφορά</span> = Η Αγορά είναι ακριβότερη → <strong>Το Leasing συμφέρει</strong></li>
<li><span class="highlight">Κοντά στο μηδέν</span> = Οριακή διαφορά</li>
</ul>
</div>
</div>
</div>

<div class="divider"></div>

<!-- Summary Results -->
<div class="section">
<h2>📋 Συνοπτικά Αποτελέσματα</h2>
<h3>Leasing</h3>
<div class="metrics">
<div class="metric-card"><h4>Συνολικά Μισθώματα</h4><div class="value" id="leasingPayments">-</div></div>
<div class="metric-card"><h4>Συνολικό Κόστος</h4><div class="value" id="leasingTotalCost">-</div></div>
<div class="metric-card"><h4>Φορολογικό Όφελος</h4><div class="value" id="leasingTaxBenefit">-</div></div>
<div class="metric-card"><h4>Καθαρό Κόστος</h4><div class="value" id="leasingNetCost">-</div></div>
</div>
<div id="enhancementDetails" style="display:none">
<h3>⚡ Προσαύξηση BEV</h3>
<div class="metrics">
<div class="metric-card"><h4>Ποσοστό 50%</h4><div class="value" id="enh50pct">-</div></div>
<div class="metric-card"><h4>Ποσοστό 25%</h4><div class="value" id="enh25pct">-</div></div>
<div class="metric-card"><h4>Ετήσια Προσαύξη 50%</h4><div class="value" id="enh50amount">-</div></div>
<div class="metric-card"><h4>Ετήσια Προσαύξη 25%</h4><div class="value" id="enh25amount">-</div></div>
</div>
<div class="info-box" id="enhancementCalc"></div>
</div>

<h3>Αγορά με Δάνειο</h3>
<div class="metrics">
<div class="metric-card"><h4>Μηνιαία Δόση</h4><div class="value" id="loanMonthly">-</div></div>
<div class="metric-card"><h4>Συνολικοί Τόκοι</h4><div class="value" id="loanInterestTotal">-</div></div>
<div class="metric-card"><h4>Έξοδα Ασφάλειας/Service</h4><div class="value" id="loanExtraCosts">-</div></div>
<div class="metric-card"><h4>Φορολογικό Όφελος</h4><div class="value" id="loanTaxBenefit2">-</div></div>
</div>
<div class="info-box" id="loanDetails"></div>
</div>

<div class="divider"></div>

<!-- Email Generator -->
<div class="section">
<h2>✉️ Email</h2>
<div class="grid">
<div class="form-group"><label for="companyName">Όνομα Εταιρείας</label><input type="text" id="companyName" value="(εταιρεία)" onchange="generateEmail()"></div>
<div class="form-group"><label for="clientName">Το όνομά σου</label><input type="text" id="clientName" value="Panagiotis ..." onchange="generateEmail()"></div>
</div>
<textarea id="emailText" readonly></textarea><br><br>
<button class="btn" onclick="copyEmail()">📋 Αντιγραφή Email</button>
<button class="btn" style="background:#6c757d" onclick="downloadReport()">📄 Κατέβασε Report</button>
</div>
</div>
</div>

<script>
// Custom function for Greek number format with dot as thousands separator
function euro(x){
if(isNaN(x) || x === null || x === undefined) return '€0';
var num = Math.round(x);
var str = num.toString();
var result = '';
var count = 0;
for(var i = str.length - 1; i >= 0; i--){
if(count > 0 && count % 3 === 0){
result = '.' + result;
}
result = str[i] + result;
count++;
}
return '€' + result;
}

function formatNumber(x){
if(isNaN(x) || x === null || x === undefined) return '0';
var num = Math.round(x);
var str = num.toString();
var result = '';
var count = 0;
for(var i = str.length - 1; i >= 0; i--){
if(count > 0 && count % 3 === 0){
result = '.' + result;
}
result = str[i] + result;
count++;
}
return result;
}

function pct(x){return Math.round(x)+'%'}

function updateInputPreview(id){
var input = document.getElementById(id);
var value = parseFloat(input.value) || 0;
var preview = document.getElementById(id + '-preview');
if(!preview) return;

switch(id){
case 'ltvp':
case 'monthlyPayment':
case 'downPaymentLeasing':
case 'buyoutPrice':
case 'downPaymentLoan':
case 'loanAmount':
case 'residualValue':
case 'annualInsurance':
case 'annualService':
preview.textContent = euro(value);
break;
case 'durationMonths':
case 'loanDuration':
var years = Math.round(value / 12 * 10) / 10;
preview.textContent = value + ' μήνες (' + years + ' έτη)';
break;
case 'residualYears':
preview.textContent = value + ' έτη';
break;
case 'loanInterest':
case 'taxRate':
preview.textContent = value + '%';
break;
case 'depreciationRate':
case 'deductibility':
preview.textContent = value + '%';
break;
}
}

function updateDepreciationDisplay(val){
document.getElementById('depreciationRateDisplay').textContent=val+'%';
}

function estimateResidualValue(ltvp,years,vehicleType,marketCondition,customRate){
var baseRate={'conventional':0.15,'hev':0.16,'phev':0.18,'bev':0.22}[vehicleType];
var conditionMultiplier={'optimistic':0.85,'normal':1,'pessimistic':1.15}[marketCondition];
var annualDepreciation=customRate?(customRate/100):(baseRate*conditionMultiplier);
var residualValue=ltvp*Math.pow(1-annualDepreciation,years);
var minValue=ltvp*0.05;
var finalResidual=Math.max(residualValue,minValue);
return{value:finalResidual,percentage:(finalResidual/ltvp)*100,annualRate:annualDepreciation*100,years:years};
}

function applyEstimatedResidual(){
var estimated=document.getElementById('estimatedResidual').textContent;
var numericValue=parseFloat(estimated.replace(/[€.]/g,'').replace(',','.'));
if(!isNaN(numericValue)){
document.getElementById('residualValue').value=Math.round(numericValue);
updateInputPreview('residualValue');
calculateAll();
alert('Η υπολειμματική αξία ενημερώθηκε: '+estimated);
}
}

function calculateLoanPayment(principal,annualRate,months){
var monthlyRate=(annualRate/100)/12;
if(monthlyRate===0)return principal/months;
return principal*(monthlyRate*Math.pow(1+monthlyRate,months))/(Math.pow(1+monthlyRate,months)-1);
}

function calculateAll(){
var vehicleType=document.getElementById('vehicleType').value;
var usageType=document.getElementById('usageType').value;
var ltvp=parseFloat(document.getElementById('ltvp').value)||0;
var monthlyPayment=parseFloat(document.getElementById('monthlyPayment').value)||0;
var durationMonths=parseInt(document.getElementById('durationMonths').value)||0;
var downPaymentLeasing=parseFloat(document.getElementById('downPaymentLeasing').value)||0;
var buyoutPrice=parseFloat(document.getElementById('buyoutPrice').value)||0;
var downPaymentLoan=parseFloat(document.getElementById('downPaymentLoan').value)||0;
var loanAmount=parseFloat(document.getElementById('loanAmount').value)||0;
var loanInterest=parseFloat(document.getElementById('loanInterest').value)||0;
var loanDuration=parseInt(document.getElementById('loanDuration').value)||0;
var depreciationRate=parseFloat(document.getElementById('depreciationRate').value)||0;
var residualValue=parseFloat(document.getElementById('residualValue').value)||0;
var taxRate=parseFloat(document.getElementById('taxRate').value)||0;
var deductibility=(parseFloat(document.getElementById('deductibility').value)||0)/100;
var annualInsurance=parseFloat(document.getElementById('annualInsurance').value)||0;
var annualService=parseFloat(document.getElementById('annualService').value)||0;
var residualYears=parseInt(document.getElementById('residualYears').value)||8;
var marketCondition=document.getElementById('marketCondition').value;
var customDepreciation=parseFloat(document.getElementById('customDepreciation').value)||20;
var vatRate=0.24;
var isElectric=vehicleType==='bev';
var years=5;

// RESIDUAL VALUE ESTIMATION
var residualEstimate=estimateResidualValue(ltvp,residualYears,vehicleType,marketCondition,customDepreciation);
document.getElementById('estimatedResidual').textContent=euro(residualEstimate.value);
document.getElementById('residualPercentage').textContent=pct(residualEstimate.percentage);
document.getElementById('avgAnnualDepreciation').textContent=pct(residualEstimate.annualRate);

var vehicleTypeNames={'conventional':'Συμβατικό (15% ετήσια απόσβεση)','hev':'Υβριδικό HEV (16% ετήσια απόσβεση)','phev':'Plug-in Hybrid (18% ετήσια απόσβεση)','bev':'Ηλεκτρικό BEV (22% ετήσια απόσβεση)'};
var marketNames={'optimistic':'Αισιόδοξο (-15% απόσβεση)','normal':'Κανονική (χωρίς αλλαγή)','pessimistic':'Απαισιόδοξο (+15% απόσβεση)'};

document.getElementById('residualCalculationDetails').innerHTML='<strong>Παράμετροι Εκτίμησης:</strong><br>• Τύπος οχήματος: '+vehicleTypeNames[vehicleType]+'<br>• Χρόνια: '+residualYears+'<br>• Κατάσταση αγοράς: '+marketNames[marketCondition]+'<br>• Προσαρμοσμένη ετήσια απόσβεση: '+pct(residualEstimate.annualRate)+'<br><br><strong>Υπολογισμός:</strong> '+euro(ltvp)+' × (1 - '+pct(residualEstimate.annualRate)+')^'+residualYears+' = '+euro(residualEstimate.value)+'<br><em>Ελάχιστο όριο 5%: '+euro(ltvp*0.05)+'</em>';

// Calculate enhancement rates
var enhancement50pct=0,enhancement25pct=0;
if(isElectric&&ltvp>0){
if(ltvp<=40000){enhancement50pct=1;enhancement25pct=0;}else{enhancement50pct=40000/ltvp;enhancement25pct=1-enhancement50pct;}
}

// LEASING CALCULATIONS (CORRECTED)

var monthlyPaymentNet=usageType==='ix'?monthlyPayment:monthlyPayment/(1+vatRate);
var annualPayment=monthlyPayment*12;
var annualPaymentNet=monthlyPaymentNet*12;

var leasingYears=durationMonths/12;

// ✅ Κατανομή προκαταβολής
var annualDownPayment=downPaymentLeasing/leasingYears;

// ✅ Σωστή βάση για προσαύξηση
var annualBaseLeasing=annualPaymentNet+annualDownPayment;

var totalLeasingPayments=monthlyPayment*durationMonths;
var leasingAcquisitionCost=totalLeasingPayments+downPaymentLeasing+buyoutPrice;

// ✅ Προσαύξηση πάνω στη σωστή βάση
var annualEnhancement50=isElectric?annualBaseLeasing*enhancement50pct*0.5:0;
var annualEnhancement25=isElectric?annualBaseLeasing*enhancement25pct*0.25:0;

var annualLeasingDeduction=annualBaseLeasing+annualEnhancement50+annualEnhancement25;
var totalLeasingDeduction=annualLeasingDeduction*leasingYears;
var taxBenefitLeasing=totalLeasingDeduction*taxRate*deductibility;

var netCostLeasing=leasingAcquisitionCost-taxBenefitLeasing;

// LOAN CALCULATIONS
var monthlyLoanPayment=calculateLoanPayment(loanAmount,loanInterest,loanDuration);
var totalLoanPayments=monthlyLoanPayment*loanDuration;
var totalInterestPaid=totalLoanPayments-loanAmount;
var loanAcquisitionCost=downPaymentLoan+totalLoanPayments;
var insuranceTotal=annualInsurance*years;
var serviceTotal=annualService*years;
var extraCostsTotal=insuranceTotal+serviceTotal;
var totalLoanCosts=loanAcquisitionCost+extraCostsTotal;
var depreciableAmount=ltvp-residualValue;
var annualDepreciation=depreciableAmount*(depreciationRate/100);
var totalDepreciation5y=Math.min(annualDepreciation*5,depreciableAmount);
var totalLoanDeduction=totalDepreciation5y+totalInterestPaid;
var taxBenefitLoan=totalLoanDeduction*taxRate;
var netCostLoan=totalLoanCosts-taxBenefitLoan;

// UPDATE UI
document.getElementById('compLeasingTotal').textContent=euro(leasingAcquisitionCost);
document.getElementById('compLoanTotal').textContent=euro(loanAcquisitionCost);
document.getElementById('compLeasingInsurance').textContent=euro(0)+' (συμπεριλ.)';
document.getElementById('compLoanInsurance').textContent=euro(insuranceTotal);
document.getElementById('compLeasingService').textContent=euro(0)+' (συμπεριλ.)';
document.getElementById('compLoanService').textContent=euro(serviceTotal);
document.getElementById('compLeasingAllCosts').textContent=euro(leasingAcquisitionCost);
document.getElementById('compLoanAllCosts').textContent=euro(totalLoanCosts);
document.getElementById('compLeasingDeduction').textContent=euro(totalLeasingDeduction);
document.getElementById('compLoanDeduction').textContent=euro(totalLoanDeduction);
document.getElementById('compLeasingTaxBenefit').textContent=euro(taxBenefitLeasing);
document.getElementById('compLoanTaxBenefit').textContent=euro(taxBenefitLoan);
document.getElementById('compLeasingNet').innerHTML='<b>'+euro(netCostLeasing)+'</b>';
document.getElementById('compLoanNet').innerHTML='<b>'+euro(netCostLoan)+'</b>';
document.getElementById('compLeasingAnnual').textContent=euro(netCostLeasing/5);
document.getElementById('compLoanAnnual').textContent=euro(netCostLoan/5);

// Winner - ΣΩΣΤΗ ΛΟΓΙΚΗ
var diff=netCostLeasing-netCostLoan;
var winnerDiv=document.getElementById('winnerResult');
if(diff>1000){
winnerDiv.className='result-box result-success';
winnerDiv.innerHTML='<h3>🟢 Η Αγορά με Δάνειο συμφέρει!</h3><p>Κερδίζετε: <b>'+euro(diff)+'</b> σε 5 χρόνια<br>('+euro(diff/5)+'/έτος)<br><small>Το Leasing είναι ακριβότερο κατά '+euro(diff)+'</small></p>';
}
else if(diff<-1000){
winnerDiv.className='result-box result-error';
winnerDiv.innerHTML='<h3>🔴 Το Leasing συμφέρει!</h3><p>Κερδίζετε: <b>'+euro(Math.abs(diff))+'</b> σε 5 χρόνια<br>('+euro(Math.abs(diff)/5)+'/έτος)<br><small>Η Αγορά είναι ακριβότερη κατά '+euro(Math.abs(diff))+'</small></p>';
}
else{
winnerDiv.className='result-box result-warning';
winnerDiv.innerHTML='<h3>🟡 Οριακή διαφορά</h3><p>Διαφορά: <b>'+euro(Math.abs(diff))+'</b><br>Επιλέξτε με βάση άλλα κριτήρια (ευελιξία, κτλ.)</p>';
}

// Summary Results
document.getElementById('leasingPayments').textContent=euro(totalLeasingPayments);
document.getElementById('leasingTotalCost').textContent=euro(leasingAcquisitionCost);
document.getElementById('leasingTaxBenefit').textContent=euro(taxBenefitLeasing);
document.getElementById('leasingNetCost').textContent=euro(netCostLeasing);

document.getElementById('loanMonthly').textContent=euro(monthlyLoanPayment);
document.getElementById('loanInterestTotal').textContent=euro(totalInterestPaid);
document.getElementById('loanExtraCosts').textContent=euro(extraCostsTotal);
document.getElementById('loanTaxBenefit2').textContent=euro(taxBenefitLoan);

// Enhancement details
var enhSummaryDiv=document.getElementById('enhancementDetails');
if(isElectric){
enhSummaryDiv.style.display='block';
document.getElementById('enh50pct').textContent=pct(enhancement50pct*100);
document.getElementById('enh25pct').textContent=pct(enhancement25pct*100);
document.getElementById('enh50amount').textContent=euro(annualEnhancement50);
document.getElementById('enh25amount').textContent=euro(annualEnhancement25);
document.getElementById('enhancementCalc').innerHTML='<strong>Υπολογισμός Προσαύξησης:</strong><br>- ΛΤΠΦ: '+euro(ltvp)+'<br>- Έως €40.000 ('+pct(enhancement50pct*100)+'): '+euro(annualPaymentNet*enhancement50pct)+' × 50% = <strong>'+euro(annualEnhancement50)+'/έτος</strong><br>- Υπερβάλλον ('+pct(enhancement25pct*100)+'): '+euro(annualPaymentNet*enhancement25pct)+' × 25% = <strong>'+euro(annualEnhancement25)+'/έτος</strong><br>- Βασική έκπτωση: '+euro(annualPaymentNet)+'/έτος<br>- <strong>Σύνολο ετήσιας έκπτωσης: '+euro(annualLeasingDeduction)+'/έτος</strong><br>- <strong>Σύνολο περιόδου: '+euro(totalLeasingDeduction)+'</strong>';
}else{enhSummaryDiv.style.display='none';}

// Loan details
var yearsOfDepreciation=annualDepreciation>0?Math.ceil((ltvp-residualValue)/annualDepreciation):0;
document.getElementById('loanDetails').innerHTML='<strong>Κόστος απόκτησης:</strong> '+euro(loanAcquisitionCost)+'<br><strong>Έξοδα ασφάλειας:</strong> '+euro(insuranceTotal)+'<br><strong>Έξοδα service:</strong> '+euro(serviceTotal)+'<br><strong>Σύνολο εξόδων:</strong> '+euro(totalLoanCosts)+'<br><strong>Απόσβεση:</strong> '+euro(annualDepreciation)+'/έτος<br><strong>Σύνολο εκπιπτέων:</strong> '+euro(totalLoanDeduction);

// DETAILED CALCULATIONS
var monthlyRate=(loanInterest/100)/12;

document.getElementById('calcLeasingStep1').innerHTML=euro(monthlyPayment)+' × 12 = <strong>'+euro(annualPayment)+'</strong>';
document.getElementById('calcLeasingVatDetail').textContent=usageType==='ix'?'ΙΧ: Εκπίπτει όλο το ποσό με ΦΠΑ (€'+formatNumber(monthlyPayment)+')':'Εταιρικό: Εκπίπτει η καθαρή αξία €'+formatNumber(monthlyPaymentNet)+' (ο ΦΠΑ συμψηφίζεται)';

var enhDiv=document.getElementById('calcEnhancementStep');
if(isElectric){
enhDiv.style.display='block';
var portion50=annualPaymentNet*enhancement50pct;
var portion25=annualPaymentNet*enhancement25pct;
document.getElementById('calcEnhancementDetail').innerHTML='ΛΤΠΦ = '+euro(ltvp)+' (> €40.000, οπότε χωρίζεται σε δύο κλιμάκια)<br><br><strong>Κλιμάκιο 50%:</strong><br>Ποσοστό: '+pct(enhancement50pct*100)+' του μισθώματος<br>Ποσό: '+euro(annualPaymentNet)+' × '+pct(enhancement50pct*100)+' = '+euro(portion50)+'<br>Προσαύξηση: '+euro(portion50)+' × 50% = <strong>'+euro(annualEnhancement50)+'</strong><br><br><strong>Κλιμάκιο 25%:</strong><br>Ποσοστό: '+pct(enhancement25pct*100)+' του μισθώματος<br>Ποσό: '+euro(annualPaymentNet)+' × '+pct(enhancement25pct*100)+' = '+euro(portion25)+'<br>Προσαύξηση: '+euro(portion25)+' × 25% = <strong>'+euro(annualEnhancement25)+'</strong>';
}else{enhDiv.style.display='none';}

document.getElementById('calcLeasingDeduction').innerHTML=isElectric?'Βασική έκπτωση: '+euro(annualPaymentNet)+'<br>+ Προσαύξηση 50%: '+euro(annualEnhancement50)+'<br>+ Προσαύξηση 25%: '+euro(annualEnhancement25):'Βασική έκπτωση: '+euro(annualPaymentNet)+' (χωρίς προσαύξηση - όχι BEV)';
document.getElementById('calcLeasingDeductionResult').textContent='Σύνολο: '+euro(annualLeasingDeduction)+'/έτος';
document.getElementById('calcLeasingPeriod').innerHTML=euro(annualLeasingDeduction)+' × '+(durationMonths/12)+' έτη = <strong>'+euro(totalLeasingDeduction)+'</strong>';
document.getElementById('calcLeasingTaxBenefitDetail').innerHTML=euro(totalLeasingDeduction)+' × '+pct(taxRate*100)+' × '+pct(deductibility*100)+' = <strong>'+euro(taxBenefitLeasing)+'</strong>';
document.getElementById('calcLeasingTaxBenefitResult').textContent='Φορολογικό όφελος: '+euro(taxBenefitLeasing);
document.getElementById('calcLeasingAcquisition').innerHTML=euro(totalLeasingPayments)+' + '+euro(downPaymentLeasing)+' + '+euro(buyoutPrice)+' = <strong>'+euro(leasingAcquisitionCost)+'</strong>';
document.getElementById('calcLeasingNetDetail').innerHTML=euro(leasingAcquisitionCost)+' - '+euro(taxBenefitLeasing)+' = <strong>'+euro(netCostLeasing)+'</strong>';
document.getElementById('calcLeasingNetResult').textContent='Καθαρό κόστος Leasing: '+euro(netCostLeasing);

document.getElementById('calcLoanStep1').innerHTML='P='+euro(loanAmount)+', r='+(monthlyRate*100).toFixed(4)+'%, n='+loanDuration+'<br>Μηνιαία δόση = <strong>'+euro(monthlyLoanPayment)+'</strong>';
document.getElementById('calcLoanInterest').innerHTML='('+euro(monthlyLoanPayment)+' × '+loanDuration+') - '+euro(loanAmount)+' = <strong>'+euro(totalInterestPaid)+'</strong>';
document.getElementById('calcLoanInterestResult').textContent='Συνολικοί τόκοι: '+euro(totalInterestPaid);
document.getElementById('calcLoanTotalPaid').innerHTML=euro(monthlyLoanPayment)+' × '+loanDuration+' = <strong>'+euro(totalLoanPayments)+'</strong>';
document.getElementById('calcLoanAcquisition').innerHTML=euro(downPaymentLoan)+' + '+euro(totalLoanPayments)+' = <strong>'+euro(loanAcquisitionCost)+'</strong>';
document.getElementById('calcInsuranceDetail').innerHTML=euro(annualInsurance)+'/έτος × '+years+' έτη = <strong>'+euro(insuranceTotal)+'</strong>';
document.getElementById('calcServiceDetail').innerHTML=euro(annualService)+'/έτος × '+years+' έτη = <strong>'+euro(serviceTotal)+'</strong>';
document.getElementById('calcTotalExpenses').innerHTML=euro(loanAcquisitionCost)+' + '+euro(insuranceTotal)+' + '+euro(serviceTotal)+' = <strong>'+euro(totalLoanCosts)+'</strong>';
document.getElementById('calcTotalExpensesResult').textContent='Σύνολο εξόδων αγοράς: '+euro(totalLoanCosts);
document.getElementById('calcDepreciation').innerHTML='('+euro(ltvp)+' - '+euro(residualValue)+') × '+pct(depreciationRate)+' = <strong>'+euro(annualDepreciation)+'</strong>/έτος';
var actualDepreciationYears=Math.min(5,yearsOfDepreciation);
document.getElementById('calcDepreciation5y').innerHTML=euro(annualDepreciation)+'/έτος × '+actualDepreciationYears+' έτη = <strong>'+euro(totalDepreciation5y)+'</strong>';
document.getElementById('calcLoanDeduction').innerHTML=euro(totalDepreciation5y)+' + '+euro(totalInterestPaid)+' = <strong>'+euro(totalLoanDeduction)+'</strong>';
document.getElementById('calcLoanDeductionResult').textContent='Σύνολο εκπιπτέων: '+euro(totalLoanDeduction);
document.getElementById('calcLoanTaxBenefitDetail').innerHTML=euro(totalLoanDeduction)+' × '+pct(taxRate*100)+' = <strong>'+euro(taxBenefitLoan)+'</strong>';
document.getElementById('calcLoanTaxBenefitResult').textContent='Φορολογικό όφελος: '+euro(taxBenefitLoan);
document.getElementById('calcLoanNetDetail').innerHTML=euro(totalLoanCosts)+' - '+euro(taxBenefitLoan)+' = <strong>'+euro(netCostLoan)+'</strong>';
document.getElementById('calcLoanNetResult').textContent='Καθαρό κόστος Αγοράς: '+euro(netCostLoan);

document.getElementById('calcFinalComparison').innerHTML=euro(netCostLeasing)+' - '+euro(netCostLoan)+' = <strong>'+euro(diff)+'</strong>';
var finalText;
if(diff>1000){
finalText='✅ Η Αγορά με Δάνειο συμφέρει! Το Leasing είναι ακριβότερο κατά '+euro(diff);
}else if(diff<-1000){
finalText='✅ Το Leasing συμφέρει! Η Αγορά είναι ακριβότερη κατά '+euro(Math.abs(diff));
}else{
finalText='⚖️ Οριακή διαφορά: '+euro(Math.abs(diff));
}
document.getElementById('calcFinalResult').textContent=finalText;

generateEmail();
}

function generateEmail(){
var companyName=document.getElementById('companyName').value;
var clientName=document.getElementById('clientName').value;
var leasingNet=document.getElementById('leasingNetCost').textContent;
var loanNet=document.getElementById('compLoanNet').textContent;
var winnerText=document.querySelector('#winnerResult h3').textContent;
document.getElementById('emailText').value='Θέμα: Σύγκριση Leasing vs Αγοράς με Δάνειο\\n\\nΑξιότιμοι κύριοι/κυρίες της '+companyName+',\\n\\nΣας αποστέλλω σύγκριση κόστους αυτοκινήτου:\\n\\nLeasing: '+leasingNet+'\\nΑγορά με Δάνειο: '+loanNet+'\\n\\nΑποτέλεσμα: '+winnerText+'\\n\\nΠαρακαλώ για την προσφορά σας.\\n\\nΜε εκτίμηση,\\n'+clientName;
}

function copyEmail(){
var emailText=document.getElementById('emailText');
emailText.select();
document.execCommand('copy');
alert('Το email αντιγράφηκε!');
}

function downloadReport(){
var today=new Date().toLocaleDateString('el-GR');
var leasingNet=document.getElementById('leasingNetCost').textContent;
var loanNet=document.getElementById('compLoanNet').textContent;
var winnerText=document.querySelector('#winnerResult h3').textContent;
var report='Leasing vs Αγορά με Δάνειο - Report\\n===============================\\nΗμερομηνία: '+today+'\\n\\nLeasing: '+leasingNet+'\\nΑγορά με Δάνειο: '+loanNet+'\\n\\nΑποτέλεσμα: '+winnerText;
var blob=new Blob([report],{type:'text/plain'});
var url=URL.createObjectURL(blob);
var a=document.createElement('a');
a.href=url;
a.download='leasing_vs_loan_report.txt';
a.click();
URL.revokeObjectURL(url);
}

// Initialize
window.onload=function(){
var inputs=['ltvp','monthlyPayment','durationMonths','downPaymentLeasing','buyoutPrice','downPaymentLoan','loanAmount','loanInterest','loanDuration','depreciationRate','residualValue','taxRate','deductibility','residualYears','annualInsurance','annualService'];
for(var i=0;i<inputs.length;i++){
updateInputPreview(inputs[i]);
}
calculateAll();
};
</script>
</body>
</html>
"""

components.html(HTML_CODE, height=3000, scrolling=True)