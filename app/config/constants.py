# All constant values (points, thresholds)

# Karma System Constants

# User Verification Levels
VERIFICATION_LEVELS = {
    "NEW": 0,
    "EMAIL_VERIFIED": 1,
    "PHONE_VERIFIED": 2,
    "ID_VERIFIED": 3
}

# Report Categories
REPORT_CATEGORIES = {
    "INFRASTRUCTURE": {
        "POTHOLE": "Pothole",
        "BROKEN_ROAD": "Broken Road/Sidewalk",
        "TRAFFIC_SIGNAL": "Traffic Signal Malfunction",
        "DAMAGED_SIGNAGE": "Damaged Signage",
        "BRIDGE_DAMAGE": "Bridge or Overpass Damage"
    },
    "ENVIRONMENTAL": {
        "GARBAGE": "Garbage Dumping",
        "BURNING": "Open Burning",
        "VEGETATION": "Overgrown Vegetation",
        "POLLUTION": "Pollution",
        "WATER": "Stagnant Water"
    }
}

# Karma Points Configuration
KARMA_POINTS = {
    "REPORT_CREATION": 10,
    "REPORT_VERIFICATION": 20,
    "REPORT_RESOLUTION": 50,
    "ENDORSEMENT": 5
}

# Time Constants (in days)
TIME_CONSTANTS = {
    "KARMA_DECAY_PERIOD": {
        "HIGH_IMPACT": 120,
        "STANDARD": 90,
        "MINOR": 60
    }
}

# Rate Limiting
RATE_LIMITS = {
    "REPORTS_PER_DAY": 10,
    "ENDORSEMENTS_PER_DAY": 20
}
