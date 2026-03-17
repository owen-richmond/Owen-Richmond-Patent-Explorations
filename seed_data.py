"""
Seed / sample patent dataset for the NewSpace dashboard.
Based on publicly documented patent portfolios (as of 2025).
Used when real API data has not yet been fetched.

Includes a curated SpaceX Starlink phased-array antenna family
with realistic prosecution history for the family tree panel.
"""

import pandas as pd
import numpy as np

# ── Per-company patent title lists ────────────────────────────────────────────

SPACEX_TITLES = [
    ("Phased array antenna for low Earth orbit satellite communication", "H04B7/195", "Satellite / Wireless Comms"),
    ("User terminal for satellite broadband internet access", "H04W84/06", "Satellite / Wireless Comms"),
    ("Flat panel antenna with electronically steerable beam", "H01Q3/26", "Antenna Design"),
    ("Low-latency network routing for LEO satellite constellations", "H04L45/00", "Satellite / Wireless Comms"),
    ("Satellite bus thermal management system", "B64G1/50", "Spacecraft / Launch Systems"),
    ("Intersatellite optical communication link system", "H04B10/00", "Satellite / Wireless Comms"),
    ("Ground terminal tracking antenna with MEMS steering", "H01Q3/22", "Antenna Design"),
    ("Radio frequency interference mitigation for satellite terminals", "H04B1/10", "Satellite / Wireless Comms"),
    ("Propellant mass gauging for spacecraft", "B64G1/40", "Spacecraft / Launch Systems"),
    ("Satellite constellation deployment and maintenance", "B64G1/10", "Spacecraft / Launch Systems"),
    ("Wideband phased array with digital beamforming", "H01Q21/00", "Antenna Design"),
    ("Frequency allocation system for broadband satellite networks", "H04W16/14", "Satellite / Wireless Comms"),
    ("Reusable rocket landing leg deployment mechanism", "B64G1/62", "Spacecraft / Launch Systems"),
    ("Cryogenic propellant transfer in microgravity", "F17C7/00", "Spacecraft / Launch Systems"),
    ("Thermal protection tiles for reusable launch vehicles", "B64C1/38", "Aeronautics / Structures"),
    ("High-gain antenna with automated pointing for moving platforms", "H01Q1/32", "Antenna Design"),
    ("Satellite attitude control via reaction wheels", "B64G1/28", "Spacecraft / Launch Systems"),
    ("Link budget optimization for satellite broadband", "H04B7/185", "Satellite / Wireless Comms"),
    ("Phased array calibration system and method", "H01Q3/00", "Antenna Design"),
    ("Signal processing for satellite uplink interference rejection", "H04B7/15", "Signal Processing"),
    ("LEO satellite handover management for ground users", "H04W36/00", "Satellite / Wireless Comms"),
    ("Metasurface-based flat lens antenna", "H01Q15/00", "Antenna Design"),
    ("Ground station diversity for satellite communications", "H04B7/12", "Satellite / Wireless Comms"),
    ("Integrated modem for satellite internet terminals", "H04L27/00", "Signal Processing"),
    ("Attitude and orbit control for satellite formation flying", "B64G1/36", "Spacecraft / Launch Systems"),
    ("Satellite solar array deployment mechanism", "B64G1/44", "Spacecraft / Launch Systems"),
    ("Multi-beam satellite communications payload", "H04B7/204", "Satellite / Wireless Comms"),
    ("Carbon fiber composite rocket body structure", "B64C1/00", "Aeronautics / Structures"),
    ("Regenerative heat exchanger for rocket engines", "F02K9/00", "Rocket Propulsion"),
    ("Autonomous drone ship precision landing system", "B64G5/00", "Spacecraft / Launch Systems"),
    ("High-volume manufacturing methods for satellite hardware", "B64G1/00", "Spacecraft / Launch Systems"),
    ("Mesh networking protocol for satellite constellations", "H04L12/00", "Satellite / Wireless Comms"),
    ("RF power amplifier for phased array transmitter modules", "H03F3/00", "Signal Processing"),
    ("User scheduling for multi-beam satellite broadband", "H04W72/00", "Satellite / Wireless Comms"),
    ("Polar orbit satellite coverage optimization", "H04B7/195", "Satellite / Wireless Comms"),
    ("Satellite lifetime propulsion management system", "B64G1/26", "Spacecraft / Launch Systems"),
    ("GaN-based transmit/receive module for satellite antennas", "H01Q21/06", "Antenna Design"),
    ("Deployable reflector with shape-memory actuators", "H01Q15/14", "Antenna Design"),
    ("On-orbit servicing interface for modular satellites", "B64G4/00", "Spacecraft / Launch Systems"),
    ("Digital channelizer for satellite payload processing", "H04J4/00", "Signal Processing"),
    ("Satellite constellation collision avoidance maneuver planning", "B64G1/10", "Spacecraft / Launch Systems"),
    ("Adaptive modulation and coding for satellite links", "H04L1/00", "Satellite / Wireless Comms"),
    ("Electronically scanned array with reconfigurable aperture", "H01Q3/44", "Antenna Design"),
    ("Space-ground network protocol for low-latency services", "H04L47/00", "Satellite / Wireless Comms"),
    ("Thermal-electric power management for CubeSat class satellites", "H02J7/00", "Power / Electrical Systems"),
    ("Optical inter-satellite crosslink terminal design", "H04B10/112", "Satellite / Wireless Comms"),
    ("Propellant-free satellite attitude control using momentum wheels", "B64G1/28", "Spacecraft / Launch Systems"),
    ("Re-entry vehicle thermal protection using ablative materials", "B64G1/58", "Spacecraft / Launch Systems"),
    ("Electric propulsion system for station keeping in LEO", "B64G1/40", "Spacecraft / Launch Systems"),
    ("Launch vehicle interstage separation mechanism", "B64G1/64", "Spacecraft / Launch Systems"),
]

