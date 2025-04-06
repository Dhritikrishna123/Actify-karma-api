"""Community karma configuration."""

from .base_config import QUALITY_MULTIPLIERS, SIZE_MULTIPLIERS

# Karma points for community actions
COMMUNITY_POINTS = {
    "COMMUNITY_CREATION": 30,
    "EVENT_ORGANIZATION": 25,
    "MENTORSHIP": 20,
    "COMMUNITY_MODERATION": 15
}

# Rate limits for community actions
COMMUNITY_RATE_LIMITS = {
    "COMMUNITIES_PER_DAY": 3,
    "EVENTS_PER_DAY": 5,
    "MENTORSHIPS_PER_DAY": 2
}

# Community types and their requirements
COMMUNITY_TYPES = {
    "LOCAL": {
        "min_members": 10,
        "max_members": 1000,
        "base_points": 25
    },
    "INTEREST": {
        "min_members": 5,
        "max_members": 5000,
        "base_points": 20
    },
    "PROFESSIONAL": {
        "min_members": 20,
        "max_members": 2000,
        "base_points": 30
    }
}

# Event organization requirements
EVENT_REQUIREMENTS = {
    "MIN_DESCRIPTION_LENGTH": 100,
    "MIN_DURATION": 1,  # hours
    "MAX_DURATION": 8,
    "REQUIRED_REGISTRATION": True,
    "MIN_ATTENDANCE": 5
}

# Mentorship program requirements
MENTORSHIP_REQUIREMENTS = {
    "MIN_DURATION": 1,  # months
    "MAX_DURATION": 12,
    "MIN_SESSIONS": 4,
    "REQUIRED_PROGRESS_TRACKING": True,
    "MIN_PROGRESS_UPDATES": 2
}

# Moderation quality thresholds
MODERATION_THRESHOLDS = {
    "MIN_ACTIONS_PER_DAY": 5,
    "MAX_ACTIONS_PER_DAY": 50,
    "REQUIRED_REPORTING": True,
    "MIN_RESPONSE_TIME": 24  # hours
} 