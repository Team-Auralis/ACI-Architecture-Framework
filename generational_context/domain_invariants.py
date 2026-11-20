"""
Domain Invariant Specifications and Gen-0 Distillation Filters
Empowering 15 Real-World Breakthroughs via Bounded-Context Tree Search (Gen-FUTS)
"""

from __future__ import annotations

import dataclasses
import math
import re
from typing import Any, Dict, List, Optional, Tuple

from .tree_search import DistilledExecutionSignature, ExecutionResult, Problem


@dataclasses.dataclass(frozen=True)
class DomainBreakthroughSpec:
    """Formal specification for a real-world scientific or industrial breakthrough."""
    domain_id: str
    name: str
    sector: str
    real_world_stake: str
    invariants: Dict[str, str]
    metric_name: str
    maximize: bool
    distillation_regexes: List[Tuple[str, str]]


# ==============================================================================
# CATALOG OF 15 REAL-WORLD BREAKTHROUGH SPECIFICATIONS
# ==============================================================================

BREAKTHROUGH_CATALOG: Dict[str, DomainBreakthroughSpec] = {
    # 1. BIOPHARMA: De Novo Drug Discovery
    "BT-01": DomainBreakthroughSpec(
        domain_id="BT-01",
        name="Stereochemical Invariant Molecular Conformation & Docking",
        sector="Biomedical & Pharmaceutical Engineering",
        real_world_stake="Eliminates toxic, unphysical, or non-synthesizable drug candidates during automated ligand discovery, saving years of wet-lab validation cycles.",
        invariants={
            "lipinski_rule_of_five": "Molecular weight <= 500 Da, LogP <= 5, H-bond donors <= 5, H-bond acceptors <= 10.",
            "valence_geometry": "Valence bond angles and formal atomic charges must not violate hybridization constraints.",
            "chirality_stability": "Absolute stereocenters (R/S designation) must remain invariant across docking sweeps.",
        },
        metric_name="binding_affinity_kcal_mol",
        maximize=False,  # Lower free energy (more negative) is better
        distillation_regexes=[
            (r"VinaAffinity:\s*(-?\d+\.\d+)", "VinaAffinity"),
            (r"ValenceViolation:\s*([^\n\r]+)", "ValenceViolation"),
            (r"StereoCenterClash:\s*([^\n\r]+)", "StereoCenterClash"),
        ],
    ),

    # 2. CLEAN ENERGY: Fusion Plasma Magnetic Confinement
    "BT-02": DomainBreakthroughSpec(
        domain_id="BT-02",
        name="Divergence-Free Tokamak Plasma Equilibrium Synthesis",
        sector="Nuclear Fusion & Clean Power",
        real_world_stake="Prevents catastrophic plasma disruptions and thermal quench against the tokamak first wall in ITER/SPARC by enforcing exact magnetohydrodynamic (MHD) equilibrium.",
        invariants={
            "magnetic_divergence": "Magnetic field must remain strictly divergence-free: ||div(B)||_inf <= 1e-12.",
            "grad_shafranov": "Plasma boundary must satisfy Delta* psi = -mu_0 * R^2 * p'(psi) - F * F'(psi).",
            "q_profile_safety": "Safety factor q(r) > 1.0 everywhere to prevent m=1 kink instabilities.",
        },
        metric_name="mhd_stability_margin",
        maximize=True,
        distillation_regexes=[
            (r"DivBError:\s*([0-9\.e\-\+]+)", "DivBError"),
            (r"BetaPoloidal:\s*([0-9\.]+)", "BetaPoloidal"),
            (r"KinkInstability:\s*([^\n\r]+)", "KinkInstability"),
        ],
    ),

    # 3. POWER GRID: High-Voltage Grid Frequency & Voltage Collapse
    "BT-03": DomainBreakthroughSpec(
        domain_id="BT-03",
        name="SCADA Bounded Contingency Dispatch & Frequency Stabilization",
        sector="National Critical Electrical Infrastructure",
        real_world_stake="Prevents regional blackout cascades during extreme weather by filtering SCADA alarm chattering and maintaining generator inertial frequency bounds.",
        invariants={
            "frequency_nadir": "System frequency must remain strictly within [59.8 Hz, 60.2 Hz] (nominal 60Hz).",
            "transformer_mva_thermal": "Transmission line loading must not exceed 100% continuous MVA thermal rating.",
            "voltage_stability_margin": "Bus voltage must satisfy 0.95 p.u. <= V <= 1.05 p.u. under N-1 contingency.",
        },
        metric_name="contingency_reserve_margin_mw",
        maximize=True,
        distillation_regexes=[
            (r"FrequencyTrip:\s*([0-9\.]+)\s*Hz", "FrequencyTrip"),
            (r"ThermalOverload:\s*([^\n\r]+)", "ThermalOverload"),
            (r"VoltageCollapse:\s*([^\n\r]+)", "VoltageCollapse"),
        ],
    ),

    # 4. AEROSPACE: Mega-Constellation Autonomous Station-Keeping
    "BT-04": DomainBreakthroughSpec(
        domain_id="BT-04",
        name="Debris-Evasive Autonomous Satellite Station-Keeping",
        sector="Orbital Defense & Space Operations",
        real_world_stake="Averts Kessler syndrome collisions in congested LEO orbits (e.g. 10,000+ satellites) under communication latency while minimizing station-keeping propellant burn.",
        invariants={
            "collision_probability": "Maximum conjunction collision probability Pc < 1e-7 across 72-hour screening window.",
            "orbital_angular_momentum": "Continuous maneuvers must preserve orbital angular momentum vector outside active burns.",
            "fuel_reserve_floor": "Station-keeping fuel mass must not drop below 15% end-of-life deorbit reserve.",
        },
        metric_name="station_keeping_delta_v_efficiency",
        maximize=True,
        distillation_regexes=[
            (r"ConjunctionWarning:\s*miss_dist=([0-9\.]+)m", "ConjunctionWarning"),
            (r"DeltaVSpent:\s*([0-9\.]+)m_s", "DeltaVSpent"),
            (r"FuelDepleted:\s*([^\n\r]+)", "FuelDepleted"),
        ],
    ),

    # 5. SEMICONDUCTORS: GPU High-Performance Kernel Synthesis
    "BT-05": DomainBreakthroughSpec(
        domain_id="BT-05",
        name="Bank-Conflict-Free GPU Kernel Optimization (Triton / CUDA)",
        sector="High-Performance AI Compute Hardware",
        real_world_stake="Generates custom GPU memory kernels (FlashAttention, MoE dispatchers) achieving >92% hardware roofline compute without shared-memory bank conflicts or illegal address faults.",
        invariants={
            "warp_synchronization": "No divergent branch divergence or unsynchronized __syncthreads() barriers.",
            "shared_memory_bounds": "Dynamic shared memory allocation must not exceed 99 KB per Streaming Multiprocessor.",
            "numerical_equivalence": "Max absolute tensor discrepancy ||Y_kernel - Y_ref||_inf <= 1e-5.",
        },
        metric_name="tensor_tflops_throughput",
        maximize=True,
        distillation_regexes=[
            (r"CUDA_EXCEPTION:\s*([^\n\r]+)", "CudaException"),
            (r"BankConflictRatio:\s*([0-9\.]+)", "BankConflictRatio"),
            (r"SharedMemExceeded:\s*([^\n\r]+)", "SharedMemExceeded"),
        ],
    ),

    # 6. EARTH SCIENCES: Enthalpy-Conserving Atmospheric Parameterization
    "BT-06": DomainBreakthroughSpec(
        domain_id="BT-06",
        name="Mass-Enthalpy Conserving Global Climate Model Parameterizer",
        sector="Atmospheric Physics & Climate Forecasting",
        real_world_stake="Eliminates non-physical energy and moisture drifts in 100-year global circulation models (GCMs), providing accurate sea-level and hurricane forecasting.",
        invariants={
            "total_water_conservation": "Column-integrated atmospheric moisture drift dW/dt - (E - P) <= 1e-9 kg/(m^2 s).",
            "first_law_enthalpy": "Global moist static energy (MSE) must be conserved: |dMSE/dt - F_net| <= 1e-4 W/m^2.",
            "positivity_moisture": "Specific humidity q_v(x, y, z, t) >= 0 everywhere.",
        },
        metric_name="decadal_rmse_climate_variance",
        maximize=False,
        distillation_regexes=[
            (r"EnergyDrift:\s*([0-9\.e\-\+]+)\s*W_m2", "EnergyDrift"),
            (r"NegativeMoisture:\s*([^\n\r]+)", "NegativeMoisture"),
            (r"CFLViolation:\s*([^\n\r]+)", "CFLViolation"),
        ],
    ),

    # 7. CYBERSECURITY: Memory-Safe Autonomous Zero-Day Patching
    "BT-07": DomainBreakthroughSpec(
        domain_id="BT-07",
        name="Sanitizer-Bounded Automated Binary Exploit Remediation",
        sector="Cyber Defense & National Vulnerability Mitigation",
        real_world_stake="Synthesizes provably sound patches for memory corruption vulnerabilities (CWE-416 Use-After-Free, CWE-122 Heap Overflow) without breaking API contracts or degrading throughput.",
        invariants={
            "asan_cleanliness": "Must execute test suite with 0 AddressSanitizer / UndefinedBehaviorSanitizer violations.",
            "abi_contract_invariance": "Exported function symbols, calling conventions, and struct layouts must remain identical.",
            "zero_functional_regression": "100% pass rate on pre-existing unit test suites.",
        },
        metric_name="exploit_mitigation_index",
        maximize=True,
        distillation_regexes=[
            (r"ASanCrash:\s*([A-Za-z0-9_\-]+)\s*on\s*address\s*(0x[0-9a-fA-F]+)", "ASanCrash"),
            (r"UndefinedBehavior:\s*([^\n\r]+)", "UndefinedBehavior"),
            (r"RegressionFail:\s*([^\n\r]+)", "RegressionFail"),
        ],
    ),

    # 8. GENOMICS: Single-Cell Batch Correction Manifold Preservation
    "BT-08": DomainBreakthroughSpec(
        domain_id="BT-08",
        name="Biological Manifold-Preserving scRNA-seq Batch Integrator",
        sector="Precision Oncology & Single-Cell Genomics",
        real_world_stake="Integrates multi-patient single-cell tumor atlases across heterogeneous sequencers without erasing rare malignant clone clusters or distorting gene correlations.",
        invariants={
            "marker_gene_conservation": "Key cell-type canonical marker genes must retain positive differential expression.",
            "cell_type_separability": "Adjusted Rand Index (ARI) on biological cell types must satisfy >= 0.82.",
            "non_negative_expression": "Denoised expression values must satisfy Y_ij >= 0.0.",
        },
        metric_name="batch_entropy_integration_score",
        maximize=True,
        distillation_regexes=[
            (r"BatchMixing:\s*([0-9\.]+)", "BatchMixing"),
            (r"MarkerLost:\s*([^\n\r]+)", "MarkerLost"),
            (r"ManifoldDistortion:\s*([0-9\.]+)", "ManifoldDistortion"),
        ],
    ),

    # 9. QUANTITATIVE FINANCE: Bounded-Context Market Liquidity & VaR
    "BT-09": DomainBreakthroughSpec(
        domain_id="BT-09",
        name="Regulatory Capital & Delta-Neutral Algorithmic Market Maker",
        sector="FinTech & Systemic Financial Stability",
        real_world_stake="Maintains continuous exchange liquidity during flash crashes while strictly preventing margin calls, regulatory capital breaches, and runaway naked exposures.",
        invariants={
            "var_capital_bound": "99.9% 1-day Value-at-Risk must not exceed 2.5% of total dedicated equity capital.",
            "delta_neutrality_envelope": "Portfolio net portfolio Delta must satisfy |Delta_net| <= 0.05 * total_assets.",
            "maximum_order_rate": "Order replacement rate must not exceed exchange anti-quote-stuffing limits (1,000 req/sec).",
        },
        metric_name="sharpe_liquidity_ratio",
        maximize=True,
        distillation_regexes=[
            (r"VaRBreach:\s*loss=([0-9\.]+)", "VaRBreach"),
            (r"DeltaLimitExceeded:\s*delta=([0-9\.\-]+)", "DeltaLimitExceeded"),
            (r"ExchangeThrottle:\s*([^\n\r]+)", "ExchangeThrottle"),
        ],
    ),

    # 10. MATERIALS SCIENCE: Thermochemical Synthesis Route Synthesis
    "BT-10": DomainBreakthroughSpec(
        domain_id="BT-10",
        name="Stoichiometric Thermochemical Pathway Discovery",
        sector="Advanced Materials & Battery Chemistries",
        real_world_stake="Discovers novel solid-state battery electrolytes (e.g. sulfide-based superionic conductors) while preventing hazardous runaway exothermic intermediates.",
        invariants={
            "gibbs_spontaneity": "Every intermediate reaction step must exhibit negative Gibbs free energy: Delta G_rxn < 0.",
            "mass_stoichiometry": "Atomic conservation of all elements across reactants and products must equal exactly 0.",
            "adiabatic_temperature_rise": "Adiabatic exothermic temperature rise Delta T_ad must not exceed 150 deg C.",
        },
        metric_name="ionic_conductivity_s_cm",
        maximize=True,
        distillation_regexes=[
            (r"EndothermicBlock:\s*DeltaG=([0-9\.\+]+)", "EndothermicBlock"),
            (r"ThermalRunawayRisk:\s*DeltaT=([0-9\.]+)", "ThermalRunawayRisk"),
            (r"MassImbalance:\s*([^\n\r]+)", "MassImbalance"),
        ],
    ),

    # 11. CIVIL DEFENSE: Reservoir Spillway & Flood Inundation Control
    "BT-11": DomainBreakthroughSpec(
        domain_id="BT-11",
        name="Hydrologic Continuity Bounded Dam Spillway Dispatcher",
        sector="Water Resources & Disaster Prevention",
        real_world_stake="Averts catastrophic dam overtopping and downriver city flooding during hurricane cloudbursts by balancing live reservoir storage against spillway structural limits.",
        invariants={
            "continuity_equation": "Reservoir volume derivative dV/dt must equal Qin - Qout at all time steps.",
            "dam_crest_freeboard": "Water surface elevation must maintain >= 1.5 meters below non-overflow dam crest.",
            "downstream_flood_stage": "Total discharge Qout must not exceed downstream levee channel capacity (3,500 m^3/s).",
        },
        metric_name="flood_peak_attenuation_ratio",
        maximize=True,
        distillation_regexes=[
            (r"DamOvertoppingWarning:\s*freeboard=([0-9\.\-]+)m", "OvertoppingWarning"),
            (r"LeveeBreachRisk:\s*Q=([0-9\.]+)m3_s", "LeveeBreachRisk"),
            (r"GateCavitation:\s*([^\n\r]+)", "GateCavitation"),
        ],
    ),

    # 12. HIGH-SPEED RAIL: Moving-Block Signalling & Headway Control
    "BT-12": DomainBreakthroughSpec(
        domain_id="BT-12",
        name="Kinematic Safe-Braking Moving-Block Rail Dispatcher",
        sector="High-Speed Rail & Public Transit",
        real_world_stake="Enables 90-second high-speed train headways at 320 km/h without risking rear-end collisions by guaranteeing instantaneous fail-safe emergency braking curves.",
        invariants={
            "safe_braking_distance": "Headway distance d_head >= d_brake(v) + d_margin(500m) under worst-case rail friction.",
            "jerk_comfort_limit": "Rate of acceleration change (jerk) must remain within [-1.2 m/s^3, +1.2 m/s^3].",
            "switch_divergence_interlock": "Points / track switches must be locked 120s prior to train arrival.",
        },
        metric_name="passengers_per_hour_throughput",
        maximize=True,
        distillation_regexes=[
            (r"HeadwayBreach:\s*dist=([0-9\.]+)m", "HeadwayBreach"),
            (r"JerkExceeded:\s*([0-9\.\-]+)m_s3", "JerkExceeded"),
            (r"InterlockViolation:\s*([^\n\r]+)", "InterlockViolation"),
        ],
    ),

    # 13. SEMICONDUCTOR LITHO: 2nm Photomask Optical Proximity Correction
    "BT-13": DomainBreakthroughSpec(
        domain_id="BT-13",
        name="Curvilinear Inverse Lithography Edge-Placement Optimizer",
        sector="Sub-2nm Semiconductor Fabrication",
        real_world_stake="Compensates for extreme ultraviolet (EUV) optical diffraction on 2nm silicon wafers, preventing bridging defects and broken gate interconnects across billions of transistors.",
        invariants={
            "edge_placement_error": "Maximum Edge Placement Error (EPE) across all critical polygon edges <= 0.8 nm.",
            "mask_rule_cleanliness": "Photomask polygons must satisfy minimum corner rounding radius >= 8.0 nm.",
            "euv_dose_uniformity": "Photomask transmission must not create local thermal hotspots exceeding 18 mJ/cm^2.",
        },
        metric_name="die_yield_predicted_percentage",
        maximize=True,
        distillation_regexes=[
            (r"EPE_Violation:\s*epe=([0-9\.]+)nm", "EPE_Violation"),
            (r"MaskBridging:\s*([^\n\r]+)", "MaskBridging"),
            (r"PinchDefect:\s*([^\n\r]+)", "PinchDefect"),
        ],
    ),

    # 14. SURGICAL ROBOTICS: Tissue-Boundary Invariant Motion Planner
    "BT-14": DomainBreakthroughSpec(
        domain_id="BT-14",
        name="Critical Anatomical Boundary & Shear-Safe Surgical Actuator",
        sector="Robotic Surgery & Medical Devices",
        real_world_stake="Prevents accidental arterial lacerations and tissue tearing during autonomous robotic endoscopic suturing by enforcing strict spatial forbidden zones and force ceilings.",
        invariants={
            "arterial_no_fly_zone": "Surgical end-effector tip must maintain >= 3.0mm distance from carotid/femoral sheath.",
            "tissue_shear_force_ceiling": "Applied tensile/shear force must not exceed 4.5 Newtons (prevents parenchymal tear).",
            "actuator_velocity_envelope": "Maximum tool tip speed <= 15 mm/s during active needle pass.",
        },
        metric_name="suture_placement_accuracy_mm",
        maximize=False,  # Lower error is better
        distillation_regexes=[
            (r"NoFlyZoneInfringement:\s*dist=([0-9\.]+)mm", "NoFlyZoneInfringement"),
            (r"ForceCeilingExceeded:\s*force=([0-9\.]+)N", "ForceCeilingExceeded"),
            (r"VelocityExceeded:\s*([^\n\r]+)", "VelocityExceeded"),
        ],
    ),

    # 15. DEEP SPACE: Autonomous Terrain-Relative Lunar/Mars Landing
    "BT-15": DomainBreakthroughSpec(
        domain_id="BT-15",
        name="Gravity-Turn Terrain-Relative Autonomous Planetary Lander",
        sector="Interplanetary Navigation & Lunar Surface Exploration",
        real_world_stake="Guarantees safe touchdown in rugged planetary crater fields (e.g. Lunar South Pole Shackleton Crater) without reliance on Earth telemetry, preserving propellant margins.",
        invariants={
            "touchdown_velocity_vector": "Vertical velocity <= 1.5 m/s, horizontal velocity <= 0.3 m/s at touchdown (t_final).",
            "glide_slope_cone": "Lander attitude must remain within 20-degree hazard avoidance cone of local gravity vector.",
            "monopropellant_reserve_floor": "Residual fuel upon engine shutdown must satisfy >= 5.0% dry mass reserve.",
        },
        metric_name="landing_pinpoint_accuracy_meters",
        maximize=False,  # Lower circular error probable is better
        distillation_regexes=[
            (r"HazardClash:\s*crater_slope=([0-9\.]+)deg", "HazardClash"),
            (r"TouchdownVelocityExceeded:\s*vz=([0-9\.]+)m_s", "TouchdownVelocityExceeded"),
            (r"FuelDepletedInDescent:\s*([^\n\r]+)", "FuelDepletedInDescent"),
        ],
    ),
}