BLUE_ORIGIN_TITLES = [
    ("Reusable suborbital launch vehicle with powered vertical landing", "B64G1/62", "Spacecraft / Launch Systems"),
    ("Crew capsule abort system for launch vehicles", "B64G1/64", "Spacecraft / Launch Systems"),
    ("Cryogenic engine throttling system for reusable rockets", "F02K9/58", "Rocket Propulsion"),
    ("BE-3 liquid hydrogen and liquid oxygen rocket engine", "F02K9/00", "Rocket Propulsion"),
    ("Large diameter composite pressure vessel for launch vehicles", "B64C1/06", "Aeronautics / Structures"),
    ("Propellant settling maneuver for in-space cryogenic tanks", "F17C7/00", "Spacecraft / Launch Systems"),
    ("Integrated launch and recovery operations control system", "B64G5/00", "Spacecraft / Launch Systems"),
    ("Blue Ring orbital transfer vehicle propulsion architecture", "B64G1/40", "Spacecraft / Launch Systems"),
    ("Turbopump for cryogenic rocket propellants", "F04D25/00", "Rocket Propulsion"),
    ("Vertical takeoff and landing propulsion control law", "B64C29/00", "Aeronautics / Structures"),
    ("BE-4 liquefied natural gas rocket engine combustion chamber", "F02K9/10", "Rocket Propulsion"),
    ("Thrust vector control actuator for launch vehicles", "B64G1/26", "Spacecraft / Launch Systems"),
    ("Space habitat environmental control and life support system", "B64G1/58", "Spacecraft / Launch Systems"),
    ("Lunar lander descent propulsion system", "B64G1/62", "Spacecraft / Launch Systems"),
    ("Reentry aeroshell thermal protection system", "B64G1/58", "Spacecraft / Launch Systems"),
    ("BE-7 LOX/hydrogen engine for lunar lander", "F02K9/00", "Rocket Propulsion"),
    ("Propulsion feed system with passive pressurant", "F02K9/44", "Rocket Propulsion"),
    ("Rotating detonation rocket engine cycle", "F02K7/00", "Rocket Propulsion"),
    ("Recovery parachute system for reusable crew capsule", "B64D17/00", "Aeronautics / Structures"),
    ("Lightweight composite tank manufacturing for cryogenic propellants", "B64G1/40", "Spacecraft / Launch Systems"),
    ("Reusable first stage booster guidance during powered descent", "B64G1/62", "Spacecraft / Launch Systems"),
    ("Variable thrust liquid rocket engine for throttleable descent", "F02K9/58", "Rocket Propulsion"),
    ("Acoustic suppression system for rocket test stand", "F02K9/00", "Rocket Propulsion"),
    ("Advanced composite nosecone for suborbital vehicles", "B64C1/00", "Aeronautics / Structures"),
    ("Pressure-fed bipropellant thruster for orbital maneuvering", "F02K9/44", "Rocket Propulsion"),
    ("Staged combustion cycle engine with full flow oxidizer preburner", "F02K9/10", "Rocket Propulsion"),
    ("Launch pad infrastructure for rapid booster reuse", "B64G5/00", "Spacecraft / Launch Systems"),
    ("Thermal insulation system for cryogenic propellant storage", "F17C3/00", "Spacecraft / Launch Systems"),
]

