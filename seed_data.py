"""
Seed / sample patent dataset for the NewSpace dashboard.
Based on publicly documented patent portfolios (as of 2025).
Used when real API data has not yet been fetched.

Includes seven curated patent families with realistic prosecution
histories for the family tree panel.
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
    ("Flat-panel satellite with integrated ion propulsion and stowable solar arrays", "B64G1/28", "Spacecraft / Launch Systems"),
    ("Satellite constellation frequency reuse via spot beam coordination", "H04W16/14", "Satellite / Wireless Comms"),
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

MAXAR_TITLES = [
    ("High-resolution electro-optical imaging satellite bus", "B64G1/10", "Spacecraft / Launch Systems"),
    ("Synthetic aperture radar for Earth observation from LEO", "G01S13/90", "Remote Sensing / GPS"),
    ("GEO satellite bus with electric propulsion station keeping", "B64G1/40", "Spacecraft / Launch Systems"),
    ("Satellite image tasking and scheduling optimization algorithm", "G06Q10/06", "Computing / Software"),
    ("On-orbit image compression and downlink management system", "H04N19/00", "Satellite / Wireless Comms"),
    ("Geospatial data fusion from multi-source satellite imagery", "G01C11/00", "Remote Sensing / GPS"),
    ("High-throughput Ka-band satellite communications payload", "H04B7/185", "Satellite / Wireless Comms"),
    ("Deployable large aperture reflector antenna for GEO satellites", "H01Q15/14", "Antenna Design"),
    ("Satellite imaging scheduling for time-critical reconnaissance", "G06Q10/04", "Computing / Software"),
    ("Multi-spectral imaging payload for land cover classification", "G01S17/88", "Remote Sensing / GPS"),
    ("Satellite-derived change detection using convolutional neural networks", "G06V20/10", "Computing / Software"),
    ("Spacecraft thermal radiator panel deployment mechanism", "B64G1/50", "Spacecraft / Launch Systems"),
    ("High-power solar array for GEO communications satellite", "H02S10/40", "Power / Electrical Systems"),
    ("Satellite attitude estimation with star tracker sensor fusion", "B64G1/36", "Spacecraft / Launch Systems"),
    ("Precision pointing system for high-resolution optical telescope payload", "G01C21/24", "Remote Sensing / GPS"),
]

PLANET_LABS_TITLES = [
    ("CubeSat imaging payload with push-broom sensor architecture", "G01S17/88", "Remote Sensing / GPS"),
    ("Daily revisit Earth imaging constellation scheduling algorithm", "B64G1/10", "Spacecraft / Launch Systems"),
    ("Ground station downlink prioritization for high-cadence imaging", "H04B7/185", "Satellite / Wireless Comms"),
    ("Low-cost satellite attitude control using magnetorquers", "B64G1/36", "Spacecraft / Launch Systems"),
    ("Automated image quality assessment pipeline for satellite imagery", "G06T7/00", "Computing / Software"),
    ("CubeSat form factor imager with precision focus mechanism", "G01C11/00", "Remote Sensing / GPS"),
    ("Satellite imagery analytics platform for agricultural monitoring", "G06V20/10", "Computing / Software"),
    ("Miniaturized reaction wheel assembly for nanosatellite pointing", "B64G1/28", "Spacecraft / Launch Systems"),
    ("Cloud mask generation for multispectral satellite image time series", "G06V10/25", "Computing / Software"),
    ("Rapid manufacturing process for high-volume small satellite production", "B64G1/00", "Spacecraft / Launch Systems"),
]

RELATIVITY_SPACE_TITLES = [
    ("Additive manufactured rocket engine combustion chamber", "F02K9/10", "Rocket Propulsion"),
    ("Large-scale metal 3D printing system for aerospace structures", "B22F10/00", "Manufacturing"),
    ("Bimetallic additive manufactured rocket nozzle with internal cooling channels", "F02K9/00", "Rocket Propulsion"),
    ("Autonomous robotic assembly of additive manufactured rocket components", "B25J11/00", "Manufacturing"),
    ("Printed propellant tank for launch vehicle constructed via direct energy deposition", "B64G1/40", "Spacecraft / Launch Systems"),
    ("Machine learning process control for rocket engine additive manufacturing", "G05B19/418", "Computing / Software"),
    ("Multi-material additive manufactured thrust structure for small launch vehicles", "B64C1/00", "Aeronautics / Structures"),
    ("Software-defined manufacturing workflow for iterative rocket development", "G05B19/00", "Computing / Software"),
]

ASTRA_SPACE_TITLES = [
    ("Autogenous pressurization system for small launch vehicle propellant tanks", "F02K9/44", "Rocket Propulsion"),
    ("Avionics architecture for automated small launch vehicle operations", "B64G1/24", "Spacecraft / Launch Systems"),
    ("Mobile launch platform and vehicle integration for responsive launch", "B64G5/00", "Spacecraft / Launch Systems"),
    ("Propellant cross-feed system for small two-stage launch vehicles", "F02K9/00", "Rocket Propulsion"),
    ("Compact attitude control module for small launch vehicles", "B64G1/26", "Spacecraft / Launch Systems"),
    ("Rapid manufacturing and assembly process for low-cost launch vehicles", "B64G1/00", "Spacecraft / Launch Systems"),
    ("Trajectory optimization for small launch vehicle to multiple orbits", "B64G1/10", "Spacecraft / Launch Systems"),
]

SIERRA_SPACE_TITLES = [
    ("Lifting body reentry vehicle thermal protection system", "B64G1/58", "Spacecraft / Launch Systems"),
    ("Cargo integration and deployment system for Dream Chaser orbital vehicle", "B64G1/64", "Spacecraft / Launch Systems"),
    ("Inflatable space habitat module pressure vessel and hatch assembly", "B64G1/12", "Spacecraft / Launch Systems"),
    ("Reusable orbital vehicle landing gear and airframe structure", "B64C25/00", "Aeronautics / Structures"),
    ("Orbital maneuvering system propulsion for reusable spaceplane", "B64G1/40", "Spacecraft / Launch Systems"),
    ("Atmospheric reentry guidance navigation and control for lifting body", "B64G1/24", "Spacecraft / Launch Systems"),
    ("Life support and environmental control for commercial space station module", "B64G1/58", "Spacecraft / Launch Systems"),
    ("Flexible solar array deployment mechanism for orbital platforms", "B64G1/44", "Spacecraft / Launch Systems"),
    ("Docking interface and capture mechanism for commercial cargo vehicle", "B64G1/64", "Spacecraft / Launch Systems"),
]


# ── Curated patent family 1: SpaceX Starlink phased-array antenna ─────────────

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
            "beams with low-latency pointing for broadband user terminals."
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
        "title": "Phased array antenna for satellite communication (PCT)",
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


# ── Curated patent family 2: SpaceX Starlink satellite bus ────────────────────

STARLINK_SAT_BUS_FAMILY = [
    {
        "node_id": "SX-SB-001",
        "pub_number": "US10800551B2",
        "title": "Flat-panel satellite with stowable solar arrays and integrated ion thruster",
        "filing_type": "Priority Application",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2016-09-15",
        "filing_year": 2016,
        "grant_date": "2020-10-13",
        "cpc_codes": "B64G1/28|B64G1/40|H02S10/40",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "A flat-panel satellite design enabling high-density stacking within a launch vehicle "
            "fairing, with stowable solar arrays that deploy on orbit and an integrated Krypton "
            "ion propulsion system for station keeping and deorbit."
        ),
        "parent_id": None,
        "relationship": None,
        "claims_count": 32,
        "inventors": "Riggs, Brian; Meneghetti, Luca; Sharma, Priya",
        "family_id": "FAM-SX-SB-001",
    },
    {
        "node_id": "SX-SB-002",
        "pub_number": "WO2018022254A1",
        "title": "Flat-panel satellite bus design (PCT)",
        "filing_type": "PCT Application",
        "status": "pending",
        "jurisdiction": "WO",
        "filing_date": "2017-08-01",
        "filing_year": 2017,
        "grant_date": None,
        "cpc_codes": "B64G1/28|B64G1/40",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "International patent application for the Starlink satellite bus architecture, "
            "claiming priority to US15/267389 and covering the flat-panel form factor and "
            "stacked launch configuration."
        ),
        "parent_id": "SX-SB-001",
        "relationship": "PCT",
        "claims_count": 26,
        "inventors": "Riggs, Brian; Meneghetti, Luca; Sharma, Priya",
        "family_id": "FAM-SX-SB-001",
    },
    {
        "node_id": "SX-SB-003",
        "pub_number": "US11286062B2",
        "title": "Satellite deployment mechanism for high-density stacked launch configuration",
        "filing_type": "Continuation",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2018-11-20",
        "filing_year": 2018,
        "grant_date": "2022-03-29",
        "cpc_codes": "B64G1/64|B64G1/28|B64G1/10",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "A continuation of US10800551 directed to claims covering the deployment sequencing "
            "mechanism that releases individual satellites from a stacked launch configuration "
            "without contact between adjacent spacecraft."
        ),
        "parent_id": "SX-SB-001",
        "relationship": "Continuation",
        "claims_count": 20,
        "inventors": "Riggs, Brian; Chen, Wei; Patel, Anika",
        "family_id": "FAM-SX-SB-001",
    },
    {
        "node_id": "SX-SB-004",
        "pub_number": "EP3490902B1",
        "title": "Flat-panel satellite bus with ion propulsion (EP)",
        "filing_type": "EP National Phase",
        "status": "granted",
        "jurisdiction": "EP",
        "filing_date": "2019-01-18",
        "filing_year": 2019,
        "grant_date": "2022-04-27",
        "cpc_codes": "B64G1/28|B64G1/40",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "European national phase entry of WO2018022254, covering the flat-panel satellite "
            "architecture with integrated propulsion for large LEO constellations."
        ),
        "parent_id": "SX-SB-002",
        "relationship": "EP National Phase",
        "claims_count": 18,
        "inventors": "Riggs, Brian; Meneghetti, Luca; Sharma, Priya",
        "family_id": "FAM-SX-SB-001",
    },
    {
        "node_id": "SX-SB-005",
        "pub_number": "JP7008011B2",
        "title": "Flat-panel satellite bus with stowable solar array (JP)",
        "filing_type": "JP National Phase",
        "status": "granted",
        "jurisdiction": "JP",
        "filing_date": "2019-01-18",
        "filing_year": 2019,
        "grant_date": "2022-01-14",
        "cpc_codes": "B64G1/28|B64G1/44",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "Japan national phase entry of WO2018022254 covering stowable solar array "
            "deployment methods for flat-panel satellite configurations."
        ),
        "parent_id": "SX-SB-002",
        "relationship": "JP National Phase",
        "claims_count": 14,
        "inventors": "Riggs, Brian; Meneghetti, Luca",
        "family_id": "FAM-SX-SB-001",
    },
    {
        "node_id": "SX-SB-006",
        "pub_number": "US11027867B2",
        "title": "Ion propulsion station keeping and deorbit method for LEO satellite",
        "filing_type": "Divisional",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2019-06-04",
        "filing_year": 2019,
        "grant_date": "2021-06-08",
        "cpc_codes": "B64G1/40|B64G1/26",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "A divisional of US10800551 directed specifically to method claims for using "
            "Krypton ion propulsion to maintain orbital altitude and perform controlled "
            "atmospheric deorbit within regulatory timelines."
        ),
        "parent_id": "SX-SB-001",
        "relationship": "Divisional",
        "claims_count": 16,
        "inventors": "Meneghetti, Luca; Sharma, Priya",
        "family_id": "FAM-SX-SB-001",
    },
]


# ── Curated patent family 3: SpaceX inter-satellite optical link ───────────────

STARLINK_ISL_FAMILY = [
    {
        "node_id": "SX-ISL-001",
        "pub_number": "US11502751B2",
        "title": "Free-space optical terminal for inter-satellite links in LEO constellations",
        "filing_type": "Priority Application",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2018-04-23",
        "filing_year": 2018,
        "grant_date": "2022-11-15",
        "cpc_codes": "H04B10/112|H04B10/11|H01Q1/12",
        "tech_category": "Satellite / Wireless Comms",
        "abstract": (
            "A free-space optical communication terminal for establishing inter-satellite links "
            "between LEO spacecraft, enabling a mesh network without ground-station relay hops "
            "and reducing end-to-end latency for transoceanic traffic."
        ),
        "parent_id": None,
        "relationship": None,
        "claims_count": 30,
        "inventors": "Ellis, Rachel; Park, Jin-Ho; Bergmann, Felix",
        "family_id": "FAM-SX-ISL-001",
    },
    {
        "node_id": "SX-ISL-002",
        "pub_number": "WO2019209799A1",
        "title": "Inter-satellite optical link terminal (PCT)",
        "filing_type": "PCT Application",
        "status": "pending",
        "jurisdiction": "WO",
        "filing_date": "2019-04-22",
        "filing_year": 2019,
        "grant_date": None,
        "cpc_codes": "H04B10/112|H04B10/11",
        "tech_category": "Satellite / Wireless Comms",
        "abstract": (
            "International filing claiming priority to US15/960432, covering the optical "
            "terminal design for bidirectional inter-satellite links between Starlink v2 satellites."
        ),
        "parent_id": "SX-ISL-001",
        "relationship": "PCT",
        "claims_count": 24,
        "inventors": "Ellis, Rachel; Park, Jin-Ho; Bergmann, Felix",
        "family_id": "FAM-SX-ISL-001",
    },
    {
        "node_id": "SX-ISL-003",
        "pub_number": "US11770173B2",
        "title": "Beam acquisition and pointing method for inter-satellite optical links",
        "filing_type": "Continuation",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2019-11-12",
        "filing_year": 2019,
        "grant_date": "2023-09-26",
        "cpc_codes": "H04B10/112|G01S17/66|H04B10/118",
        "tech_category": "Satellite / Wireless Comms",
        "abstract": (
            "A continuation of US11502751 directed to the acquisition, pointing, and tracking "
            "protocol enabling rapid link establishment between satellites at orbital closing speeds."
        ),
        "parent_id": "SX-ISL-001",
        "relationship": "Continuation",
        "claims_count": 22,
        "inventors": "Ellis, Rachel; Nguyen, Linh; Park, Jin-Ho",
        "family_id": "FAM-SX-ISL-001",
    },
    {
        "node_id": "SX-ISL-004",
        "pub_number": "EP3785382B1",
        "title": "Free-space optical inter-satellite link terminal (EP)",
        "filing_type": "EP National Phase",
        "status": "granted",
        "jurisdiction": "EP",
        "filing_date": "2020-10-21",
        "filing_year": 2020,
        "grant_date": "2023-05-17",
        "cpc_codes": "H04B10/112|H04B10/11",
        "tech_category": "Satellite / Wireless Comms",
        "abstract": (
            "European national phase entry of WO2019209799, covering the optical terminal "
            "hardware for inter-satellite mesh networking."
        ),
        "parent_id": "SX-ISL-002",
        "relationship": "EP National Phase",
        "claims_count": 16,
        "inventors": "Ellis, Rachel; Park, Jin-Ho; Bergmann, Felix",
        "family_id": "FAM-SX-ISL-001",
    },
    {
        "node_id": "SX-ISL-005",
        "pub_number": "US20230074059A1",
        "title": "Adaptive optics compensation for atmospheric turbulence in near-earth optical links",
        "filing_type": "Continuation-in-Part",
        "status": "pending",
        "jurisdiction": "US",
        "filing_date": "2021-09-08",
        "filing_year": 2021,
        "grant_date": None,
        "cpc_codes": "H04B10/112|G02B26/06|H04B10/118",
        "tech_category": "Satellite / Wireless Comms",
        "abstract": (
            "A continuation-in-part introducing new matter directed to wavefront sensing and "
            "correction techniques for optical links in the lower atmosphere, extending the "
            "technology to ground-to-satellite optical communications."
        ),
        "parent_id": "SX-ISL-001",
        "relationship": "Continuation-in-Part",
        "claims_count": 26,
        "inventors": "Bergmann, Felix; Park, Jin-Ho; Walsh, Emily",
        "family_id": "FAM-SX-ISL-001",
    },
]


# ── Curated patent family 4: SpaceX Falcon 9 grid fin deployment ──────────────

FALCON_GRID_FIN_FAMILY = [
    {
        "node_id": "SX-GF-001",
        "pub_number": "US9665136B2",
        "title": "Deployable grid fin for atmospheric reentry aerodynamic control",
        "filing_type": "Priority Application",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2014-06-20",
        "filing_year": 2014,
        "grant_date": "2017-05-30",
        "cpc_codes": "B64G1/62|B64C3/54|B64C9/00",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "A deployable grid fin system for a returning launch vehicle booster, providing "
            "aerodynamic stabilization and steering authority during hypersonic and subsonic "
            "powered descent to enable precision propulsive landing."
        ),
        "parent_id": None,
        "relationship": None,
        "claims_count": 28,
        "inventors": "Koenigsmann, Hans; Bjelde, Brian; Musk, Elon",
        "family_id": "FAM-SX-GF-001",
    },
    {
        "node_id": "SX-GF-002",
        "pub_number": "WO2015200124A1",
        "title": "Deployable grid fin for reusable launch vehicle (PCT)",
        "filing_type": "PCT Application",
        "status": "pending",
        "jurisdiction": "WO",
        "filing_date": "2015-06-19",
        "filing_year": 2015,
        "grant_date": None,
        "cpc_codes": "B64G1/62|B64C3/54",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "International PCT application claiming priority to US14/311224, covering the "
            "deployable grid fin concept for reusable booster recovery systems globally."
        ),
        "parent_id": "SX-GF-001",
        "relationship": "PCT",
        "claims_count": 22,
        "inventors": "Koenigsmann, Hans; Bjelde, Brian",
        "family_id": "FAM-SX-GF-001",
    },
    {
        "node_id": "SX-GF-003",
        "pub_number": "US10040560B2",
        "title": "Aerodynamic braking trajectory for reusable launch vehicle booster",
        "filing_type": "Continuation",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2016-09-14",
        "filing_year": 2016,
        "grant_date": "2018-08-07",
        "cpc_codes": "B64G1/62|B64G1/24|G05D1/10",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "A continuation of US9665136 directed to method claims for computing and executing "
            "an aerodynamic braking trajectory using deployable grid fins during booster descent."
        ),
        "parent_id": "SX-GF-001",
        "relationship": "Continuation",
        "claims_count": 20,
        "inventors": "Koenigsmann, Hans; Kynard, Branden",
        "family_id": "FAM-SX-GF-001",
    },
    {
        "node_id": "SX-GF-004",
        "pub_number": "EP3160851B1",
        "title": "Deployable grid fin for launch vehicle atmospheric reentry (EP)",
        "filing_type": "EP National Phase",
        "status": "granted",
        "jurisdiction": "EP",
        "filing_date": "2016-12-14",
        "filing_year": 2016,
        "grant_date": "2021-04-07",
        "cpc_codes": "B64G1/62|B64C3/54",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "European national phase entry of WO2015200124, covering grid fin mechanisms "
            "for aerodynamic control of reusable booster vehicles during atmospheric reentry."
        ),
        "parent_id": "SX-GF-002",
        "relationship": "EP National Phase",
        "claims_count": 15,
        "inventors": "Koenigsmann, Hans; Bjelde, Brian",
        "family_id": "FAM-SX-GF-001",
    },
    {
        "node_id": "SX-GF-005",
        "pub_number": "US10654605B2",
        "title": "Electrically actuated grid fin for launch vehicle aerodynamic control",
        "filing_type": "Continuation-in-Part",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2018-05-22",
        "filing_year": 2018,
        "grant_date": "2020-05-19",
        "cpc_codes": "B64C3/54|B64G1/62|H02K7/00",
        "tech_category": "Spacecraft / Launch Systems",
        "abstract": (
            "A continuation-in-part of US9665136 introducing new matter covering electrically "
            "actuated grid fin designs that replace hydraulic actuation, reducing system mass "
            "and complexity in the Falcon 9 Block 5 booster configuration."
        ),
        "parent_id": "SX-GF-001",
        "relationship": "Continuation-in-Part",
        "claims_count": 24,
        "inventors": "Koenigsmann, Hans; Bjelde, Brian; Chen, Wei",
        "family_id": "FAM-SX-GF-001",
    },
]


# ── Curated patent family 5: Blue Origin VTOL reusable landing ────────────────

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
            "landing on floating or fixed surfaces. Claims cover reusable booster landing "
            "on unimproved or mobile surfaces."
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
            "European national phase entry from WO2012112309, pending examination "
            "at the European Patent Office."
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
        "title": "SpaceX IPR petition challenging US8678321B2 reusable landing claims",
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


# ── Curated patent family 6: Blue Origin BE-4 engine ─────────────────────────

BLUE_ORIGIN_BE4_FAMILY = [
    {
        "node_id": "BO-BE4-001",
        "pub_number": "US10378474B2",
        "title": "Full-flow staged combustion cycle rocket engine with oxidizer-rich preburner",
        "filing_type": "Priority Application",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2014-09-10",
        "filing_year": 2014,
        "grant_date": "2019-08-13",
        "cpc_codes": "F02K9/10|F02K9/58|F02K9/00",
        "tech_category": "Rocket Propulsion",
        "abstract": (
            "A full-flow staged combustion cycle rocket engine burning liquid oxygen and "
            "liquefied natural gas, using an oxidizer-rich preburner to drive high-pressure "
            "turbopumps. The BE-4 engine is designed for reuse across multiple flights "
            "and serves as the primary propulsion for the New Glenn orbital launch vehicle."
        ),
        "parent_id": None,
        "relationship": None,
        "claims_count": 34,
        "inventors": "Vilas, Gary; Crocker, Andrew; Guzik, Mark",
        "family_id": "FAM-BO-BE4-001",
    },
    {
        "node_id": "BO-BE4-002",
        "pub_number": "WO2016040126A1",
        "title": "Full-flow staged combustion rocket engine (PCT)",
        "filing_type": "PCT Application",
        "status": "pending",
        "jurisdiction": "WO",
        "filing_date": "2015-09-04",
        "filing_year": 2015,
        "grant_date": None,
        "cpc_codes": "F02K9/10|F02K9/58",
        "tech_category": "Rocket Propulsion",
        "abstract": (
            "International patent application covering the BE-4 full-flow staged combustion "
            "engine architecture, claiming priority to US14/483199."
        ),
        "parent_id": "BO-BE4-001",
        "relationship": "PCT",
        "claims_count": 28,
        "inventors": "Vilas, Gary; Crocker, Andrew; Guzik, Mark",
        "family_id": "FAM-BO-BE4-001",
    },
    {
        "node_id": "BO-BE4-003",
        "pub_number": "US10934965B2",
        "title": "Combustion chamber geometry for full-flow staged combustion engine",
        "filing_type": "Continuation",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2016-10-01",
        "filing_year": 2016,
        "grant_date": "2021-03-02",
        "cpc_codes": "F02K9/10|F02K9/52|F23R3/00",
        "tech_category": "Rocket Propulsion",
        "abstract": (
            "A continuation of US10378474 directed to claims covering specific combustion "
            "chamber geometries that improve mixing efficiency and reduce combustion instability "
            "in high chamber-pressure LOX/LNG engines."
        ),
        "parent_id": "BO-BE4-001",
        "relationship": "Continuation",
        "claims_count": 22,
        "inventors": "Vilas, Gary; Eddlemon, Thomas",
        "family_id": "FAM-BO-BE4-001",
    },
    {
        "node_id": "BO-BE4-004",
        "pub_number": "EP3191696B1",
        "title": "Full-flow staged combustion rocket engine (EP)",
        "filing_type": "EP National Phase",
        "status": "granted",
        "jurisdiction": "EP",
        "filing_date": "2016-08-12",
        "filing_year": 2016,
        "grant_date": "2022-02-16",
        "cpc_codes": "F02K9/10|F02K9/58",
        "tech_category": "Rocket Propulsion",
        "abstract": (
            "European national phase entry of WO2016040126, covering the staged combustion "
            "cycle engine architecture for high-performance, reusable liquid rocket engines."
        ),
        "parent_id": "BO-BE4-002",
        "relationship": "EP National Phase",
        "claims_count": 18,
        "inventors": "Vilas, Gary; Crocker, Andrew; Guzik, Mark",
        "family_id": "FAM-BO-BE4-001",
    },
    {
        "node_id": "BO-BE4-005",
        "pub_number": "US11022071B2",
        "title": "Turbopump assembly for cryogenic staged combustion rocket engine",
        "filing_type": "Divisional",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2018-08-14",
        "filing_year": 2018,
        "grant_date": "2021-06-01",
        "cpc_codes": "F04D25/00|F02K9/58|F02K9/44",
        "tech_category": "Rocket Propulsion",
        "abstract": (
            "A divisional of US10378474 covering the turbopump assembly claims, specifically "
            "directed to the high-speed centrifugal pump rotor and bearing systems that "
            "enable the high chamber pressure of the BE-4 engine."
        ),
        "parent_id": "BO-BE4-001",
        "relationship": "Divisional",
        "claims_count": 18,
        "inventors": "Crocker, Andrew; Guzik, Mark",
        "family_id": "FAM-BO-BE4-001",
    },
]


# ── Curated patent family 7: Rocket Lab Electron electric turbopump ───────────

ROCKET_LAB_TURBOPUMP_FAMILY = [
    {
        "node_id": "RL-TP-001",
        "pub_number": "US10844798B2",
        "title": "Electric motor driven turbopump for bipropellant rocket engine",
        "filing_type": "Priority Application",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2015-11-03",
        "filing_year": 2015,
        "grant_date": "2020-11-24",
        "cpc_codes": "F04D25/00|F02K9/44|H02K7/00",
        "tech_category": "Rocket Propulsion",
        "abstract": (
            "A battery-powered electric motor turbopump system for pumping liquid oxygen and "
            "kerosene propellants in a small rocket engine. The Rutherford engine eliminates "
            "a gas generator cycle preburner, replacing it with a compact BLDC motor and "
            "lithium polymer battery system, significantly simplifying engine design."
        ),
        "parent_id": None,
        "relationship": None,
        "claims_count": 29,
        "inventors": "Beck, Peter; Stickland, Lachlan; Withy, Shaun",
        "family_id": "FAM-RL-TP-001",
    },
    {
        "node_id": "RL-TP-002",
        "pub_number": "NZ727087",
        "title": "Electric turbopump for rocket engine (NZ priority filing)",
        "filing_type": "Priority Application",
        "status": "granted",
        "jurisdiction": "NZ",
        "filing_date": "2014-11-04",
        "filing_year": 2014,
        "grant_date": "2017-08-25",
        "cpc_codes": "F04D25/00|F02K9/44",
        "tech_category": "Rocket Propulsion",
        "abstract": (
            "New Zealand priority filing establishing the earliest priority date for the "
            "electric turbopump technology, granted by the Intellectual Property Office of New Zealand."
        ),
        "parent_id": None,
        "relationship": None,
        "claims_count": 20,
        "inventors": "Beck, Peter; Stickland, Lachlan",
        "family_id": "FAM-RL-TP-001",
    },
    {
        "node_id": "RL-TP-003",
        "pub_number": "WO2016073407A1",
        "title": "Electric turbopump for liquid rocket engine (PCT)",
        "filing_type": "PCT Application",
        "status": "pending",
        "jurisdiction": "WO",
        "filing_date": "2015-11-03",
        "filing_year": 2015,
        "grant_date": None,
        "cpc_codes": "F04D25/00|F02K9/44|H02K7/00",
        "tech_category": "Rocket Propulsion",
        "abstract": (
            "PCT international application claiming priority to NZ727087, covering the "
            "electric motor turbopump concept for use in small and medium-class liquid rocket engines."
        ),
        "parent_id": "RL-TP-002",
        "relationship": "PCT",
        "claims_count": 24,
        "inventors": "Beck, Peter; Stickland, Lachlan; Withy, Shaun",
        "family_id": "FAM-RL-TP-001",
    },
    {
        "node_id": "RL-TP-004",
        "pub_number": "US11306681B2",
        "title": "Pump speed control method for electric turbopump rocket engine",
        "filing_type": "Continuation",
        "status": "granted",
        "jurisdiction": "US",
        "filing_date": "2017-07-25",
        "filing_year": 2017,
        "grant_date": "2022-04-19",
        "cpc_codes": "F04D25/00|F02K9/58|H02P6/00",
        "tech_category": "Rocket Propulsion",
        "abstract": (
            "A continuation of US10844798 directed to method claims for controlling pump "
            "speed and mixture ratio in flight to manage propellant consumption and engine "
            "performance during ascent."
        ),
        "parent_id": "RL-TP-001",
        "relationship": "Continuation",
        "claims_count": 18,
        "inventors": "Beck, Peter; Withy, Shaun",
        "family_id": "FAM-RL-TP-001",
    },
    {
        "node_id": "RL-TP-005",
        "pub_number": "EP3215730B1",
        "title": "Electric motor driven turbopump for bipropellant rocket engine (EP)",
        "filing_type": "EP National Phase",
        "status": "granted",
        "jurisdiction": "EP",
        "filing_date": "2016-04-29",
        "filing_year": 2016,
        "grant_date": "2021-07-14",
        "cpc_codes": "F04D25/00|F02K9/44|H02K7/00",
        "tech_category": "Rocket Propulsion",
        "abstract": (
            "European national phase entry of WO2016073407, covering the electric turbopump "
            "architecture for liquid rocket engines. Granted after examination at the EPO."
        ),
        "parent_id": "RL-TP-003",
        "relationship": "EP National Phase",
        "claims_count": 16,
        "inventors": "Beck, Peter; Stickland, Lachlan; Withy, Shaun",
        "family_id": "FAM-RL-TP-001",
    },
]


# ── Helper to build general patent rows ──────────────────────────────────────

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
            "filing_type": None,
            "parent_id": None,
            "relationship": None,
            "claims_count": int(rng.integers(8, 30)),
            "inventors": "",
        })
    return rows


def _family_to_rows(family: list, company: str, assignee: str) -> list:
    """Convert a curated family list to the full DataFrame schema."""
    rows = []
    for rec in family:
        rows.append({
            "company": company,
            "lens_id": rec["node_id"],
            "pub_number": rec["pub_number"],
            "title": rec["title"],
            "abstract": rec["abstract"],
            "pub_type": "granted_patent" if rec["status"] == "granted" else "patent_application",
            "status": rec["status"],
            "assignee": assignee,
            "jurisdiction": rec["jurisdiction"],
            "filing_date": rec["filing_date"],
            "filing_year": rec["filing_year"],
            "pub_date": rec.get("grant_date") or "",
            "pub_year": int(rec["grant_date"][:4]) if rec.get("grant_date") else None,
            "cpc_codes": rec["cpc_codes"],
            "tech_category": rec["tech_category"],
            "inventor_count": len(rec["inventors"].split(";")),
            "family_id": rec["family_id"],
            "family_size": len(family),
            "filing_type": rec["filing_type"],
            "parent_id": rec["parent_id"],
            "relationship": rec["relationship"],
            "claims_count": rec["claims_count"],
            "inventors": rec["inventors"],
        })
    return rows


def get_sample_data() -> pd.DataFrame:
    """Return a realistic sample dataset covering nine NewSpace companies."""
    all_rows = []
    all_rows.extend(_make_patents(SPACEX_TITLES,          "SpaceX",                       (2014, 2025), 0.65))
    all_rows.extend(_make_patents(BLUE_ORIGIN_TITLES,     "Blue Origin",                  (2013, 2025), 0.70))
    all_rows.extend(_make_patents(ROCKET_LAB_TITLES,      "Rocket Lab",                   (2016, 2025), 0.55))
    all_rows.extend(_make_patents(VIRGIN_GALACTIC_TITLES, "Virgin Galactic",              (2010, 2025), 0.60))
    all_rows.extend(_make_patents(MAXAR_TITLES,           "Maxar Technologies",           (2005, 2025), 0.72))
    all_rows.extend(_make_patents(PLANET_LABS_TITLES,     "Planet Labs",                  (2012, 2025), 0.55))
    all_rows.extend(_make_patents(RELATIVITY_SPACE_TITLES,"Relativity Space",             (2016, 2025), 0.50))
    all_rows.extend(_make_patents(ASTRA_SPACE_TITLES,     "Astra Space",                  (2016, 2025), 0.45))
    all_rows.extend(_make_patents(SIERRA_SPACE_TITLES,    "Sierra Nevada / Sierra Space", (2008, 2025), 0.65))

    df = pd.DataFrame(all_rows)

    # Replace generic seed rows for the first family group of each company with
    # the curated prosecution histories, which have rich, realistic data.
    curated_rows = []
    curated_rows.extend(_family_to_rows(STARLINK_ANTENNA_FAMILY, "SpaceX",      "Space Exploration Technologies Corp"))
    curated_rows.extend(_family_to_rows(STARLINK_SAT_BUS_FAMILY, "SpaceX",      "Space Exploration Technologies Corp"))
    curated_rows.extend(_family_to_rows(STARLINK_ISL_FAMILY,     "SpaceX",      "Space Exploration Technologies Corp"))
    curated_rows.extend(_family_to_rows(FALCON_GRID_FIN_FAMILY,  "SpaceX",      "Space Exploration Technologies Corp"))
    curated_rows.extend(_family_to_rows(BLUE_ORIGIN_VTOL_FAMILY, "Blue Origin", "Blue Origin LLC"))
    curated_rows.extend(_family_to_rows(BLUE_ORIGIN_BE4_FAMILY,  "Blue Origin", "Blue Origin LLC"))
    curated_rows.extend(_family_to_rows(ROCKET_LAB_TURBOPUMP_FAMILY, "Rocket Lab", "Rocket Lab USA Inc"))
    df_curated = pd.DataFrame(curated_rows)

    # Remove the first seed family for SpaceX, Blue Origin, Rocket Lab (FAM-SPA-0000, etc.)
    drop_families = {"FAM-SPA-0000", "FAM-BLU-0000", "FAM-ROC-0000"}
    df = df[~df["family_id"].isin(drop_families)]
    df = pd.concat([df, df_curated], ignore_index=True)
    return df


def get_antenna_family() -> list[dict]:
    return STARLINK_ANTENNA_FAMILY


def get_all_families() -> dict:
    """Return all curated patent families as {display_label: records_list}."""
    return {
        "SpaceX  |  Starlink Phased-Array Antenna  (US10236574B2)": STARLINK_ANTENNA_FAMILY,
        "SpaceX  |  Starlink Satellite Bus  (US10800551B2)": STARLINK_SAT_BUS_FAMILY,
        "SpaceX  |  Inter-Satellite Optical Link  (US11502751B2)": STARLINK_ISL_FAMILY,
        "SpaceX  |  Falcon 9 Grid Fin Deployment  (US9665136B2)": FALCON_GRID_FIN_FAMILY,
        "Blue Origin  |  VTOL Reusable Landing  (US8678321B2 + IPR2015-01765)": BLUE_ORIGIN_VTOL_FAMILY,
        "Blue Origin  |  BE-4 Staged Combustion Engine  (US10378474B2)": BLUE_ORIGIN_BE4_FAMILY,
        "Rocket Lab  |  Electron Electric Turbopump  (US10844798B2)": ROCKET_LAB_TURBOPUMP_FAMILY,
    }


if __name__ == "__main__":
    df = get_sample_data()
    import os
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/all_patents_sample.csv", index=False)
    print(f"Sample dataset: {len(df)} rows")
    print(df.groupby("company")["lens_id"].count().sort_values(ascending=False))
    print("\nFamilies available:", list(get_all_families().keys()))
