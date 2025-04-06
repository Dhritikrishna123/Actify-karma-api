"""Base configuration for karma system."""

# Quality multipliers range
QUALITY_MULTIPLIERS = {
    "MIN": 0.5,
    "MAX": 2.0,
    "DEFAULT": 1.0
}

# Time-based multipliers
TIME_MULTIPLIERS = {
    "QUICK_RESOLUTION_THRESHOLD": 24,  # hours
    "QUICK_RESOLUTION_BONUS": 1.2
}

# Size-based multipliers
SIZE_MULTIPLIERS = {
    "COMMUNITY_SIZE_DIVISOR": 100,
    "EVENT_ATTENDANCE_DIVISOR": 50,
    "MAX_MULTIPLIER": 2.0
}

# Verification level multipliers
VERIFICATION_MULTIPLIERS = {
    "NEW": 1.0,
    "EMAIL_VERIFIED": 1.1,
    "PHONE_VERIFIED": 1.2,
    "ID_VERIFIED": 1.3
}

# Karma decay configuration
KARMA_DECAY = {
    "HIGH_IMPACT": {
        "PERIOD": 120,  # days
        "RATE": 0.1  # 10% decay per period
    },
    "STANDARD": {
        "PERIOD": 90,
        "RATE": 0.15
    },
    "MINOR": {
        "PERIOD": 60,
        "RATE": 0.2
    }
} 