ROCKET_LAB_TITLES = [
    ("Carbon fiber rocket fuselage construction and bonding method", "B64C1/00", "Aeronautics / Structures"),
    ("Electric turbopump for LOX/kerosene small launch vehicle", "F04D25/00", "Rocket Propulsion"),
    ("Photon satellite bus modular avionics architecture", "B64G1/10", "Spacecraft / Launch Systems"),
    ("Battery-powered turbopump for small launch vehicles", "F04D25/00", "Rocket Propulsion"),
    ("Kick stage in-space propulsion for precision orbit insertion", "B64G1/40", "Spacecraft / Launch Systems"),
    ("Small satellite dispenser mechanism", "B64G1/64", "Spacecraft / Launch Systems"),
    ("Attitude determination system for small satellites", "B64G1/36", "Spacecraft / Launch Systems"),
    ("Rapid integration launch operations for small launch vehicles", "B64G5/00", "Spacecraft / Launch Systems"),
    ("Cubesat-compatible monopropellant propulsion module", "B64G1/40", "Spacecraft / Launch Systems"),
    ("Composite overwrapped pressure vessel for small spacecraft", "B64C1/06", "Aeronautics / Structures"),
    ("Electron booster guided atmospheric descent and recovery", "B64G1/62", "Spacecraft / Launch Systems"),
    ("Mid-air capture system for rocket booster recovery", "B64G5/00", "Spacecraft / Launch Systems"),
    ("Space solar power demonstration payload architecture", "H02S10/40", "Power / Electrical Systems"),
    ("Autonomous mission operations for satellite constellations", "B64G1/24", "Spacecraft / Launch Systems"),
    ("Optical inter-satellite link terminal for small satellites", "H04B10/11", "Satellite / Wireless Comms"),
    ("Additive manufactured rocket engine injector plate", "F02K9/00", "Rocket Propulsion"),
    ("Reusable fairing half-shell with guided recovery system", "B64G1/64", "Spacecraft / Launch Systems"),
    ("Propellant management device for zero-gravity operation", "B64G1/40", "Spacecraft / Launch Systems"),
]

VIRGIN_GALACTIC_TITLES = [
    ("SpaceShipTwo hybrid rocket motor design", "F02K9/00", "Rocket Propulsion"),
    ("Feathering reentry mechanism for suborbital spaceplane", "B64C3/38", "Aeronautics / Structures"),
    ("Carrier aircraft structural integration for air-launched vehicles", "B64C1/00", "Aeronautics / Structures"),
    ("Hybrid solid propellant grain for spaceplane motor", "C06B21/00", "Other"),
    ("Crew cabin pressurization and environmental control for spaceplane", "B64D13/00", "Aeronautics / Structures"),
    ("Passenger restraint system for commercial suborbital flight", "B64D11/00", "Aeronautics / Structures"),
    ("Acoustic signature reduction for air-launched rockets", "B64D27/00", "Aeronautics / Structures"),
    ("Thermal management for reusable composite spaceplane fuselage", "B64C1/38", "Aeronautics / Structures"),
    ("Lifting body aerodynamic control surfaces for reentry", "B64C30/00", "Aeronautics / Structures"),
    ("Reaction control system thruster for suborbital vehicles", "B64G1/26", "Spacecraft / Launch Systems"),
    ("Automated pre-flight checklist system for commercial spaceflight", "G05D1/00", "Computing / Software"),
    ("Hybrid motor oxidizer injection system", "F02K9/72", "Rocket Propulsion"),
    ("Spaceplane wing structural reinforcement under rocket thrust", "B64C3/18", "Aeronautics / Structures"),
    ("Cabin window assembly for high-altitude pressure differential", "B64C1/14", "Aeronautics / Structures"),
]


