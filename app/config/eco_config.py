"""Eco karma configuration."""

from .base_config import QUALITY_MULTIPLIERS, SIZE_MULTIPLIERS

# Karma points for eco actions
ECO_POINTS = {
    "CHALLENGE_PARTICIPATION": 15,
    "CHALLENGE_CREATION": 30,
    "IMPACT_DOCUMENTATION": 25,
    "COMMUNITY_ENGAGEMENT": 10
}

# Rate limits for eco actions
ECO_RATE_LIMITS = {
    "CHALLENGES_PER_DAY": 5,
    "PARTICIPATIONS_PER_DAY": 10,
    "DOCUMENTATIONS_PER_DAY": 8
}

# Challenge categories and their impact levels
CHALLENGE_CATEGORIES = {
    "WASTE_REDUCTION": {
        "points": 15,
        "impact": "STANDARD",
        "duration": 7  # days
    },
    "ENERGY_CONSERVATION": {
        "points": 20,
        "impact": "HIGH_IMPACT",
        "duration": 14
    },
    "WATER_CONSERVATION": {
        "points": 18,
        "impact": "HIGH_IMPACT",
        "duration": 14
    },
    "COMMUNITY_CLEANUP": {
        "points": 25,
        "impact": "HIGH_IMPACT",
        "duration": 1
    }
}

# Impact documentation requirements
IMPACT_DOCUMENTATION = {
    "MIN_DESCRIPTION_LENGTH": 100,
    "REQUIRED_MEDIA": True,
    "MIN_MEDIA_COUNT": 2,
    "MAX_MEDIA_COUNT": 5,
    "REQUIRED_METRICS": True
}

# Community engagement thresholds
COMMUNITY_ENGAGEMENT = {
    "MIN_PARTICIPANTS": 5,
    "MIN_DURATION": 1,  # hours
    "MAX_DURATION": 8,
    "REQUIRED_FOLLOWUP": True
} 