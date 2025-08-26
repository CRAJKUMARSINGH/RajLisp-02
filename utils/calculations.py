"""
Structural calculation utilities for RajLisp Structural Design Suite
"""
import numpy as np
import math


def calculate_column_capacity(diameter, length, concrete_grade, steel_grade, steel_area):
    """Calculate axial capacity of circular column"""
    # Concrete properties
    fck_values = {'M20': 20, 'M25': 25, 'M30': 30, 'M35': 35, 'M40': 40, 'M45': 45}
    fck = fck_values.get(concrete_grade, 25)
    
    # Steel properties  
    fy_values = {'Fe415': 415, 'Fe500': 500, 'Fe550': 550}
    fy = fy_values.get(steel_grade, 415)
    
    # Column area
    area = math.pi * (diameter/2)**2
    
    # Steel ratio
    steel_ratio = steel_area / area
    
    # Effective length factor (assumed as pinned-pinned)
    le_factor = 1.0
    effective_length = le_factor * length
    
    # Slenderness ratio
    radius_of_gyration = diameter / 4
    slenderness_ratio = effective_length / radius_of_gyration
    
    # Check for short/long column
    if slenderness_ratio <= 12:
        # Short column
        p_design = 0.4 * fck * (area - steel_area) + 0.67 * fy * steel_area
    else:
        # Long column - apply reduction factor
        reduction_factor = 1.25 - (slenderness_ratio / 48)
        if reduction_factor < 0.3:
            reduction_factor = 0.3
        p_design = reduction_factor * (0.4 * fck * (area - steel_area) + 0.67 * fy * steel_area)
    
    return {
        'capacity': p_design / 1000,  # Convert to kN
        'axial_capacity': p_design / 1000,
        'area': area,
        'steel_ratio': steel_ratio * 100,  # Percentage
        'slenderness_ratio': slenderness_ratio,
        'column_type': 'Short' if slenderness_ratio <= 12 else 'Long'
    }


def calculate_rectangular_column_capacity(width, depth, length, concrete_grade, steel_grade, steel_area):
    """Calculate axial capacity of rectangular column"""
    # Concrete properties
    fck_values = {'M20': 20, 'M25': 25, 'M30': 30, 'M35': 35, 'M40': 40, 'M45': 45}
    fck = fck_values.get(concrete_grade, 25)
    
    # Steel properties
    fy_values = {'Fe415': 415, 'Fe500': 500, 'Fe550': 550}
    fy = fy_values.get(steel_grade, 415)
    
    # Column area
    area = width * depth
    
    # Steel ratio
    steel_ratio = steel_area / area
    
    # Effective length factor
    le_factor = 1.0
    effective_length = le_factor * length
    
    # Radius of gyration for rectangular section
    radius_of_gyration = min(width, depth) / (2 * math.sqrt(3))
    slenderness_ratio = effective_length / radius_of_gyration
    
    # Capacity calculation
    if slenderness_ratio <= 12:
        # Short column
        p_design = 0.4 * fck * (area - steel_area) + 0.67 * fy * steel_area
    else:
        # Long column
        reduction_factor = 1.25 - (slenderness_ratio / 48)
        if reduction_factor < 0.3:
            reduction_factor = 0.3
        p_design = reduction_factor * (0.4 * fck * (area - steel_area) + 0.67 * fy * steel_area)
    
    return {
        'capacity': p_design / 1000,  # Convert to kN
        'axial_capacity': p_design / 1000,
        'area': area,
        'steel_ratio': steel_ratio * 100,
        'slenderness_ratio': slenderness_ratio,
        'column_type': 'Short' if slenderness_ratio <= 12 else 'Long'
    }


def calculate_footing_bearing_capacity(footing_width, footing_depth, soil_bearing_capacity, load):
    """Calculate footing bearing pressure and safety factor"""
    # Footing area
    if isinstance(footing_width, (int, float)) and isinstance(footing_depth, (int, float)):
        # Rectangular footing
        area = footing_width * footing_depth
    else:
        # Circular footing - footing_width is diameter
        area = math.pi * (footing_width/2)**2
    
    # Bearing pressure
    bearing_pressure = load / area
    
    # Safety factor
    safety_factor = soil_bearing_capacity / bearing_pressure
    
    return {
        'area': area,
        'bearing_pressure': bearing_pressure,
        'safety_factor': safety_factor,
        'status': 'Safe' if safety_factor >= 2.5 else 'Unsafe'
    }


