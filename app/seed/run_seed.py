"""Idempotent demo seed for 6 Hidden India destinations.

Requires SEED_DEMO=true. All rows are marked is_demo=true.
Verified-facts-only copy — no invented prices, ratings, or availability.
"""

from __future__ import annotations

import sys

from sqlalchemy import select

from app.config import get_settings
from app.db import SessionLocal
from app.models.destination import Destination
from app.models.hidden_india import HiddenIndiaStory
from app.models.trip import Trip

SEED_DESTINATIONS = [
    {
        "slug": "double-decker-living-root-bridge",
        "name": "Double Decker Living Root Bridge",
        "region": "Northeast",
        "state": "Meghalaya",
        "summary": (
            "Near Nongriat in the East Khasi Hills, the double-decker living root bridge is a "
            "Khasi-grown Ficus elastica structure formed by guiding aerial roots across a stream. "
            "It is one of Meghalaya's best-known examples of living architecture."
        ),
        "editorial": {"pull_quote": "Roots trained across water over decades, not poured in a season."},
        "hidden": {
            "slug": "hidden-living-root-bridge",
            "title": "Living Root Bridge",
            "tagline": "A Khasi bridge grown from the forest itself.",
            "layer_discover": {
                "headline": "Discover the double decker",
                "body": (
                    "The double-decker living root bridge near Nongriat spans a jungle stream with two "
                    "walkable levels of living Ficus roots. Similar single bridges appear across the Khasi "
                    "and Jaintia hills where heavy monsoon rains make lasting crossings essential."
                ),
                "tips": ["Expect a long staircase approach from Tyrna.", "Wear shoes with grip after rain."],
                "media_refs": [],
            },
            "layer_experience": {
                "headline": "Experience the approach",
                "body": (
                    "Visitors typically descend many stone steps from Tyrna village, cross smaller root bridges, "
                    "and reach Nongriat. The walk is strenuous and weather-dependent; local guides know seasonal "
                    "conditions better than any static itinerary."
                ),
                "tips": ["Start early to avoid afternoon storms.", "Carry water; village stalls vary by season."],
                "media_refs": [],
            },
            "layer_explore": {
                "headline": "Explore with Travel Jungle",
                "body": (
                    "Travel Jungle frames this place as living heritage: slow travel, respect for Khasi communities, "
                    "and no invented price tags. Demo trip notes below are illustrative only."
                ),
                "tips": ["Ask before photographing people.", "Stay on marked paths around the roots."],
                "media_refs": [],
            },
        },
        "trip": {
            "slug": "demo-root-bridge-walk",
            "title": "Demo: Root Bridge Valley Walk",
            "summary": (
                "Illustrative multi-day outline for Meghalaya's living root bridges. "
                "Demo content only — no live pricing or guaranteed departures."
            ),
            "duration_days": 4,
            "itinerary": [
                {"day": 1, "title": "Arrive Shillong region", "summary": "Settle in and brief on Khasi hill trails."},
                {"day": 2, "title": "Tyrna approach", "summary": "Descend toward Nongriat and smaller bridges."},
                {"day": 3, "title": "Double decker", "summary": "Time at the double-decker bridge and return climb."},
                {"day": 4, "title": "Buffer / departure", "summary": "Weather buffer day before onward travel."},
            ],
            "inclusions": ["Demo outline only", "No commercial inclusions claimed"],
        },
    },
    {
        "slug": "majuli",
        "name": "Majuli",
        "region": "Northeast",
        "state": "Assam",
        "summary": (
            "Majuli is a large river island in the Brahmaputra in Assam, known for Satra monasteries "
            "of the Neo-Vaishnavite tradition founded in the lineage of Srimanta Sankardev, and for "
            "Assamese cultural life shaped by the river."
        ),
        "editorial": {"note": "Island geography changes with Brahmaputra floods and erosion."},
        "hidden": {
            "slug": "hidden-majuli",
            "title": "Majuli Island",
            "tagline": "Satras, mask craft, and a living river island.",
            "layer_discover": {
                "headline": "Discover Majuli",
                "body": (
                    "Majuli sits in the Brahmaputra and is widely described as one of the world's large river "
                    "islands. Its Satras preserve dance, drama (bhaona), and manuscript traditions tied to "
                    "Assam's Neo-Vaishnavite movement."
                ),
                "tips": ["Ferry schedules depend on river levels.", "Monsoon can reshape access."],
                "media_refs": [],
            },
            "layer_experience": {
                "headline": "Experience Satra culture",
                "body": (
                    "Visitors often see monastic compounds, mask-making associated with Samaguri Satra, "
                    "and village life along embankments. Always follow Satra etiquette: modest dress and quiet respect."
                ),
                "tips": ["Remove footwear where asked.", "Ask permission before photographing rituals."],
                "media_refs": [],
            },
            "layer_explore": {
                "headline": "Explore with Travel Jungle",
                "body": (
                    "Travel Jungle treats Majuli as cultural landscape, not a checklist. Demo itineraries here "
                    "are placeholders without invented tickets or prices."
                ),
                "tips": ["Combine with Upper Assam only when travel windows allow."],
                "media_refs": [],
            },
        },
        "trip": {
            "slug": "demo-majuli-satra",
            "title": "Demo: Majuli Satra Circuit",
            "summary": "Illustrative Assam island outline. Demo only — no live availability.",
            "duration_days": 3,
            "itinerary": [
                {"day": 1, "title": "Ferry to Majuli", "summary": "Cross the Brahmaputra and settle near a Satra area."},
                {"day": 2, "title": "Satra visits", "summary": "Monastery compounds and craft workshops if open."},
                {"day": 3, "title": "Return", "summary": "River crossing back toward mainland Assam."},
            ],
            "inclusions": ["Demo outline only"],
        },
    },
    {
        "slug": "tirthan-valley",
        "name": "Tirthan Valley",
        "region": "Western Himalaya",
        "state": "Himachal Pradesh",
        "summary": (
            "Tirthan Valley in Himachal Pradesh follows the Tirthan River toward the Great Himalayan "
            "National Park (a UNESCO World Heritage site). The valley is known for trout waters, "
            "village stays, and trail access into protected high country."
        ),
        "editorial": {"note": "GHNP entry rules and permits are managed by park authorities."},
        "hidden": {
            "slug": "hidden-tirthan",
            "title": "Tirthan Valley",
            "tagline": "River villages at the edge of a World Heritage park.",
            "layer_discover": {
                "headline": "Discover Tirthan",
                "body": (
                    "The Tirthan River drains a western Himalayan catchment adjoining the Great Himalayan "
                    "National Park. Settlements such as Gushaini and Banjar serve as common bases for walks "
                    "and park approaches."
                ),
                "tips": ["Check GHNP permit requirements before planning treks.", "Nights are cold even outside winter."],
                "media_refs": [],
            },
            "layer_experience": {
                "headline": "Experience the river",
                "body": (
                    "Days often mix riverside walks, village paths, and short hikes. Fishing and park trekking "
                    "are regulated; follow local and forest department guidance."
                ),
                "tips": ["Pack layers for altitude swings.", "Respect private orchards and homestay quiet hours."],
                "media_refs": [],
            },
            "layer_explore": {
                "headline": "Explore with Travel Jungle",
                "body": (
                    "Travel Jungle highlights slow Himachal valleys without inventing lodge rates or "
                    "departure calendars. Demo trip text is illustrative."
                ),
                "tips": ["Pair with neighboring Seraj only when roads are open."],
                "media_refs": [],
            },
        },
        "trip": {
            "slug": "demo-tirthan-river",
            "title": "Demo: Tirthan River Days",
            "summary": "Illustrative Himachal valley outline. Demo only.",
            "duration_days": 4,
            "itinerary": [
                {"day": 1, "title": "Arrive valley", "summary": "Reach a Tirthan riverside base."},
                {"day": 2, "title": "Village walks", "summary": "Short trails and river viewpoints."},
                {"day": 3, "title": "Park edge", "summary": "Guided approach subject to permits."},
                {"day": 4, "title": "Depart", "summary": "Return toward Aut / Kullu corridor."},
            ],
            "inclusions": ["Demo outline only"],
        },
    },
    {
        "slug": "ziro-valley",
        "name": "Ziro Valley",
        "region": "Northeast",
        "state": "Arunachal Pradesh",
        "summary": (
            "Ziro Valley in Lower Subansiri, Arunachal Pradesh, is the homeland of the Apatani people, "
            "noted for wet-rice cultivation, pine-clad hills, and the Ziro Festival of Music held in the valley. "
            "Protected Area Permit (PAP) rules apply for many visitors to Arunachal."
        ),
        "editorial": {"note": "Confirm current PAP/ILP requirements before travel."},
        "hidden": {
            "slug": "hidden-ziro",
            "title": "Ziro Valley",
            "tagline": "Apatani fields under Arunachal pines.",
            "layer_discover": {
                "headline": "Discover Ziro",
                "body": (
                    "Ziro's Apatani plateau combines irrigated rice fields with surrounding pine forest. "
                    "The landscape is part of a proposed UNESCO tentative listing for Apatani cultural landscape "
                    "values widely cited in heritage discussions."
                ),
                "tips": ["Carry valid permits for Arunachal.", "Altitude is moderate but nights chill."],
                "media_refs": [],
            },
            "layer_experience": {
                "headline": "Experience Apatani life",
                "body": (
                    "Visitors see paddy fields, bamboo and pine villages, and seasonal cultural events. "
                    "The music festival is a modern gathering in the same valley — not a substitute for everyday Apatani life."
                ),
                "tips": ["Ask before entering private compounds.", "Dress for mud after rain."],
                "media_refs": [],
            },
            "layer_explore": {
                "headline": "Explore with Travel Jungle",
                "body": (
                    "Travel Jungle keeps Ziro India-scoped and permit-aware. Demo itineraries omit fake ticket prices."
                ),
                "tips": ["Build buffer days for road delays from Assam."],
                "media_refs": [],
            },
        },
        "trip": {
            "slug": "demo-ziro-plateau",
            "title": "Demo: Ziro Plateau Stay",
            "summary": "Illustrative Arunachal outline. Demo only.",
            "duration_days": 3,
            "itinerary": [
                {"day": 1, "title": "Reach Ziro", "summary": "Arrive via Assam corridor with permits in hand."},
                {"day": 2, "title": "Valley circuit", "summary": "Fields, viewpoints, and village walks."},
                {"day": 3, "title": "Depart", "summary": "Return toward Assam plains."},
            ],
            "inclusions": ["Demo outline only"],
        },
    },
    {
        "slug": "shnongpdeng",
        "name": "Shnongpdeng",
        "region": "Northeast",
        "state": "Meghalaya",
        "summary": (
            "Shnongpdeng is a village on the Umngot (Dawki) river in the Jaintia Hills of Meghalaya, "
            "known for unusually clear water, riverside camping zones, and proximity to the Dawki–Tamabil "
            "border crossing with Bangladesh."
        ),
        "editorial": {"note": "Water clarity varies with rainfall and upstream conditions."},
        "hidden": {
            "slug": "hidden-shnongpdeng",
            "title": "Shnongpdeng",
            "tagline": "Clear Umngot water at the Jaintia edge.",
            "layer_discover": {
                "headline": "Discover Shnongpdeng",
                "body": (
                    "Shnongpdeng sits along the Umngot River, whose clarity in fair weather makes riverbed stones "
                    "visible from boats. The wider Dawki area is a documented Meghalaya–Bangladesh frontier landscape."
                ),
                "tips": ["Clarity drops after heavy rain.", "Follow local rules on camping zones."],
                "media_refs": [],
            },
            "layer_experience": {
                "headline": "Experience the river",
                "body": (
                    "Common activities include supervised boating and riverside stays organized by local operators. "
                    "Travel Jungle does not invent capacity or price figures for these services."
                ),
                "tips": ["Life jackets where provided.", "Respect fishing and bathing customs."],
                "media_refs": [],
            },
            "layer_explore": {
                "headline": "Explore with Travel Jungle",
                "body": (
                    "Pair Shnongpdeng with other Meghalaya stories carefully — distances are short on the map "
                    "but winding on the road. Demo content only."
                ),
                "tips": ["Check road status in monsoon."],
                "media_refs": [],
            },
        },
        "trip": {
            "slug": "demo-umngot-edge",
            "title": "Demo: Umngot River Edge",
            "summary": "Illustrative Meghalaya river outline. Demo only.",
            "duration_days": 2,
            "itinerary": [
                {"day": 1, "title": "Arrive Shnongpdeng", "summary": "Riverside orientation."},
                {"day": 2, "title": "River morning", "summary": "Boat or bank time if conditions allow."},
            ],
            "inclusions": ["Demo outline only"],
        },
    },
    {
        "slug": "hampi",
        "name": "Hampi",
        "region": "Deccan",
        "state": "Karnataka",
        "summary": (
            "Hampi in Karnataka is the ruined capital of the Vijayanagara Empire and a UNESCO World Heritage Site, "
            "spread across boulder hills and the Tungabhadra River with temple complexes such as Virupaksha "
            "and the Vittala temple area."
        ),
        "editorial": {"note": "ASI-protected monuments; follow posted conservation rules."},
        "hidden": {
            "slug": "hidden-hampi",
            "title": "Hampi",
            "tagline": "Vijayanagara stone across the Tungabhadra.",
            "layer_discover": {
                "headline": "Discover Hampi",
                "body": (
                    "Hampi preserves the urban core of Vijayanagara, one of medieval South India's major capitals. "
                    "Granite temples, bazaars, and fortifications sit among iconic Deccan boulders along the Tungabhadra."
                ),
                "tips": ["Start early to avoid heat.", "Hire licensed guides for monument context."],
                "media_refs": [],
            },
            "layer_experience": {
                "headline": "Experience the sacred core",
                "body": (
                    "Virupaksha remains an active temple; other zones are archaeological parks. "
                    "Sunrise and sunset light on the boulders is well known — without needing invented 'best view' rankings."
                ),
                "tips": ["Cover shoulders at active shrines.", "Do not climb fragile structures."],
                "media_refs": [],
            },
            "layer_explore": {
                "headline": "Explore with Travel Jungle",
                "body": (
                    "Travel Jungle presents Hampi as layered history, not a race through ticket gates. "
                    "Demo trip notes omit fake pricing."
                ),
                "tips": ["Combine with Anegundi across the river when ferries run."],
                "media_refs": [],
            },
        },
        "trip": {
            "slug": "demo-hampi-stones",
            "title": "Demo: Hampi Heritage Walks",
            "summary": "Illustrative Karnataka outline. Demo only.",
            "duration_days": 3,
            "itinerary": [
                {"day": 1, "title": "Sacred centre", "summary": "Virupaksha and nearby bazaar ruins."},
                {"day": 2, "title": "Royal & Vittala", "summary": "Royal enclosure and Vittala complex."},
                {"day": 3, "title": "River & departure", "summary": "Tungabhadra views and onward travel."},
            ],
            "inclusions": ["Demo outline only"],
        },
    },
]


