from django.db import models
from django.utils.translation import gettext_lazy as _


class EventTypeChoices(models.TextChoices):
    CONFERENCE = "conference", _("Conference")
    WEBINAR = "webinar", _("Webinar")
    WORKSHOP = "workshop", _("Workshop")
    MEETUP = "meetup", _("Meetup")
    NETWORKING = "networking", _("Networking Event")
    TRADE_SHOW = "trade_show", _("Trade Show / Expo")
    SEMINAR = "seminar", _("Seminar")
    PANEL_DISCUSSION = "panel_discussion", _("Panel Discussion")
    FESTIVAL = "festival", _("Festival")
    LECTURE = "lecture", _("Lecture")
    ROUNDTABLE = "roundtable", _("Roundtable")
    HACKATHON = "hackathon", _("Hackathon")
    RETREAT = "retreat", _("Retreat")
    SUMMIT = "summit", _("Summit")
    PRODUCT_LAUNCH = "product_launch", _("Product Launch")
    AWARD_CEREMONY = "award_ceremony", _("Award Ceremony")
    CHARITY_EVENT = "charity_event", _("Charity Event")
    TEAM_BUILDING = "team_building", _("Team Building")
    TRAINING_SESSION = "training_session", _("Training Session")
    EXHIBITION = "exhibition", _("Exhibition")
    CONFERENCE_CALL = "conference_call", _("Conference Call / Virtual Meeting")
    OPEN_HOUSE = "open_house", _("Open House")
    TOWN_HALL = "town_hall", _("Town Hall")
    QA_SESSION = "qa_session", _("Q&A Session")


class LocationTypeChoices(models.TextChoices):
    VIRTUAL = "virtual", _("Virtual")
    IN_PERSON = "in_person", _("In-Person")
    HYBRID = "hybrid", _("Hybrid")