# ── Curated SpaceX phased-array antenna patent family ─────────────────────────
# Models a realistic prosecution history: original US application ->
# continuation chain -> PCT -> national phase entries -> divisional

STARLINK_ANTENNA_FAMILY = [
    {
        "node_id": "SX-PA-001",
        "pub_number": "US10236574B2",
        "title": "Phased array antenna for low Earth orbit satellite communication",
        "filing_type": "Priority Application",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2016-01-20",
        "filing_year": 2016,
        "grant_date": "2019-03-19",
        "cpc_codes": "H01Q3/26|H04B7/195|H01Q21/06",
        "tech_category": "Antenna Design",
        "abstract": (
            "A phased array antenna system for communication with low Earth orbit satellites, "
            "comprising a plurality of antenna elements arranged to provide electronically steerable "
            "beams with low latency pointing for broadband user terminals."
        ),
        "parent_id": None,
        "relationship": None,
        "claims_count": 24,
        "inventors": "Jorgensen, Mark; Kim, David; Patel, Sarah",
        "family_id": "FAM-SX-ANT-001",
    },
    {
        "node_id": "SX-PA-002",
        "pub_number": "WO2017127323A1",
        "title": "Phased array antenna for satellite communication — international filing",
        "filing_type": "PCT Application",
        "status": "pending",
        "jurisdiction": "WO",
        "filing_date": "2017-01-19",
        "filing_year": 2017,
        "grant_date": None,
        "cpc_codes": "H01Q3/26|H04B7/195",
        "tech_category": "Antenna Design",
        "abstract": (
            "International patent application claiming priority to US15/001234, directed to "
            "phased array antenna systems for broadband satellite internet terminals."
        ),
        "parent_id": "SX-PA-001",
        "relationship": "PCT",
        "claims_count": 20,
        "inventors": "Jorgensen, Mark; Kim, David; Patel, Sarah",
        "family_id": "FAM-SX-ANT-001",
    },
    {
        "node_id": "SX-PA-003",
        "pub_number": "US10651566B2",
        "title": "Phased array antenna with adaptive beam steering for satellite terminals",
        "filing_type": "Continuation",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2018-03-15",
        "filing_year": 2018,
        "grant_date": "2020-05-12",
        "cpc_codes": "H01Q3/26|H04B7/195|H01Q3/22",
        "tech_category": "Antenna Design",
        "abstract": (
            "A continuation of US10236574, adding claims directed to adaptive beam steering "
            "algorithms for tracking LEO satellites across the sky at high angular rates."
        ),
        "parent_id": "SX-PA-001",
        "relationship": "Continuation",
        "claims_count": 18,
        "inventors": "Jorgensen, Mark; Kim, David; Torres, Carlos",
        "family_id": "FAM-SX-ANT-001",
    },
    {
        "node_id": "SX-PA-004",
        "pub_number": "EP3407479B1",
        "title": "Phased array antenna for satellite communication (EP)",
        "filing_type": "EP National Phase",
        "status": "granted",
        "jurisdiction": "EP",
        "filing_date": "2018-07-20",
        "filing_year": 2018,
        "grant_date": "2021-04-14",
        "cpc_codes": "H01Q3/26|H04B7/195",
        "tech_category": "Antenna Design",
        "abstract": (
            "European national phase entry of WO2017127323, granted after substantive examination "
            "by the European Patent Office with amended claims directed to terminal hardware."
        ),
        "parent_id": "SX-PA-002",
        "relationship": "EP National Phase",
        "claims_count": 15,
        "inventors": "Jorgensen, Mark; Kim, David; Patel, Sarah",
        "family_id": "FAM-SX-ANT-001",
    },
    {
        "node_id": "SX-PA-005",
        "pub_number": "JP6887462B2",
        "title": "Phased array antenna for satellite communication (JP)",
        "filing_type": "JP National Phase",
        "status": "granted",
        "jurisdiction": "JP",
        "filing_date": "2018-07-20",
        "filing_year": 2018,
        "grant_date": "2021-05-19",
        "cpc_codes": "H01Q3/26|H04B7/195",
        "tech_category": "Antenna Design",
        "abstract": (
            "Japan national phase entry of WO2017127323, granted by the Japan Patent Office "
            "covering phased array antenna systems for broadband satellite services."
        ),
        "parent_id": "SX-PA-002",
        "relationship": "JP National Phase",
        "claims_count": 12,
        "inventors": "Jorgensen, Mark; Kim, David; Patel, Sarah",
        "family_id": "FAM-SX-ANT-001",
    },
    {
        "node_id": "SX-PA-006",
        "pub_number": "CN109075454B",
        "title": "Phased array antenna for satellite communication (CN)",
        "filing_type": "CN National Phase",
        "status": "granted",
        "jurisdiction": "CN",
        "filing_date": "2018-09-18",
        "filing_year": 2018,
        "grant_date": "2022-01-07",
        "cpc_codes": "H01Q3/26|H04B7/195",
        "tech_category": "Antenna Design",
        "abstract": (
            "China national phase entry of WO2017127323, granted by CNIPA after prosecution "
            "including responses to office actions relating to claim scope."
        ),
        "parent_id": "SX-PA-002",
        "relationship": "CN National Phase",
        "claims_count": 10,
        "inventors": "Jorgensen, Mark; Kim, David; Patel, Sarah",
        "family_id": "FAM-SX-ANT-001",
    },
    {
        "node_id": "SX-PA-007",
        "pub_number": "CA3012101A1",
        "title": "Phased array antenna for satellite communication (CA)",
        "filing_type": "CA National Phase",
        "status": "pending",
        "jurisdiction": "CA",
        "filing_date": "2018-07-20",
        "filing_year": 2018,
        "grant_date": None,
        "cpc_codes": "H01Q3/26|H04B7/195",
        "tech_category": "Antenna Design",
        "abstract": (
            "Canada national phase entry of WO2017127323, currently pending examination "
            "at the Canadian Intellectual Property Office."
        ),
        "parent_id": "SX-PA-002",
        "relationship": "CA National Phase",
        "claims_count": 18,
        "inventors": "Jorgensen, Mark; Kim, David; Patel, Sarah",
        "family_id": "FAM-SX-ANT-001",
    },
    {
        "node_id": "SX-PA-008",
        "pub_number": "US11005188B2",
        "title": "Beam steering method and apparatus for satellite user terminal",
        "filing_type": "Divisional",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2020-02-25",
        "filing_year": 2020,
        "grant_date": "2021-05-11",
        "cpc_codes": "H01Q3/26|H04B7/195|H04W36/00",
        "tech_category": "Antenna Design",
        "abstract": (
            "A divisional of US10236574, directed to method claims for dynamically steering "
            "phased array antenna beams to maintain link with passing LEO satellites."
        ),
        "parent_id": "SX-PA-001",
        "relationship": "Divisional",
        "claims_count": 16,
        "inventors": "Jorgensen, Mark; Kim, David",
        "family_id": "FAM-SX-ANT-001",
    },
    {
        "node_id": "SX-PA-009",
        "pub_number": "US11296426B2",
        "title": "Phased array antenna with MIMO capability for satellite broadband",
        "filing_type": "Continuation",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2021-02-01",
        "filing_year": 2021,
        "grant_date": "2022-04-05",
        "cpc_codes": "H01Q3/26|H01Q21/00|H04B7/0456",
        "tech_category": "Antenna Design",
        "abstract": (
            "A continuation of US10651566, adding claims directed to MIMO spatial multiplexing "
            "configurations for phased array satellite terminals to improve throughput."
        ),
        "parent_id": "SX-PA-003",
        "relationship": "Continuation",
        "claims_count": 22,
        "inventors": "Kim, David; Torres, Carlos; Walsh, Emily",
        "family_id": "FAM-SX-ANT-001",
    },
    {
        "node_id": "SX-PA-010",
        "pub_number": "US20210384631A1",
        "title": "Electronically steerable antenna with reconfigurable aperture for satellite terminals",
        "filing_type": "Continuation-in-Part",
        "status": "pending",
        "jurisdiction": "US",
        "filing_date": "2021-08-16",
        "filing_year": 2021,
        "grant_date": None,
        "cpc_codes": "H01Q3/44|H01Q21/00|H04B7/195",
        "tech_category": "Antenna Design",
        "abstract": (
            "A continuation-in-part of US10651566 introducing new matter directed to "
            "reconfigurable aperture configurations allowing software-defined beam patterns."
        ),
        "parent_id": "SX-PA-003",
        "relationship": "Continuation-in-Part",
        "claims_count": 28,
        "inventors": "Torres, Carlos; Walsh, Emily; Nguyen, Linh",
        "family_id": "FAM-SX-ANT-001",
    },
    {
        "node_id": "SX-PA-011",
        "pub_number": "AU2017210840B2",
        "title": "Phased array antenna for satellite communication (AU)",
        "filing_type": "AU National Phase",
        "status": "granted",
        "jurisdiction": "AU",
        "filing_date": "2018-07-20",
        "filing_year": 2018,
        "grant_date": "2020-11-12",
        "cpc_codes": "H01Q3/26|H04B7/195",
        "tech_category": "Antenna Design",
        "abstract": (
            "Australia national phase entry of WO2017127323, granted by IP Australia "
            "covering the core phased array terminal architecture."
        ),
        "parent_id": "SX-PA-002",
        "relationship": "AU National Phase",
        "claims_count": 14,
        "inventors": "Jorgensen, Mark; Kim, David; Patel, Sarah",
        "family_id": "FAM-SX-ANT-001",
    },
    {
        "node_id": "SX-PA-012",
        "pub_number": "US11588228B2",
        "title": "Low-power phased array antenna for satellite IoT terminal",
        "filing_type": "Continuation",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2022-03-10",
        "filing_year": 2022,
        "grant_date": "2023-02-21",
        "cpc_codes": "H01Q3/26|H04B7/195|H04W84/18",
        "tech_category": "Antenna Design",
        "abstract": (
            "A continuation of US11296426, narrowing claims to low-power configurations "
            "targeting IoT and machine-type communication use cases on the Starlink network."
        ),
        "parent_id": "SX-PA-009",
        "relationship": "Continuation",
        "claims_count": 14,
        "inventors": "Kim, David; Walsh, Emily",
        "family_id": "FAM-SX-ANT-001",
    },
]