def run() -> None:
    settings = get_settings()
    if not settings.seed_demo:
        print("SEED_DEMO is not true; refusing to seed.", file=sys.stderr)
        sys.exit(1)

    db = SessionLocal()
    created_dest = 0
    created_hidden = 0
    created_trips = 0
    try:
        for item in SEED_DESTINATIONS:
            dest = db.scalar(select(Destination).where(Destination.slug == item["slug"]))
            if not dest:
                dest = Destination(
                    slug=item["slug"],
                    name=item["name"],
                    region=item["region"],
                    state=item["state"],
                    summary=item["summary"],
                    hero_image_url=None,
                    editorial=item.get("editorial"),
                    is_published=True,
                    is_demo=True,
                )
                db.add(dest)
                db.flush()
                created_dest += 1

            hidden_data = item["hidden"]
            existing_hidden = db.scalar(
                select(HiddenIndiaStory).where(HiddenIndiaStory.slug == hidden_data["slug"])
            )
            if not existing_hidden:
                db.add(
                    HiddenIndiaStory(
                        slug=hidden_data["slug"],
                        destination_id=dest.id,
                        title=hidden_data["title"],
                        tagline=hidden_data["tagline"],
                        layer_discover=hidden_data["layer_discover"],
                        layer_experience=hidden_data["layer_experience"],
                        layer_explore=hidden_data["layer_explore"],
                        is_published=True,
                        is_demo=True,
                    )
                )
                created_hidden += 1

            trip_data = item["trip"]
            existing_trip = db.scalar(select(Trip).where(Trip.slug == trip_data["slug"]))
            if not existing_trip:
                db.add(
                    Trip(
                        slug=trip_data["slug"],
                        destination_id=dest.id,
                        title=trip_data["title"],
                        summary=trip_data["summary"],
                        duration_days=trip_data.get("duration_days"),
                        itinerary=trip_data.get("itinerary"),
                        inclusions=trip_data.get("inclusions"),
                        hero_image_url=None,
                        is_published=True,
                        is_demo=True,
                    )
                )
                created_trips += 1

        db.commit()
        print(
            f"Seed complete (idempotent). destinations+={created_dest} "
            f"hidden+={created_hidden} trips+={created_trips}"
        )
    finally:
        db.close()


if __name__ == "__main__":
    run()
