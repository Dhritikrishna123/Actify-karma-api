"""Civic karma configuration."""

from .base_config import QUALITY_MULTIPLIERS, TIME_MULTIPLIERS

# Karma points for civic actions
CIVIC_POINTS = {
    "REPORT_CREATION": 10,
    "REPORT_VERIFICATION": 20,
    "REPORT_RESOLUTION": 50,
    "ENDORSEMENT": 5
}

# Rate limits for civic actions
CIVIC_RATE_LIMITS = {
    "REPORTS_PER_DAY": 10,
    "ENDORSEMENTS_PER_DAY": 20,
    "VERIFICATIONS_PER_DAY": 15
}

# Report categories and their impact levels
REPORT_CATEGORIES = {
    "INFRASTRUCTURE": {
        "POTHOLE": {"points": 10, "impact": "STANDARD"},
        "BROKEN_ROAD": {"points": 15, "impact": "HIGH_IMPACT"},
        "TRAFFIC_SIGNAL": {"points": 20, "impact": "HIGH_IMPACT"},
        "DAMAGED_SIGNAGE": {"points": 8, "impact": "MINOR"},
        "BRIDGE_DAMAGE": {"points": 25, "impact": "HIGH_IMPACT"}
    },
    "ENVIRONMENTAL": {
        "GARBAGE": {"points": 8, "impact": "STANDARD"},
        "BURNING": {"points": 15, "impact": "HIGH_IMPACT"},
        "VEGETATION": {"points": 5, "impact": "MINOR"},
        "POLLUTION": {"points": 20, "impact": "HIGH_IMPACT"},
        "WATER": {"points": 12, "impact": "STANDARD"}
    }
}

# Quality thresholds for civic actions
CIVIC_QUALITY_THRESHOLDS = {
    "REPORT": {
        "MIN_DESCRIPTION_LENGTH": 50,
        "MIN_MEDIA_COUNT": 1,
        "MAX_MEDIA_COUNT": 5
    },
    "VERIFICATION": {
        "MIN_CONFIRMATION_COUNT": 2,
        "MAX_CONFIRMATION_COUNT": 5
    },
    "RESOLUTION": {
        "MIN_DESCRIPTION_LENGTH": 100,
        "REQUIRED_MEDIA": True
    }
} 