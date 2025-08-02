"""
DXF utility functions for RajLisp Structural Design Suite
"""
import ezdxf
from ezdxf.math import Vec3


def create_dxf_header(doc, title="Structural Drawing"):
    """Create standard DXF header with drawing setup"""
    doc.header['$INSUNITS'] = 4  # Millimeters
    doc.header['$MEASUREMENT'] = 1  # Metric
    
    # Add standard layers
    layers = [
        ('OUTLINE', 1),  # Red
        ('DIMENSIONS', 2),  # Yellow  
        ('TEXT', 3),  # Green
        ('CONSTRUCTION', 4),  # Cyan
        ('REINFORCEMENT', 5),  # Blue
        ('HATCHING', 6),  # Magenta
    ]
    
    for layer_name, color in layers:
        if layer_name not in doc.layers:
            doc.layers.new(layer_name, dxfattribs={'color': color})
    
    return doc


def add_dimensions(msp, start_point, end_point, dim_line_y_offset=100, text=""):
    """Add dimension line between two points"""
    try:
        # Create dimension
        dim = msp.add_linear_dim(
            base=Vec3(start_point[0], start_point[1] + dim_line_y_offset, 0),
            p1=Vec3(start_point[0], start_point[1], 0),
            p2=Vec3(end_point[0], end_point[1], 0),
            dimstyle="EZDXF",
            dxfattribs={'layer': 'DIMENSIONS'}
        )
        
        if text:
            dim.dxf.text = text
            
        return dim
    except Exception:
        # Fallback: draw simple dimension lines
        # Dimension line
        msp.add_line(
            (start_point[0], start_point[1] + dim_line_y_offset),
            (end_point[0], end_point[1] + dim_line_y_offset),
            dxfattribs={'layer': 'DIMENSIONS', 'color': 2}
        )
        
        # Extension lines
        msp.add_line(
            start_point,
            (start_point[0], start_point[1] + dim_line_y_offset + 20),
            dxfattribs={'layer': 'DIMENSIONS', 'color': 2}
        )
        msp.add_line(
            end_point,
            (end_point[0], end_point[1] + dim_line_y_offset + 20),
            dxfattribs={'layer': 'DIMENSIONS', 'color': 2}
        )
        
        # Dimension text
        mid_x = (start_point[0] + end_point[0]) / 2
        text_y = start_point[1] + dim_line_y_offset + 30
        
        dimension_value = abs(end_point[0] - start_point[0])
        dim_text = text if text else f"{dimension_value:.0f}"
        
        msp.add_text(
            dim_text,
            height=50,
            dxfattribs={'layer': 'TEXT', 'color': 3}
        ).set_placement((mid_x, text_y), align="MIDDLE_CENTER")


def add_text_with_leader(msp, text, position, leader_points=None):
    """Add text with optional leader line"""
    # Add text
    text_entity = msp.add_text(
        text,
        height=40,
        dxfattribs={'layer': 'TEXT', 'color': 3}
    )
    text_entity.set_placement(position, align="MIDDLE_LEFT")
    
    # Add leader if points provided
    if leader_points:
        for i in range(len(leader_points) - 1):
            msp.add_line(
                leader_points[i],
                leader_points[i + 1],
                dxfattribs={'layer': 'CONSTRUCTION', 'color': 4}
            )
    
    return text_entity


def create_title_block(msp, drawing_title, scale="1:50", drawn_by="RajLisp"):
    """Create standard title block"""
    # Title block rectangle
    title_x = -2000
    title_y = -1500
    title_width = 4000
    title_height = 800
    
    # Main rectangle
    msp.add_lwpolyline([
        (title_x, title_y),
        (title_x + title_width, title_y),
        (title_x + title_width, title_y + title_height),
        (title_x, title_y + title_height),
        (title_x, title_y)
    ], dxfattribs={'layer': 'OUTLINE', 'color': 1})
    
    # Internal divisions
    msp.add_line(
        (title_x, title_y + 400),
        (title_x + title_width, title_y + 400),
        dxfattribs={'layer': 'OUTLINE', 'color': 1}
    )
    
    msp.add_line(
        (title_x + title_width - 1000, title_y),
        (title_x + title_width - 1000, title_y + 400),
        dxfattribs={'layer': 'OUTLINE', 'color': 1}
    )
    
    # Title text
    title_text = msp.add_text(
        drawing_title,
        height=120,
        dxfattribs={'layer': 'TEXT', 'color': 3}
    )
    title_text.set_placement((title_x + title_width/2, title_y + 600), align="MIDDLE_CENTER")
    
    # Scale text
    scale_text = msp.add_text(
        f"SCALE: {scale}",
        height=60,
        dxfattribs={'layer': 'TEXT', 'color': 3}
    )
    scale_text.set_placement((title_x + title_width - 500, title_y + 300), align="MIDDLE_CENTER")
    
    # Drawn by text
    drawn_text = msp.add_text(
        f"DRAWN BY: {drawn_by}",
        height=60,
        dxfattribs={'layer': 'TEXT', 'color': 3}
    )
    drawn_text.set_placement((title_x + title_width - 500, title_y + 150), align="MIDDLE_CENTER")


def add_grid_lines(msp, width, height, grid_spacing=1000):
    """Add construction grid lines"""
    # Vertical grid lines
    for x in range(0, int(width) + grid_spacing, grid_spacing):
        msp.add_line(
            (x, 0),
            (x, height),
            dxfattribs={'layer': 'CONSTRUCTION', 'color': 4, 'linetype': 'DASHDOT'}
        )
    
    # Horizontal grid lines  
    for y in range(0, int(height) + grid_spacing, grid_spacing):
        msp.add_line(
            (0, y),
            (width, y),
            dxfattribs={'layer': 'CONSTRUCTION', 'color': 4, 'linetype': 'DASHDOT'}
        )


def add_section_marker(msp, start_point, end_point, section_name="A"):
    """Add section cut marker"""
    # Section line
    msp.add_line(
        start_point,
        end_point,
        dxfattribs={'layer': 'CONSTRUCTION', 'color': 1, 'lineweight': 70}
    )
    
    # Arrow heads
    arrow_size = 100
    
    # Start arrow
    msp.add_lwpolyline([
        (start_point[0] - arrow_size, start_point[1] - arrow_size/2),
        start_point,
        (start_point[0] - arrow_size, start_point[1] + arrow_size/2),
        (start_point[0] - arrow_size, start_point[1] - arrow_size/2)
    ], dxfattribs={'layer': 'CONSTRUCTION', 'color': 1})
    
    # End arrow
    msp.add_lwpolyline([
        (end_point[0] + arrow_size, end_point[1] - arrow_size/2),
        end_point,
        (end_point[0] + arrow_size, end_point[1] + arrow_size/2),
        (end_point[0] + arrow_size, end_point[1] - arrow_size/2)
    ], dxfattribs={'layer': 'CONSTRUCTION', 'color': 1})
    
    # Section labels
    start_label = msp.add_text(
        section_name,
        height=80,
        dxfattribs={'layer': 'TEXT', 'color': 3}
    )
    start_label.set_placement((start_point[0] - 200, start_point[1] + 150), align="MIDDLE_CENTER")
    
    end_label = msp.add_text(
        section_name,
        height=80,
        dxfattribs={'layer': 'TEXT', 'color': 3}
    )
    end_label.set_placement((end_point[0] + 200, end_point[1] + 150), align="MIDDLE_CENTER")