# ── Helper to build the general patent rows ───────────────────────────────────

def _make_patents(titles_cpcs: list, company: str, year_range: tuple, grant_rate: float) -> list:
    rng = np.random.default_rng(hash(company) % (2**32))
    rows = []
    filing_years = rng.integers(year_range[0], year_range[1], size=len(titles_cpcs))
    jurisdictions = rng.choice(["US", "US", "US", "US", "WO", "EP"], size=len(titles_cpcs))

    for i, (title, cpc, category) in enumerate(titles_cpcs):
        fy = int(filing_years[i])
        granted = rng.random() < grant_rate
        status = "granted" if granted else "pending"
        pub_year = fy + rng.integers(1, 4)

        rows.append({
            "company": company,
            "lens_id": f"SEED-{company[:3].upper()}-{i:04d}",
            "pub_number": f"{jurisdictions[i]}{10000000 + i + hash(company) % 100000:09d}",
            "title": title,
            "abstract": f"[Sample] {title}.",
            "pub_type": "granted_patent" if granted else "patent_application",
            "status": status,
            "assignee": company,
            "jurisdiction": jurisdictions[i],
            "filing_date": f"{fy}-{rng.integers(1,13):02d}-{rng.integers(1,29):02d}",
            "filing_year": fy,
            "pub_date": f"{pub_year}-{rng.integers(1,13):02d}-{rng.integers(1,29):02d}",
            "pub_year": int(pub_year),
            "cpc_codes": cpc,
            "tech_category": category,
            "inventor_count": int(rng.integers(1, 7)),
            "family_id": f"FAM-{company[:3].upper()}-{i // 3:04d}",
            "family_size": int(rng.integers(1, 8)),
            # Fields only used by family tree panel
            "filing_type": None,
            "parent_id": None,
            "relationship": None,
            "claims_count": int(rng.integers(8, 30)),
            "inventors": "",
        })
    return rows