def create_breakthrough_problem(spec: DomainBreakthroughSpec) -> Problem:
    """Creates an executable Problem instance from a DomainBreakthroughSpec."""
    return Problem(
        description=f"[{spec.domain_id} - {spec.sector}] {spec.name}: {spec.real_world_stake}",
        invariants=spec.invariants,
        metric_name=spec.metric_name,
        maximize=spec.maximize,
    )


def distill_domain_execution(
    spec: DomainBreakthroughSpec,
    raw_output: str,
    score: float,
    parent_score: float,
    status: str = "SUCCESS",
) -> DistilledExecutionSignature:
    """
    Distills domain-specific simulation logs into an atomic signature tuple,
    protecting the search tree from Softmax Inundation while retaining critical root causes.
    """
    raw_tokens = len(re.findall(r"\w+", raw_output)) or 1
    metric_delta = (score - parent_score) if spec.maximize else (parent_score - score)

    # Prioritize scanning for explicit constraint violations and critical anomalies
    matched_cause = None
    violation_keywords = ("violation", "breach", "clash", "overload", "crash", "trip", "infringement", "exceeded", "imbalance", "defect", "fail")

    # Pass 1: Check for hard invariant violations
    for pattern, label in spec.distillation_regexes:
        if any(vk in label.lower() for vk in violation_keywords):
            m = re.search(pattern, raw_output)
            if m:
                matched_cause = f"{label}: {m.group(0)[:60]}"
                status = "INVARIANT_VIOLATION"
                break

    # Pass 2: If no hard violation, check for diagnostic telemetry anomalies
    if not matched_cause:
        for pattern, label in spec.distillation_regexes:
            m = re.search(pattern, raw_output)
            if m:
                matched_cause = f"{label}: {m.group(0)[:60]}"
                if status == "SUCCESS" and "error" in label.lower():
                    status = "ANOMALY"
                break

    if not matched_cause and status != "SUCCESS":
        matched_cause = f"GenericExecutionFailure in {spec.domain_id}"

    summary = f"[{spec.domain_id}] Status={status} | Score={score:.4f} | Delta={metric_delta:+.4f}"
    if matched_cause:
        summary += f" | RootCause=[{matched_cause}]"

    distilled_tokens = len(re.findall(r"\w+", summary))

    return DistilledExecutionSignature(
        status=status,
        score=score,
        metric_delta=metric_delta,
        root_cause_signature=matched_cause,
        summary=summary,
        raw_tokens=raw_tokens,
        distilled_tokens=distilled_tokens,
    )
