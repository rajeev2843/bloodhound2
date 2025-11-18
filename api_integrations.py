import httpx
import json
from datetime import datetime, timedelta
import random

# Mock API calls for demo (replace with real APIs in production)

def extract_pan_from_gstin(gstin: str) -> str:
    """Extract PAN from GSTIN (positions 2-11)"""
    if len(gstin) >= 15:
        return gstin[2:12].upper()
    return ""

# GSTN API
async def fetch_gstn_data(gstin: str) -> dict:
    """
    Real API: https://api.gstin.in/search/{gstin}
    Requires API key from GSTN portal
    """
    # Mock data for demo
    await asyncio.sleep(0.5)  # Simulate API delay
    
    registration_date = datetime.now() - timedelta(days=random.randint(10, 1500))
    
    return {
        "gstin": gstin,
        "legal_name": f"Company {gstin[:5]}",
        "trade_name": f"Trading As {gstin[:5]}",
        "registration_date": registration_date.strftime("%Y-%m-%d"),
        "status": random.choice(["Active", "Active", "Suspended", "Cancelled"]),
        "taxpayer_type": "Regular",
        "gstr1_last_filed": random.choice(["2024-10", "2024-09", "Not Filed"]),
        "gstr3b_last_filed": random.choice(["2024-10", "2024-09", "Not Filed"]),
        "center_jurisdiction": "Mumbai Central",
        "state_jurisdiction": "Maharashtra",
        "api_timestamp": datetime.now().isoformat()
    }

# MCA API
async def fetch_mca_data(pan: str) -> dict:
    """
    Real API: https://mca.gov.in/api/v1/company/{pan}
    Requires MCA portal registration
    """
    await asyncio.sleep(0.5)
    
    company_count = random.randint(1, 50)
    
    return {
        "pan": pan,
        "director_name": f"Director {random.randint(1, 100)}",
        "total_companies": company_count,
        "active_companies": random.randint(1, company_count),
        "dissolved_companies": random.randint(0, company_count // 3),
        "recent_incorporations": random.randint(0, 5),
        "flagged_entities": random.randint(0, 3),
        "compliance_status": random.choice(["Compliant", "Minor Defaults", "Major Defaults"]),
        "api_timestamp": datetime.now().isoformat()
    }

# IBBI/NCLT API (Insolvency check)
async def fetch_ibbi_data(pan: str) -> dict:
    """Check if entity is under insolvency proceedings"""
    await asyncio.sleep(0.3)
    
    return {
        "pan": pan,
        "insolvency_status": random.choice(["Clear", "Clear", "Clear", "Under Process"]),
        "nclt_cases": random.randint(0, 2),
        "ibbi_registered": False,
        "api_timestamp": datetime.now().isoformat()
    }

# Udyam Portal (MSME verification)
async def fetch_udyam_data(gstin: str) -> dict:
    """Verify MSME status"""
    await asyncio.sleep(0.3)
    
    return {
        "gstin": gstin,
        "udyam_registered": random.choice([True, False]),
        "msme_category": random.choice(["Micro", "Small", "Medium", None]),
        "registration_date": datetime.now().strftime("%Y-%m-%d"),
        "api_timestamp": datetime.now().isoformat()
    }

# Comprehensive API orchestrator
async def run_all_checks(gstin: str) -> dict:
    """Run all API checks in parallel"""
    pan = extract_pan_from_gstin(gstin)
    
    # In production, use asyncio.gather for parallel execution
    gstn_data = await fetch_gstn_data(gstin)
    mca_data = await fetch_mca_data(pan)
    ibbi_data = await fetch_ibbi_data(pan)
    udyam_data = await fetch_udyam_data(gstin)
    
    return {
        "gstin_data": gstn_data,
        "mca_data": mca_data,
        "ibbi_data": ibbi_data,
        "udyam_data": udyam_data,
        "pan_extracted": pan,
        "check_timestamp": datetime.now().isoformat()
    }

# Synchronous wrapper for Streamlit
import asyncio

def check_vendor_apis(gstin: str) -> dict:
    """Synchronous wrapper for Streamlit"""
    return asyncio.run(run_all_checks(gstin))