def get_sample_data() -> pd.DataFrame:
    """Return a realistic sample dataset for the dashboard."""
    all_rows = []
    all_rows.extend(_make_patents(SPACEX_TITLES,          "SpaceX",         (2014, 2025), 0.65))
    all_rows.extend(_make_patents(BLUE_ORIGIN_TITLES,     "Blue Origin",    (2013, 2025), 0.70))
    all_rows.extend(_make_patents(ROCKET_LAB_TITLES,      "Rocket Lab",     (2016, 2025), 0.55))
    all_rows.extend(_make_patents(VIRGIN_GALACTIC_TITLES, "Virgin Galactic", (2010, 2025), 0.60))

    # Replace the first SpaceX family with the curated antenna family so the
    # family tree panel has rich, realistic prosecution history.
    antenna_rows = []
    for rec in STARLINK_ANTENNA_FAMILY:
        antenna_rows.append({
            "company": "SpaceX",
            "lens_id": rec["node_id"],
            "pub_number": rec["pub_number"],
            "title": rec["title"],
            "abstract": rec["abstract"],
            "pub_type": "granted_patent" if rec["status"] == "granted" else "patent_application",
            "status": rec["status"],
            "assignee": "Space Exploration Technologies Corp",
            "jurisdiction": rec["jurisdiction"],
            "filing_date": rec["filing_date"],
            "filing_year": rec["filing_year"],
            "pub_date": rec.get("grant_date") or "",
            "pub_year": int(rec["grant_date"][:4]) if rec.get("grant_date") else None,
            "cpc_codes": rec["cpc_codes"],
            "tech_category": rec["tech_category"],
            "inventor_count": len(rec["inventors"].split(";")),
            "family_id": rec["family_id"],
            "family_size": len(STARLINK_ANTENNA_FAMILY),
            "filing_type": rec["filing_type"],
            "parent_id": rec["parent_id"],
            "relationship": rec["relationship"],
            "claims_count": rec["claims_count"],
            "inventors": rec["inventors"],
        })

    df = pd.DataFrame(all_rows)
    df_antenna = pd.DataFrame(antenna_rows)
    # Remove any existing FAM-SPA-0000 rows and substitute the curated family
    df = df[df["family_id"] != "FAM-SPA-0000"]
    df = pd.concat([df, df_antenna], ignore_index=True)
    return df