def calculate_beam_moment_capacity(width, depth, concrete_grade, steel_grade, tension_steel, compression_steel=0):
    """Calculate moment capacity of beam section"""
    # Material properties
    fck_values = {'M20': 20, 'M25': 25, 'M30': 30, 'M35': 35, 'M40': 40, 'M45': 45}
    fck = fck_values.get(concrete_grade, 25)
    
    fy_values = {'Fe415': 415, 'Fe500': 500, 'Fe550': 550}
    fy = fy_values.get(steel_grade, 415)
    
    # Effective depth (assumed 90% of total depth)
    d = 0.9 * depth
    
    # Steel areas
    ast = tension_steel
    asc = compression_steel
    
    # Balanced steel ratio
    xu_max = 0.48 * d  # Maximum neutral axis depth
    ast_balanced = 0.36 * fck * width * xu_max / (0.87 * fy)
    
    # Check if section is under-reinforced
    if ast <= ast_balanced:
        # Under-reinforced section
        xu = ast * 0.87 * fy / (0.36 * fck * width)
        moment_capacity = 0.87 * fy * ast * (d - 0.42 * xu)
    else:
        # Over-reinforced - limit to balanced
        xu = xu_max
        moment_capacity = 0.87 * fy * ast_balanced * (d - 0.42 * xu)
    
    # Add compression steel contribution if present
    if asc > 0:
        moment_capacity += 0.87 * fy * asc * (d - 50)  # Assumed 50mm cover
    
    return {
        'moment_capacity': moment_capacity / 1e6,  # Convert to kNm
        'steel_ratio': (ast / (width * d)) * 100,
        'section_type': 'Under-reinforced' if ast <= ast_balanced else 'Over-reinforced',
        'balanced_steel': ast_balanced
    }


def calculate_shear_capacity(width, depth, concrete_grade, stirrup_diameter, stirrup_spacing):
    """Calculate shear capacity of beam"""
    fck_values = {'M20': 20, 'M25': 25, 'M30': 30, 'M35': 35, 'M40': 40, 'M45': 45}
    fck = fck_values.get(concrete_grade, 25)
    
    # Effective depth
    d = 0.9 * depth
    
    # Concrete shear strength
    tau_c = 0.62 * math.sqrt(fck)  # Simplified
    vc_concrete = tau_c * width * d
    
    # Stirrup contribution
    if stirrup_spacing > 0:
        asv = 2 * math.pi * (stirrup_diameter/2)**2  # Two legs
        vc_stirrup = 0.87 * 415 * asv * d / stirrup_spacing  # Assuming Fe415 stirrups
    else:
        vc_stirrup = 0
    
    total_shear_capacity = vc_concrete + vc_stirrup
    
    return {
        'shear_capacity': total_shear_capacity / 1000,  # Convert to kN
        'concrete_contribution': vc_concrete / 1000,
        'stirrup_contribution': vc_stirrup / 1000
    }


def calculate_deflection_check(span, depth, loading_type='uniformly_distributed'):
    """Check deflection limits"""
    # Basic span-to-depth ratios from IS 456
    if loading_type == 'simply_supported':
        basic_ratio = 20
    elif loading_type == 'continuous':
        basic_ratio = 26
    elif loading_type == 'cantilever':
        basic_ratio = 7
    else:
        basic_ratio = 20  # Default
    
    actual_ratio = span / depth
    
    return {
        'span_depth_ratio': actual_ratio,
        'allowable_ratio': basic_ratio,
        'status': 'OK' if actual_ratio <= basic_ratio else 'Increase depth',
        'deflection_ok': actual_ratio <= basic_ratio
    }


def calculate_staircase_design(riser, tread, waist_thickness, span, load):
    """Calculate staircase structural parameters"""
    # Effective span
    effective_span = span + waist_thickness
    
    # Step angle
    step_angle = math.atan(riser / tread)
    step_angle_degrees = math.degrees(step_angle)
    
    # Effective thickness
    effective_thickness = waist_thickness / math.cos(step_angle)
    
    # Load calculations
    dead_load = 25 * effective_thickness / 1000  # Concrete self-weight
    step_weight = 25 * (riser * tread / 2) / (tread * 1000)  # Triangular step weight
    total_dead_load = dead_load + step_weight
    
    # Total load
    total_load = total_dead_load + load
    
    # Moment
    moment = total_load * effective_span**2 / 8
    
    return {
        'step_angle': step_angle_degrees,
        'effective_thickness': effective_thickness,
        'effective_span': effective_span,
        'total_load': total_load,
        'moment': moment,
        'dead_load': total_dead_load
    }


def calculate_development_length(bar_diameter, concrete_grade, steel_grade):
    """Calculate development length for reinforcement"""
    fck_values = {'M20': 20, 'M25': 25, 'M30': 30, 'M35': 35, 'M40': 40, 'M45': 45}
    fck = fck_values.get(concrete_grade, 25)
    
    fy_values = {'Fe415': 415, 'Fe500': 500, 'Fe550': 550}
    fy = fy_values.get(steel_grade, 415)
    
    # Bond stress
    tau_bd = 1.2 * math.sqrt(fck)  # For plain bars
    
    # Development length
    ld = (fy * bar_diameter) / (4 * tau_bd)
    
    return {
        'development_length': ld,
        'bond_stress': tau_bd
    }


