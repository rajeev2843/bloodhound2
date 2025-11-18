from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime, Enum, Text, Float, JSON
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
import enum
import os

# Enums
class UserRole(enum.Enum):
    CLIENT = "client"
    CA = "ca"
    ADMIN = "admin"

class EntityType(enum.Enum):
    PROPRIETORSHIP = "Proprietorship"
    PARTNERSHIP = "Partnership"
    LLP = "LLP"
    PRIVATE_LIMITED = "Private Limited"
    PUBLIC_LIMITED = "Public Limited"

class RiskLevel(enum.Enum):
    LOW = "Low Risk"
    MEDIUM = "Medium Risk"
    HIGH = "High Risk"
    CRITICAL = "Critical"

Base = declarative_base()

# 1. User Table
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)
    google_oauth_id = Column(String, unique=True, nullable=True)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CLIENT, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    ca_profile = relationship("CAProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    entity_profile = relationship("EntityProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

# 2. CA Profile
class CAProfile(Base):
    __tablename__ = 'ca_profiles'

    ca_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True, nullable=False)
    firm_name = Column(String, nullable=False)
    membership_no = Column(String, unique=True, nullable=False)
    contact_number = Column(String)
    invite_code = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="ca_profile")
    clients = relationship("EntityProfile", back_populates="linked_ca")
    billing_logs = relationship("BillingLog", back_populates="ca")

# 3. Entity Profile
class EntityProfile(Base):
    __tablename__ = 'entity_profiles'

    entity_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True, nullable=False)
    ca_id = Column(Integer, ForeignKey('ca_profiles.ca_id'), nullable=True)

    entity_name = Column(String, nullable=False)
    entity_type = Column(Enum(EntityType), nullable=False)
    gstin = Column(String(15), unique=True, nullable=False, index=True)
    pan = Column(String(10), nullable=False, index=True)
    registration_no = Column(String, nullable=True)
    tan_number = Column(String, nullable=True)
    registered_address = Column(Text)
    industry_sector = Column(String)
    is_setup_complete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="entity_profile")
    linked_ca = relationship("CAProfile", back_populates="clients")
    vendors = relationship("Vendor", back_populates="entity", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="entity", cascade="all, delete-orphan")

# 4. Vendor Table
class Vendor(Base):
    __tablename__ = 'vendors'

    vendor_id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey('entity_profiles.entity_id'), nullable=False)
    
    name = Column(String, nullable=False)
    gstin = Column(String(15), nullable=False, index=True)
    pan = Column(String(10), nullable=True)
    
    registration_days = Column(Integer, default=0)
    address_type = Column(String, default="Unknown")
    director_companies = Column(Integer, default=0)
    
    gstr1_status = Column(String, default="Unknown")
    gstr3b_status = Column(String, default="Unknown")
    months_not_filed = Column(Integer, default=0)
    
    transaction_count = Column(Integer, default=0)
    itc_amount = Column(Float, default=0.0)
    cash_payments = Column(Float, default=0.0)
    
    risk_score = Column(Integer, default=0)
    risk_level = Column(Enum(RiskLevel), default=RiskLevel.LOW)
    risk_factors = Column(JSON, default=list)
    
    last_analyzed_at = Column(DateTime, default=datetime.utcnow)
    gstn_api_data = Column(JSON, default=dict)
    mca_api_data = Column(JSON, default=dict)
    
    is_watchlisted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    entity = relationship("EntityProfile", back_populates="vendors")
    transactions = relationship("Transaction", back_populates="vendor", cascade="all, delete-orphan")

# 5. Transaction Table
class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey('entity_profiles.entity_id'), nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendors.vendor_id'), nullable=False)
    
    transaction_date = Column(DateTime, nullable=False)
    invoice_number = Column(String)
    transaction_amount = Column(Float, nullable=False)
    tax_amount = Column(Float, default=0.0)
    payment_mode = Column(String, default="Bank Transfer")
    
    created_at = Column(DateTime, default=datetime.utcnow)

    entity = relationship("EntityProfile", back_populates="transactions")
    vendor = relationship("Vendor", back_populates="transactions")

# 6. Billing Log (For CA billing tracking)
class BillingLog(Base):
    __tablename__ = 'billing_logs'

    log_id = Column(Integer, primary_key=True, index=True)
    ca_id = Column(Integer, ForeignKey('ca_profiles.ca_id'), nullable=False)
    entity_id = Column(Integer, ForeignKey('entity_profiles.entity_id'), nullable=False)
    
    activity_type = Column(String, nullable=False)  # "login", "report", "analysis"
    hours_logged = Column(Float, default=0.0)
    description = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    ca = relationship("CAProfile", back_populates="billing_logs")

# 7. System Audit Log (For compliance trail)
class AuditLog(Base):
    __tablename__ = 'audit_logs'

    log_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    action = Column(String, nullable=False)
    details = Column(JSON, default=dict)
    ip_address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database Setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bloodhound_prod.db")

def get_engine():
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
        echo=False
    )
    return engine

def init_database():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    return engine

def get_session():
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