def get_antenna_family() -> list[dict]:
    return STARLINK_ANTENNA_FAMILY


# ── Blue Origin VTOL reusable landing family ─────────────────────────────────
# US8678321B2 — the patent SpaceX challenged via IPR2015-01765 at the PTAB.
# The PTAB denied institution. This family illustrates competitive IP dynamics
# between the two leading reusable launch vehicle companies.

BLUE_ORIGIN_VTOL_FAMILY = [
    {
        "node_id": "BO-VL-001",
        "pub_number": "US8678321B2",
        "title": "Sea and land takeoff and landing capability for vertical takeoff and landing vehicle",
        "filing_type": "Priority Application",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2011-02-15",
        "filing_year": 2011,
        "grant_date": "2014-03-25",
        "cpc_codes": "B64G1/62|B64C29/00|B64G1/26",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "A vertical takeoff and landing vehicle configured for operation from sea-based "
            "and land-based platforms, incorporating powered descent guidance and propulsive "
            "landing on floating or fixed surfaces. Claims cover the concept of reusable "
            "booster landing on unimproved or mobile surfaces."
        ),
        "parent_id": None,
        "relationship": None,
        "claims_count": 26,
        "inventors": "Dumbacher, Stephen; Malone, Thomas",
        "family_id": "FAM-BO-VTOL-001",
    },
    {
        "node_id": "BO-VL-002",
        "pub_number": "WO2012112309A1",
        "title": "VTOL vehicle sea and land takeoff and landing capability (PCT)",
        "filing_type": "PCT Application",
        "status": "pending",
        "jurisdiction": "WO",
        "filing_date": "2012-02-14",
        "filing_year": 2012,
        "grant_date": None,
        "cpc_codes": "B64G1/62|B64C29/00",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "International PCT application claiming priority to US13/027948, directed to "
            "the core VTOL landing concept across multiple jurisdictions."
        ),
        "parent_id": "BO-VL-001",
        "relationship": "PCT",
        "claims_count": 22,
        "inventors": "Dumbacher, Stephen; Malone, Thomas",
        "family_id": "FAM-BO-VTOL-001",
    },
    {
        "node_id": "BO-VL-003",
        "pub_number": "EP2675709A1",
        "title": "VTOL vehicle sea and land landing capability (EP)",
        "filing_type": "EP National Phase",
        "status": "pending",
        "jurisdiction": "EP",
        "filing_date": "2013-09-24",
        "filing_year": 2013,
        "grant_date": None,
        "cpc_codes": "B64G1/62|B64C29/00",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "European national phase entry from WO2012112309, pending examination at the "
            "European Patent Office."
        ),
        "parent_id": "BO-VL-002",
        "relationship": "EP National Phase",
        "claims_count": 18,
        "inventors": "Dumbacher, Stephen; Malone, Thomas",
        "family_id": "FAM-BO-VTOL-001",
    },
    {
        "node_id": "BO-VL-004",
        "pub_number": "CA2827055A1",
        "title": "VTOL vehicle sea and land landing capability (CA)",
        "filing_type": "CA National Phase",
        "status": "pending",
        "jurisdiction": "CA",
        "filing_date": "2013-08-14",
        "filing_year": 2013,
        "grant_date": None,
        "cpc_codes": "B64G1/62|B64C29/00",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "Canada national phase entry from WO2012112309, pending examination at CIPO."
        ),
        "parent_id": "BO-VL-002",
        "relationship": "CA National Phase",
        "claims_count": 18,
        "inventors": "Dumbacher, Stephen; Malone, Thomas",
        "family_id": "FAM-BO-VTOL-001",
    },
    {
        "node_id": "BO-VL-005",
        "pub_number": "US9108714B2",
        "title": "Reusable suborbital launch vehicle with sea-based landing capability",
        "filing_type": "Continuation",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2014-03-04",
        "filing_year": 2014,
        "grant_date": "2015-08-18",
        "cpc_codes": "B64G1/62|B64C29/00|B64G5/00",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "A continuation of US8678321, directed to suborbital vehicles specifically "
            "configured for soft landing on sea-based platforms with active stabilization."
        ),
        "parent_id": "BO-VL-001",
        "relationship": "Continuation",
        "claims_count": 20,
        "inventors": "Dumbacher, Stephen; Malone, Thomas; Kent, Robert",
        "family_id": "FAM-BO-VTOL-001",
    },
    {
        "node_id": "BO-VL-006",
        "pub_number": "IPR2015-01765",
        "title": "SpaceX IPR petition — challenging US8678321B2 reusable landing claims",
        "filing_type": "IPR Challenge",
        "status": "denied",
        "jurisdiction": "USPTO/PTAB",
        "filing_date": "2015-07-17",
        "filing_year": 2015,
        "grant_date": None,
        "cpc_codes": "",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "Inter partes review petition filed by Space Exploration Technologies Corp at "
            "the Patent Trial and Appeal Board, asserting that Blue Origin's US8678321 claims "
            "were anticipated by prior art. The PTAB denied institution in April 2016, finding "
            "SpaceX had not shown a reasonable likelihood of prevailing on the asserted grounds."
        ),
        "parent_id": "BO-VL-001",
        "relationship": "IPR Challenge",
        "claims_count": 0,
        "inventors": "Petitioner: Space Exploration Technologies Corp",
        "family_id": "FAM-BO-VTOL-001",
    },
    {
        "node_id": "BO-VL-007",
        "pub_number": "US9758240B2",
        "title": "Reusable launch vehicle with variable-thrust propulsive landing system",
        "filing_type": "Continuation",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2016-01-12",
        "filing_year": 2016,
        "grant_date": "2017-09-12",
        "cpc_codes": "B64G1/62|F02K9/58|B64C29/00",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "A continuation of US9108714, adding claims directed to throttle control systems "
            "enabling precise velocity management during powered descent for reusable boosters."
        ),
        "parent_id": "BO-VL-005",
        "relationship": "Continuation",
        "claims_count": 17,
        "inventors": "Malone, Thomas; Kent, Robert",
        "family_id": "FAM-BO-VTOL-001",
    },
]


def get_all_families() -> dict:
    """Return all curated patent families as {display_label: records_list}."""
    return {
        "SpaceX  |  Starlink Phased-Array Antenna  (US10236574B2)": STARLINK_ANTENNA_FAMILY,
        "Blue Origin  |  VTOL Reusable Landing  (US8678321B2 + IPR2015-01765)": BLUE_ORIGIN_VTOL_FAMILY,
    }


if __name__ == "__main__":
    df = get_sample_data()
    import os
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/all_patents_sample.csv", index=False)
    print(f"Sample: {len(df)} rows")
    print(df.groupby("company")["lens_id"].count())