def check_crack_width(cover, bar_spacing, steel_stress):
    """Check crack width in concrete"""
    # Simplified crack width calculation
    crack_width = (3 * steel_stress * cover) / (1000 * bar_spacing)
    
    allowable_crack_width = 0.3  # mm for normal exposure
    
    return {
        'crack_width': crack_width,
        'allowable': allowable_crack_width,
        'status': 'OK' if crack_width <= allowable_crack_width else 'Reduce spacing'
    }


def calculate_footing_design(footing_type, footing_dimension, footing_thickness, column_load, 
                           soil_bearing_capacity, concrete_grade, steel_grade, main_bar_dia, 
                           main_bar_spacing, dist_bar_dia, dist_bar_spacing):
    """Calculate footing design parameters and reinforcement"""
    
    # Material properties
    fck_values = {'M20': 20, 'M25': 25, 'M30': 30, 'M35': 35, 'M40': 40, 'M45': 45}
    fck = fck_values.get(concrete_grade, 25)
    
    fy_values = {'Fe415': 415, 'Fe500': 500, 'Fe550': 550}
    fy = fy_values.get(steel_grade, 415)
    
    # Calculate footing area and bearing pressure
    if footing_type == "Square":
        footing_area = footing_dimension ** 2
        footing_width = footing_dimension
        footing_depth = footing_dimension
    elif footing_type == "Rectangular":
        # Assume 1.5:1 ratio for rectangular footing
        footing_width = footing_dimension * 1.2
        footing_depth = footing_dimension
        footing_area = footing_width * footing_depth
    else:  # Circular
        footing_area = math.pi * (footing_dimension/2)**2
        footing_width = footing_dimension
        footing_depth = footing_dimension
    
    # Self weight of footing
    footing_self_weight = footing_area * footing_thickness * 25 / 1000  # kN (25 kN/m³ for concrete)
    total_load = column_load + footing_self_weight
    
    # Bearing pressure
    bearing_pressure = total_load / footing_area
    
    # Safety factor against bearing failure
    bearing_safety_factor = soil_bearing_capacity / bearing_pressure
    
    # Punching shear check
    effective_depth = footing_thickness - 75  # Assuming 75mm cover
    critical_perimeter = 4 * (300 + effective_depth)  # Assuming 300mm column
    punching_shear_stress = (total_load * 1000) / (critical_perimeter * effective_depth)
    allowable_punching_shear = 0.62 * math.sqrt(fck)
    punching_safety_factor = allowable_punching_shear / punching_shear_stress
    
    # Bending moment calculation (simplified)
    if footing_type == "Square":
        cantilever_length = (footing_dimension - 0.3) / 2  # Assuming 300mm column
        bending_moment = (bearing_pressure * footing_dimension * cantilever_length**2) / 2
    else:
        cantilever_length = (footing_width - 0.3) / 2
        bending_moment = (bearing_pressure * footing_width * cantilever_length**2) / 2
    
    # Required steel area
    moment_arm = 0.87 * effective_depth
    required_steel_area = (bending_moment * 1e6) / (0.87 * fy * moment_arm)
    
    # Provided steel area
    if footing_type == "Circular":
        num_bars = int(math.pi * footing_dimension / main_bar_spacing)
    else:
        num_bars = int(footing_width / main_bar_spacing)
    
    provided_main_area = num_bars * math.pi * (main_bar_dia/2)**2
    
    # Distribution steel
    dist_steel_area = 0.12 * footing_area * footing_thickness / 100  # 0.12% minimum
    provided_dist_area = (footing_depth / dist_bar_spacing) * math.pi * (dist_bar_dia/2)**2
    
    # Steel ratios
    main_steel_ratio = (provided_main_area / (footing_width * effective_depth)) * 100
    dist_steel_ratio = (provided_dist_area / (footing_depth * effective_depth)) * 100
    
    return {
        'footing_area': footing_area,
        'footing_self_weight': footing_self_weight,
        'total_load': total_load,
        'bearing_pressure': bearing_pressure,
        'bearing_safety_factor': bearing_safety_factor,
        'bearing_status': 'Safe' if bearing_safety_factor >= 2.5 else 'Unsafe',
        'punching_shear_stress': punching_shear_stress,
        'allowable_punching_shear': allowable_punching_shear,
        'punching_safety_factor': punching_safety_factor,
        'punching_status': 'Safe' if punching_safety_factor >= 2.0 else 'Unsafe',
        'bending_moment': bending_moment,
        'required_steel_area': required_steel_area,
        'provided_main_area': provided_main_area,
        'provided_dist_area': provided_dist_area,
        'main_steel_ratio': main_steel_ratio,
        'dist_steel_ratio': dist_steel_ratio,
        'main_steel_status': 'OK' if provided_main_area >= required_steel_area else 'Increase steel',
        'dist_steel_status': 'OK' if provided_dist_area >= dist_steel_area else 'Increase steel',
        'num_main_bars': num_bars,
        'effective_depth': effective_depth
    }