"""Skill karma configuration."""

from .base_config import QUALITY_MULTIPLIERS, VERIFICATION_MULTIPLIERS

# Karma points for skill actions
SKILL_POINTS = {
    "SKILL_LISTING": 20,
    "SERVICE_COMPLETION": 30,
    "SKILL_VERIFICATION": 25,
    "SERVICE_REVIEW": 10
}

# Rate limits for skill actions
SKILL_RATE_LIMITS = {
    "LISTINGS_PER_DAY": 5,
    "REVIEWS_PER_DAY": 10,
    "VERIFICATIONS_PER_DAY": 8
}

# Skill categories and their base values
SKILL_CATEGORIES = {
    "TECHNICAL": {
        "base_points": 25,
        "verification_required": True,
        "min_experience": 1  # years
    },
    "CREATIVE": {
        "base_points": 20,
        "verification_required": False,
        "min_experience": 0.5
    },
    "PROFESSIONAL": {
        "base_points": 30,
        "verification_required": True,
        "min_experience": 2
    },
    "LIFESTYLE": {
        "base_points": 15,
        "verification_required": False,
        "min_experience": 0.5
    }
}

# Service completion requirements
SERVICE_COMPLETION = {
    "MIN_DESCRIPTION_LENGTH": 100,
    "REQUIRED_MEDIA": True,
    "MIN_MEDIA_COUNT": 1,
    "MAX_MEDIA_COUNT": 5,
    "REQUIRED_CLIENT_FEEDBACK": True
}

# Review quality thresholds
REVIEW_THRESHOLDS = {
    "MIN_DESCRIPTION_LENGTH": 50,
    "MIN_RATING": 1,
    "MAX_RATING": 5,
    "REQUIRED_DETAILS": True
}

# Verification requirements
VERIFICATION_REQUIREMENTS = {
    "MIN_EVIDENCE_COUNT": 2,
    "MAX_EVIDENCE_COUNT": 5,
    "REQUIRED_ENDORSEMENTS": 3,
    "MIN_ENDORSEMENT_RATING": 4
} 