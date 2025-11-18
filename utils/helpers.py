from database import get_session, Vendor, RiskLevel
from datetime import datetime, timedelta
import json

def calculate_vendor_risk_score(vendor_data: dict) -> tuple:
    """Calculate risk score and return (score, risk_factors, risk_level)"""
    score = 0
    risk_factors = []
    
    # Registration age check
    reg_days = vendor_data.get('registration_days', 365)
    if reg_days < 30:
        score += 35
        risk_factors.append(f"⚠️ Recently registered ({reg_days} days) - High fraud risk")
    elif reg_days < 90:
        score += 25
        risk_factors.append(f"⚠️ New vendor ({reg_days} days) - Enhanced due diligence required")
    elif reg_days < 180:
        score += 10
        risk_factors.append(f"ℹ️ Relatively new vendor ({reg_days} days)")
    
    # Address type check
    address_type = vendor_data.get('address_type', '')
    if address_type in ['Rented Room', 'Virtual Office']:
        score += 25
        risk_factors.append(f"🏢 Operating from {address_type} - Shell company indicator")
    elif address_type == 'Residential':
        score += 15
        risk_factors.append("🏠 Operating from residential address - Verify legitimacy")
    
    # Director proliferation check
    dir_companies = vendor_data.get('director_companies', 0)
    if dir_companies > 30:
        score += 20
        risk_factors.append(f"👥 Director in {dir_companies} companies - Shell network risk")
    elif dir_companies > 15:
        score += 10
        risk_factors.append(f"👥 Director in {dir_companies} companies - Monitor activity")
    
    # GST filing check
    gstr1_status = vendor_data.get('gstr1_status', 'Unknown')
    if gstr1_status == 'Nil Return':
        score += 15
        risk_factors.append("📋 NIL GSTR-1 returns - No sales despite ITC claims")
    elif gstr1_status == 'Not Filed':
        score += 20
        risk_factors.append("❌ GSTR-1 not filed - Non-compliant vendor")
    
    months_not_filed = vendor_data.get('months_not_filed', 0)
    if months_not_filed > 3:
        score += 30
        risk_factors.append(f"🚨 GSTR-3B not filed for {months_not_filed} months - Cancellation imminent")
    elif months_not_filed > 0:
        score += 15 + (months_not_filed * 3)
        risk_factors.append(f"⚠️ GSTR-3B delayed by {months_not_filed} months - ITC reversal risk")
    
    # Cash payment check
    cash_payments = vendor_data.get('cash_payments', 0)
    if cash_payments > 50000:
        score += 15
        risk_factors.append(f"💵 Cash payments ₹{cash_payments:,.0f} exceed Section 40A(3) limit")
    
    # Transaction pattern check
    trans_count = vendor_data.get('transaction_count', 0)
    itc_amount = vendor_data.get('itc_amount', 0)
    if trans_count < 10 and itc_amount > 500000:
        score += 15
        risk_factors.append(f"📊 High ITC (₹{itc_amount:,.0f}) with low transactions ({trans_count}) - Unusual pattern")
    
    # Cap score at 100
    score = min(score, 100)
    
    # Determine risk level
    if score >= 90:
        risk_level = RiskLevel.CRITICAL
    elif score >= 70:
        risk_level = RiskLevel.HIGH
    elif score >= 40:
        risk_level = RiskLevel.MEDIUM
    else:
        risk_level = RiskLevel.LOW
    
    return score, risk_factors, risk_level

def get_recommended_actions(vendor) -> list:
    """Generate action items based on risk"""
    actions = []
    
    if vendor.risk_score >= 90:
        actions.append("🛑 BLOCK ALL PAYMENTS - Do not process any transactions")
        actions.append("🔍 PHYSICAL VERIFICATION - Visit business premises immediately")
    
    if vendor.registration_days < 30:
        actions.append("📋 ENHANCED DUE DILIGENCE - Verify all documents before payment")
    
    if vendor.months_not_filed > 2:
        actions.append(f"⚠️ ITC REVERSAL RISK - ₹{vendor.itc_amount:,.0f} may need reversal")
        actions.append("📞 CONTACT VENDOR - Urgent GST compliance required")
    
    if vendor.director_companies > 20:
        actions.append("🔎 INVESTIGATE - Check for shell company patterns")
    
    if vendor.cash_payments > 50000:
        actions.append("💳 PAYMENT METHOD CHANGE - Use bank transfer only")
    
    if not actions:
        actions.append("✅ Continue monitoring vendor compliance")
    
    return actions

def format_currency(amount: float) -> str:
    """Format currency in Indian style"""
    if amount >= 10000000:  # 1 Crore
        return f"₹{amount/10000000:.2f} Cr"
    elif amount >= 100000:  # 1 Lakh
        return f"₹{amount/100000:.2f} L"
    elif amount >= 1000:  # 1 Thousand
        return f"₹{amount/1000:.2f} K"
    else:
        return f"₹{amount:.2f}"

def check_compliance_breaches(vendor) -> list:
    """Check for specific compliance violations"""
    breaches = []
    
    if vendor.cash_payments > 10000:
        breaches.append(f"⚖️ Section 40A(3) Breach: Cash payments ₹{vendor.cash_payments:,.0f}")
    
    if vendor.months_not_filed > 2:
        breaches.append(f"📋 GST Compliance: {vendor.months_not_filed} months non-filing")
    
    if vendor.gstr1_status == 'Not Filed' and vendor.itc_amount > 100000:
        breaches.append(f"❌ High ITC (₹{vendor.itc_amount:,.0f}) from non-compliant vendor")
    
    return breaches
