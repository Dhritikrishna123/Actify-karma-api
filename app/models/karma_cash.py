# Pydantic model for KarmaCash transactions

from typing import Optional, Dict
from datetime import datetime, UTC, timedelta
from pydantic import BaseModel, Field

from .base import BaseDBModel
from .user import UserReference

class KarmaCashTransaction(BaseDBModel):
    """Model for tracking karma cash transactions"""
    # Transaction Information
    user: UserReference = Field(
        ...,
        description="User involved in the transaction"
    )
    transaction_type: str = Field(
        ...,
        description="Type of transaction (e.g., 'recharge', 'conversion', 'purchase', 'refund')"
    )
    amount: float = Field(
        ...,
        description="Amount of karma cash involved"
    )
    
    # Context
    context_id: Optional[str] = Field(
        default=None,
        description="ID of the related entity (e.g., purchase_id, recharge_id)"
    )
    context_type: Optional[str] = Field(
        default=None,
        description="Type of the related entity"
    )
    description: Optional[str] = Field(
        default=None,
        description="Description of the transaction"
    )
    
    # Payment Details (if recharge)
    payment_method: Optional[str] = Field(
        default=None,
        description="Payment method used (e.g., 'credit_card', 'upi', 'net_banking')"
    )
    payment_id: Optional[str] = Field(
        default=None,
        description="Payment gateway transaction ID"
    )
    payment_amount: Optional[float] = Field(
        default=None,
        description="Amount paid in real currency"
    )
    currency: Optional[str] = Field(
        default=None,
        description="Currency used for payment"
    )
    
    # Conversion Details (if conversion)
    karma_points_used: Optional[float] = Field(
        default=None,
        description="Amount of karma points converted"
    )
    conversion_rate: Optional[float] = Field(
        default=None,
        description="Exchange rate used for conversion"
    )
    
    # Status
    status: str = Field(
        default="completed",
        description="Status of the transaction"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the transaction was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the transaction was last updated"
    )

    @classmethod
    def example(cls) -> 'KarmaCashTransaction':
        """Create an example KarmaCashTransaction instance"""
        now = datetime.now(UTC)
        return cls(
            user=UserReference(
                user_id="user_123",
                username="example_user",
                display_name="Example User"
            ),
            transaction_type="recharge",
            amount=1000.0,
            context_id="recharge_456",
            context_type="recharge",
            description="Initial recharge of 1000 Karma Cash",
            payment_method="upi",
            payment_id="upi_txn_789",
            payment_amount=100.0,
            currency="INR",
            status="completed",
            created_at=now - timedelta(days=1),
            updated_at=now
        )

class KarmaCashBalance(BaseDBModel):
    """Model for tracking user karma cash balance"""
    # User Information
    user: UserReference = Field(
        ...,
        description="User this balance belongs to"
    )
    
    # Balance Information
    current_balance: float = Field(
        default=0.0,
        description="Current karma cash balance"
    )
    total_recharged: float = Field(
        default=0.0,
        description="Total karma cash obtained through recharge"
    )
    total_converted: float = Field(
        default=0.0,
        description="Total karma cash obtained through conversion"
    )
    total_spent: float = Field(
        default=0.0,
        description="Total karma cash spent"
    )
    
    # Conversion Limits
    daily_conversion_limit: float = Field(
        default=100.0,
        description="Maximum karma cash that can be converted per day"
    )
    weekly_conversion_limit: float = Field(
        default=500.0,
        description="Maximum karma cash that can be converted per week"
    )
    
    # Statistics
    recharge_count: int = Field(
        default=0,
        description="Number of recharges made"
    )
    conversion_count: int = Field(
        default=0,
        description="Number of conversions made"
    )
    last_recharge_at: Optional[datetime] = Field(
        default=None,
        description="When the last recharge was made"
    )
    last_conversion_at: Optional[datetime] = Field(
        default=None,
        description="When the last conversion was made"
    )
    
    # Timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the balance was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="When the balance was last updated"
    )

    @classmethod
    def example(cls) -> 'KarmaCashBalance':
        """Create an example KarmaCashBalance instance"""
        now = datetime.now(UTC)
        return cls(
            user=UserReference(
                user_id="user_123",
                username="example_user",
                display_name="Example User"
            ),
            current_balance=850.0,
            total_recharged=1000.0,
            total_converted=50.0,
            total_spent=200.0,
            daily_conversion_limit=100.0,
            weekly_conversion_limit=500.0,
            recharge_count=1,
            conversion_count=1,
            last_recharge_at=now - timedelta(days=1),
            last_conversion_at=now - timedelta(hours=12),
            created_at=now - timedelta(days=1),
            updated_at=now
        )

class KarmaCashRecharge(BaseModel):
    """Model for recharging karma cash with real money"""
    amount: float = Field(
        ...,
        description="Amount of karma cash to recharge"
    )
    payment_method: str = Field(
        ...,
        description="Payment method to use"
    )
    currency: str = Field(
        default="INR",
        description="Currency to use for payment"
    )

    @classmethod
    def example(cls) -> 'KarmaCashRecharge':
        """Create an example KarmaCashRecharge instance"""
        return cls(
            amount=1000.0,
            payment_method="upi",
            currency="INR"
        )

class KarmaCashConversion(BaseModel):
    """Model for converting karma points to karma cash"""
    karma_points: float = Field(
        ...,
        description="Amount of karma points to convert"
    )
    conversion_rate: float = Field(
        default=100.0,
        description="Exchange rate (karma points per karma cash)"
    )

    @classmethod
    def example(cls) -> 'KarmaCashConversion':
        """Create an example KarmaCashConversion instance"""
        return cls(
            karma_points=5000.0,
            conversion_rate=100.0  # 5000 points = 50 Karma Cash
        )

class KarmaCashPurchase(BaseModel):
    """Model for purchasing items with karma cash"""
    item_id: str = Field(
        ...,
        description="ID of the item being purchased"
    )
    item_type: str = Field(
        ...,
        description="Type of the item (e.g., 'badge', 'feature', 'service')"
    )
    amount: float = Field(
        ...,
        description="Amount of karma cash required"
    )

    @classmethod
    def example(cls) -> 'KarmaCashPurchase':
        """Create an example KarmaCashPurchase instance"""
        return cls(
            item_id="premium_badge_001",
            item_type="badge",
            amount=200.0
        )

class KarmaCashTransactionCreate(BaseModel):
    """Model for creating new karma cash transactions"""
    user_id: str = Field(..., description="ID of the user involved in the transaction")
    transaction_type: str = Field(..., description="Type of transaction (e.g., 'recharge', 'conversion', 'purchase', 'refund')")
    amount: float = Field(..., description="Amount of karma cash involved")
    context_id: Optional[str] = Field(default=None, description="ID of the related entity")
    context_type: Optional[str] = Field(default=None, description="Type of the related entity")
    description: Optional[str] = Field(default=None, description="Description of the transaction")
    payment_method: Optional[str] = Field(default=None, description="Payment method used")
    payment_id: Optional[str] = Field(default=None, description="Payment gateway transaction ID")
    payment_amount: Optional[float] = Field(default=None, description="Amount paid in real currency")
    currency: Optional[str] = Field(default=None, description="Currency used for payment")
    karma_points_used: Optional[float] = Field(default=None, description="Amount of karma points converted")
    conversion_rate: Optional[float] = Field(default=None, description="Exchange rate used for conversion")
    status: str = Field(default="pending", description="Status of the transaction")
