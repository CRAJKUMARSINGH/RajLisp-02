import math
import os
import pandas as pd
import ezdxf
from ezdxf import *
from ezdxf.entities import Line, Circle, Arc
from math import atan2, degrees, sqrt, cos, sin, tan, radians, pi
# Clear previously defined global variables
for var in list(globals().keys()):
    if var.startswith('my_'):  # Use a common prefix for variables or filter by other criteria
        del globals()[var]                
# Define the add_text function
def add_text(text, insert, height, rotation):
    doc.modelspace().add_text(text, dxfattribs={'height': height, 'insert': insert, 'rotation': rotation})
# Create a DXF R2010 document and use default setup 
doc = ezdxf.new("R2010", setup=True)
msp = doc.modelspace()
# Helper functions for drawing
def draw_line(msp, points):
    for i in range(len(points) - 1):
        msp.add_line(points[i], points[i + 1])
def draw_rectangle(msp, pt1, pt2):
    msp.add_line(pt1, (pt2[0], pt1[1]))  # Bottom line
    msp.add_line((pt2[0], pt1[1]), pt2)  # Right line
    msp.add_line(pt2, (pt1[0], pt2[1]))  # Top line
    msp.add_line((pt1[0], pt2[1]), pt1)  # Left line
########################################################
# File operations
def opn():
    try:
        directory = r"F:\LISP 2005\P1"
        filename = "input.xlsx"
        file_path = os.path.join(directory, filename)  # Define the file_path
        f = open(file_path, "r")
        print("\nFile opened successfully.")
        return f
    except FileNotFoundError:
        print("\nError: Could not open the file.")
        exit()
#################################################
# Read variables from Excel file
def read_variables(file_path):
    try:
        df = pd.read_excel(file_path, header=None)
        df.columns = ['Value', 'Variable', 'Description']
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None
# Read variables from Excel file
file_path = r'F:\LISP 2005\P1\input.xlsx'
df = read_variables(file_path)
if df is not None:
    # Print the first output of data read
    print(df.head(1))
    # Define variables
    Scale1 = df.loc[df['Variable'] == 'SCALE1', 'Value'].values[0]
    Scale2 = df.loc[df['Variable'] == 'SCALE2', 'Value'].values[0]    
    skew = df.loc[df['Variable'] == 'SKEW', 'Value'].values[0]
    # Calculate sc
    sc = Scale1 / Scale2
    print(f"sc = {sc}")
    # Print variables
    for index, row in df.iterrows():
        print(f"Variable: {row['Variable']}, Value: {row['Value']}")
#######################################   

#######################################
def st(doc):
    # Set up a style (font) in the document
    # Note: ezdxf does not have direct control over many of these settings as AutoCAD does,
    # so we'll focus on what we can control.
    doc.styles.new("Arial", dxfattribs={'font': 'Arial.ttf'})  # Assuming Arial.ttf is available
    # Set up dimension style properties
    dimstyle = doc.dimstyles.new('PMB100')
    # Set dimension arrow size (DIMASZ)
    dimstyle.dxf.dimasz = 150
    # Set dimension decimal places (DIMDEC)
    # This is not directly supported by ezdxf, but we can set precision for dimension texts
    dimstyle.dxf.dimtdec = 0  # 0 decimal places
    # Set dimension extension line extension (DIMEXE)
    dimstyle.dxf.dimexe = 400
    # Set dimension extension line offset (DIMEXO)
    dimstyle.dxf.dimexo = 400    
    # Set dimension scale factor (DIMLFAC)
    dimstyle.dxf.dimlfac = 1   
    # Set dimension text style (DIMTXSTY)
    dimstyle.dxf.dimtxsty = "Arial"   
    # Set dimension text height (DIMTXT)
    dimstyle.dxf.dimtxt = 400   
    # Set dimension text above dimension line (DIMTAD)
    dimstyle.dxf.dimtad = 0  # 0 means below    
    # Set dimension text inside extension linedef reed(f):
    variables = [
    'SCALE1', 'SCALE2', 'SKEW', 'DATUM', 'TOPRL', 'LEFT', 'RIGHT', 'XINCR', 'YINCR', 'NOCH',
    'NSPAN', 'LBRIDGE', 'ABTL', 'RTL', 'SOFL', 'KERBW', 'KERBD', 'CCBR', 'SLBTHC', 'SLBTHE',
    'SLBTHT', 'CAPT', 'CAPB', 'CAPW', 'PIERTW', 'BATTR', 'PIERST', 'PIERN', 'SPAN1', 'FUTRL',
    'FUTD', 'FUTW', 'FUTL', 'DWTH', 'ALCW', 'ALCD', 'ALFB', 'ALFBL', 'ALTB', 'ALTBL', 'ALFO',
    'ALBB', 'ALBBL', 'ABTLEN', 'laslab', 'APWTH', 'APTHK', 'WCTH'
]
    data = {}
#########################################
# Read variables from Excel file
# Initialize the dictionary to store variable values
variable_values = {}
# Populate the dictionary with unique variables
if 'Variable' in df.columns:
    variable_values['scale1'] = df.loc[df['Variable'] == 'SCALE1', 'Value'].values[0]  # Scale1
else:
    print("Error: 'Variable' column not found in DataFrame")
variable_values['scale1'] = df.loc[df['Variable'] == 'SCALE1', 'Value'].values[0]  # Scale1
variable_values['abtlen'] = df.loc[df['Variable'] == 'ABTLEN', 'Value'].values[0]  # Length of Abutment
variable_values['dwth'] = df.loc[df['Variable'] == 'DWTH', 'Value'].values[0]  # Dirtwall Thickness
variable_values['alcw'] = df.loc[df['Variable'] == 'ALCW', 'Value'].values[0]  # Abutment Left Cap Width Excluding D/W
variable_values['alfl'] = df.loc[df['Variable'] == 'ALFL', 'Value'].values[0]  # Abutment Left Footing Level
variable_values['arfl'] = df.loc[df['Variable'] == 'ARFL', 'Value'].values[0]  # Abutment Right Footing Level
variable_values['alcd'] = df.loc[df['Variable'] == 'ALCD', 'Value'].values[0]  # Abutment Left Cap Depth
variable_values['alfb'] = df.loc[df['Variable'] == 'ALFB', 'Value'].values[0]  # Abutment Left Front Batter
variable_values['alfbl'] = df.loc[df['Variable'] == 'ALFBL', 'Value'].values[0]  # Abutment Left Front Batter RL
variable_values['alfbr'] = df.loc[df['Variable'] == 'ALFBR', 'Value'].values[0]  # Abutment Right Front Batter RL
variable_values['altb'] = df.loc[df['Variable'] == 'ALTB', 'Value'].values[0]  # Abutment Left Toe Batter
variable_values['altbl'] = df.loc[df['Variable'] == 'ALTBL', 'Value'].values[0]  # Abutment Left Toe Batter Level Footing Top
variable_values['altbr'] = df.loc[df['Variable'] == 'ALTBR', 'Value'].values[0]  # Abutment Right Toe Batter Level Footing Top
variable_values['alfo'] = df.loc[df['Variable'] == 'ALFO', 'Value'].values[0]  # Abutment Left Front Offset To Footing
variable_values['alfd'] = df.loc[df['Variable'] == 'ALFD', 'Value'].values[0]  # Abutment Left Footing Depth
variable_values['albb'] = df.loc[df['Variable'] == 'ALBB', 'Value'].values[0]  # Abutment Left Back Batter
variable_values['albbl'] = df.loc[df['Variable'] == 'ALBBL', 'Value'].values[0]  # Abutment Left Back Batter RL
variable_values['albbr'] = df.loc[df['Variable'] == 'ALBBR', 'Value'].values[0]  # Abutment Right Back Batter RL
variable_values['scale2'] = df.loc[df['Variable'] == 'SCALE2', 'Value'].values[0]  # Scale2
variable_values['skew'] = df.loc[df['Variable'] == 'SKEW', 'Value'].values[0]  # Degree Of Skew
variable_values['datum'] = df.loc[df['Variable'] == 'DATUM', 'Value'].values[0]  # Datum
variable_values['toprl'] = df.loc[df['Variable'] == 'TOPRL', 'Value'].values[0]  # Top RL Of The Bridge
variable_values['left'] = df.loc[df['Variable'] == 'LEFT', 'Value'].values[0]  # Left Most Chainage
variable_values['right'] = df.loc[df['Variable'] == 'RIGHT', 'Value'].values[0]  # Right Most Chainage
variable_values['xincr'] = df.loc[df['Variable'] == 'XINCR', 'Value'].values[0]  # Chainage Increment In X Direction
variable_values['yincr'] = df.loc[df['Variable'] == 'YINCR', 'Value'].values[0]  # Elevation Increment In Y Direction
variable_values['noch'] = df.loc[df['Variable'] == 'NOCH', 'Value'].values[0]  # Total No. Of Chainages
variable_values['nspan'] = df.loc[df['Variable'] == 'NSPAN', 'Value'].values[0]  # Number of Spans
variable_values['lbridge'] = df.loc[df['Variable'] == 'LBRIDGE', 'Value'].values[0]  # Length Of Bridge
variable_values['abtl'] = df.loc[df['Variable'] == 'ABTL', 'Value'].values[0]  # Chainage Of Left Abutment
variable_values['rtl'] = df.loc[df['Variable'] == 'RTL', 'Value'].values[0]  # Road Top Level
variable_values['sofl'] = df.loc[df['Variable'] == 'SOFL', 'Value'].values[0]  # Soffit Level
variable_values['kerbw'] = df.loc[df['Variable'] == 'KERBW', 'Value'].values[0]  # Width Of Kerb
variable_values['kerbd'] = df.loc[df['Variable'] == 'KERBD', 'Value'].values[0]  # Depth Of Kerb
variable_values['ccbr'] = df.loc[df['Variable'] == 'CCBR', 'Value'].values[0]  # Clear Carriageway Width
variable_values['slbthc'] = df.loc[df['Variable'] == 'SLBTHC', 'Value'].values[0]  # Thickness Of Slab Centre
variable_values['slbthe'] = df.loc[df['Variable'] == 'SLBTHE', 'Value'].values[0]  # Thickness Of Slab Edge
variable_values['slbtht'] = df.loc[df['Variable'] == 'SLBTHT', 'Value'].values[0]  # Thickness Of Slab Tip
variable_values['capt'] = df.loc[df['Variable'] == 'CAPT', 'Value'].values[0]  # Pier Cap Top RL
variable_values['capb'] = df.loc[df['Variable'] == 'CAPB', 'Value'].values[0]  # Pier Cap Bottom RL
variable_values['capw'] = df.loc[df['Variable'] == 'CAPW', 'Value'].values[0]  # Cap Width
variable_values['piertw'] = df.loc[df['Variable'] == 'PIERTW', 'Value'].values[0]  # Pier Top Width
variable_values['battr'] = df.loc[df['Variable'] == 'BATTR', 'Value'].values[0]  # Pier Batter
variable_values['pierst'] = df.loc[df['Variable'] == 'PIERST', 'Value'].values[0]  # Straight Length Of Pier
variable_values['piern'] = df.loc[df['Variable'] == 'PIERN', 'Value'].values[0]  # Pier Sr No.
variable_values['span1'] = df.loc[df['Variable'] == 'SPAN1', 'Value'].values[0]  # Span Individual Length
variable_values['futrl'] = df.loc[df['Variable'] == 'FUTRL', 'Value'].values[0]  # Founding RL
variable_values['futd'] = df.loc[df['Variable'] == 'FUTD', 'Value'].values[0]  # Depth Of Footing
variable_values['futw'] = df.loc[df['Variable'] == 'FUTW', 'Value'].values[0]  # Width Of Footing
variable_values['futl'] = df.loc[df['Variable'] == 'FUTL', 'Value'].values[0]  # Length Of Footing
variable_values['laslab'] = df.loc[df['Variable'] == 'LASLAB', 'Value'].values[0]  # Length of Approach Slab
variable_values['apwth'] = df.loc[df['Variable'] == 'APWTH', 'Value'].values[0]  # Width of Approach Slab
variable_values['apthk'] = df.loc[df['Variable'] == 'APTHK', 'Value'].values[0]  # Thickness of Approach Slab
variable_values['wcth'] = df.loc[df['Variable'] == 'WCTH', 'Value'].values[0]  # Thickness of Wearing Course
# Assigning variables from the dictionary
for key, value in variable_values.items():
    globals()[key] = value  # Dynamically create global variables
nspan = int(nspan)  # Convert dynamically if it's not already an integer
noch = int(noch)  # Convert dynamically if it's not already an integer
####################################################
import math
# Perform calculations
hs = 1
vs = 1
sc = Scale1 / Scale2
vvs = 1000.0 / vs
hhs = 1000.0 / hs
skew1 = skew * 0.0174532  # Convert degrees to radians
s = math.sin(skew1)
c = math.cos(skew1)
tn = s / c
# Print the computed values and the result of the sine, cosine, and tangent calculations
print(f"vvs: {vvs}")
print(f"hhs: {hhs}")
print(f"skew1 (radians): {skew1}")
print(f"sin(skew1): {s}")
print(f"cos(skew1): {c}")
print(f"tan(skew1): {tn}")
print(f"sc: {sc}")
###############################################################
def vpos(a):
    return datum + vvs * (a - datum)   
def hpos(a):
    return left + hhs * (a - left)
def v2pos(a):
    return datum + sc * vvs * (a - datum)
def h2pos(a):
    return left + sc * hhs * (a - left)
################################################################################################
# 3.0 plotting layout of elevation ( X axis Y axis etc.) 
#############################################################
##########################################
left = int(left)    
    # Define distance between lines parallel to X axis
def turn_off_osnap(doc):
    # Simulate saving the OSNAP state
    osnap_mode = doc.header.get('$OSMODE', None)  # $OSMODE corresponds to the OSMODE system variable in DXF
    print(f"OSNAP mode saved: {osnap_mode}")
    # Simulate turning off OSNAP
    doc.header['$OSMODE'] = 0  # Set OSMODE to 0
    print("OSNAP mode turned off.")
# Convert the `left` value to an integer equivalent
def adjust_left_value(left):
    adjusted_left = left - (left % 1.0)
    return adjusted_left
# Create or load a DXF document
turn_off_osnap(doc)
# Set and adjust the `left` variable
left = adjust_left_value(left)
print(f"Adjusted left value: {left}")
d1 = 20  # Distance in mm
pta1 = (left - laslab, datum)
ptb1 = (left, datum - d1 * scale1)
#############################################################
##########################################
pta2 = [hpos(lbridge + laslab), datum]
ptb2 = [hpos(right), datum - d1 * scale1]
#############################################################
##########################################
ptc1 = [left, datum - 2 * d1 * scale1]
ptc2 = [hpos(right), datum - 2 * d1 * scale1]
ptd1 = [left, vpos(toprl)]
    # Draw X-axis
msp.add_line(pta1, pta2)   
    # Draw lines parallel to X-axis
msp.add_line(ptb1, ptb2)  # 20mm below
msp.add_line(ptc1, ptc2)  # 40mm below   
########################## DRAWING BOUNDARY ###### POINTS
prb3 = ptc2 # DRAWING BOUNDARY ###### POINTS
prb4 = ptc1 # DRAWING BOUNDARY ###### POINTS
    # Draw Y-axis
msp.add_line(ptc1, ptd1)      
    # Add text for "BED LEVEL" and "CHAINAGE"
ptb3 = (left - 25 * scale1, datum - d1 * 0.5 * scale1)
msp.add_text("BED LEVEL", dxfattribs={'height': 2.5 * scale1, 'insert': ptb3, 'halign': 0})   
ptb3 = (left - 25 * scale1, datum - d1 * 1.5 * scale1)
msp.add_text("CHAINAGE", dxfattribs={'height': 2.5 * scale1, 'insert': ptb3, 'halign': 0})   
    # Define half length for small lines on Y axis
d2 = 2.5    
    # Draw small lines on Y axis
small_line_start = (left - d2 * scale1, datum)
small_line_end = (left + d2 * scale1, datum)
msp.add_line(small_line_start, small_line_end)  
nov = int((toprl - datum) // 1)  

#######################

variable_values['yincr'] = yincr    
    # Write levels on Y axis
n = (nov // yincr)
a = 0
while a <= n:
    lvl = datum + a * yincr
    b1 = "{:.3f}".format(lvl)  # converts lvl into fixed format like 100.000    
    pta1 = [left - 13 * scale1, vpos(lvl) - 1.0 * scale1]
    # Assuming you have a function or method to add text to the drawing
    # Calculate the height of the text
    # Calculate the height of the text    
    text_height = 2.0 * scale1
    # Add the text to the modelspace at the specified position
    msp.add_text(b1, dxfattribs={'height': text_height, 'rotation': 0, 'insert': pta1})
    small_line_start = (left - d2 * scale1, vpos(lvl))
    small_line_end = (left + d2 * scale1, vpos(lvl))    
    msp.add_line(small_line_start, small_line_end)
    a += 1
##########################################################################
# Write chainages on X axis
noh = right - left
n = int(noh // xincr)
d4 = 2 * d1
d5 = d4 - 2.0
d6 = d1 + 2.0
d7 = d1 - 2.0
d8 = d4 - 4.0
d9 = d1 - 4.0
for a in range(0, n + 2):
        ch = left + a * xincr
        b1 = f"{ch:.3f}"
        # Position for chainage text
        pta1 = [scale1 + hpos(ch), datum - d8 * scale1]
        add_text(b1, pta1, 2.0 * scale1, 90)
        pta1 = [hpos(ch), datum - d4 * scale1]
        pta2 = [hpos(ch), datum - d5 * scale1]
        pta3 = [hpos(ch), datum - d6 * scale1]
        pta4 = [hpos(ch), datum - d7 * scale1]
def draw_line(pt1, pt2):
    doc.modelspace().add_line(pt1, pt2, dxfattribs={'color': 7})
draw_line(pta1, pta2)
draw_line(pta3, pta4)
###############################################################
# 4.0 plotting cross section of the river and writing chainages
# # Function to read variables and plot directly
def cs():
    global left, hhs, d8, d9, d4, d5, d6, d7, xincr, b2, b1, ptb3, vpos
    # File path to the Excel file
    file_path = r'F:\LISP 2005\P1\input.xlsx'
    try:
        # Read variable 'noch' from Sheet1
        sheet1 = pd.read_excel(file_path, sheet_name="Sheet1")
        noch = int(sheet1.iloc[20, 0])  # Read 'noch' from A21 (index 20 for 0-based)
        if not noch:
            print("Error: 'noch' variable is missing or invalid. Exiting function.")
            return
    except Exception as e:
        print(f"Error reading 'noch': {e}")
        return
    try:
        # Read chainages and RLs from Sheet2
        sheet2 = pd.read_excel(file_path, sheet_name="Sheet2")
        chainages = sheet2['Chainage (x)']
        rls = sheet2['RL (y)']
    except Exception as e:
        print(f"Error reading Sheet2: {e}")
        return
    # Initialize text labels
    b2 = "RL"
    b1 = "CH"
    # Initialize variables
    a = 1
    ptb3 = None
    # Loop through the data and plot immediately
    for x, y in zip(chainages, rls):
        try:
            # Convert to float, skip invalid data
            x = float(x)
            y = float(y)
        except ValueError:
            print(f"Invalid data found: Chainage: {x}, RL: {y}")
            continue
        xx = hpos(x)
        pta1 = [xx + 0.9 * scale1, datum - d8 * scale1]
        pta2 = [xx + 0.9 * scale1, datum - d9 * scale1]
        # Write level along x-axis
        #msp.add_text(y, dxfattribs={'insert': pta2, 'height': 2 * scale1, 'rotation': 90})
        # Check if chainage x is a multiplier of increment
        b = (x - left) % xincr
        if b != 0.0:
            # Draw small lines along the X axis
            pta3 = [xx, datum - d4 * scale1]
            pta4 = [xx, datum - d5 * scale1]
            msp.add_line(pta3, pta4)        
            pta5 = [xx, datum - d6 * scale1]
            pta6 = [xx, datum - d7 * scale1]
            msp.add_line(pta5, pta6)
            pta7 = [xx, datum - 2 * scale1]
            pta8 = [xx, datum]
            msp.add_line(pta7, pta8)
        ptb4 = [xx, vpos(y)]
        if a != 1:
            # Draw connecting line between current and previous point
            msp.add_line(ptb3, ptb4)
        ptb3 = ptb4  # Update ptb3 for the next loop iteration
        a += 1
            # Draw connecting line between current and previous point        
        ptb3 = ptb4  # Update ptb3 for the next loop iteration
        print(f"ptb3: {ptb3}, ptb4: {ptb4}")
        rounded_x = round(x, 2)
        msp.add_text(rounded_x, dxfattribs={'height': 2 * scale1, 'insert': pta1, 'rotation': 90})                          
        rounded_y = round(y, 2)
        msp.add_text(rounded_y, dxfattribs={'height': 2 * scale1, 'insert': pta2, 'rotation': 90})  
        a += 1
# Call the function to generate the drawing
cs()
#################################################################
# 5.3 Drawing Super Structure in elevation
###################################################
############################ 
spans = abtl        # ; starting chainage of span
spane = spans + span1       #; end chainage of span    
lspan = span1 
rtl = df.loc[df['Variable'] == 'RTL', 'Value'].values[0]
x1 = hpos(abtl)
y1 = vpos(rtl)
x2 = hpos(abtl + lspan) 
y2 = vpos(sofl)
pta1 = [x1 + 25.0, y1]
pta2 = [x2 - 25.0, y2]
msp.add_lwpolyline([pta1, [pta2[0], pta1[1]], pta2, [pta1[0], pta2[1]], pta1], close=True)
g1 = msp.query('LWPOLYLINE')[-1]
# Corrected array insertion
nspan = int(nspan)
for i in range(nspan):
    new_entity = g1.copy()
    points = [(vertex[0] + i * span1 * hhs, vertex[1]) for vertex in new_entity.get_points()]
    new_entity.set_points(points)
    msp.add_entity(new_entity)
#######################
# Left Approach Slab Coordinates
x1_left = hpos(abtl - laslab)  # Starting point of the left approach slab, flush with deck slab
x2_left = hpos(abtl)  # End of the left approach slab (flush with expansion joint)
y1_left = vpos(rtl)  # Top of the deck slab, same as RTL
y2_left = vpos(rtl - apthk)  # Bottom of the approach slab, considering thickness
# Draw Left Approach Slab with Expansion Joint (25 mm gap between)
pta1_left = [x1_left, y1_left]
pta2_left = [x2_left, y2_left]
msp.add_lwpolyline([pta1_left, [pta2_left[0], pta1_left[1]], pta2_left, [pta1_left[0], pta2_left[1]], pta1_left], close=True)
# Right Approach Slab Coordinates
x1_right = hpos(abtl + (nspan * span1))  # Starting point of the right approach slab, flush with deck slab
x2_right = hpos(abtl + (nspan * span1) + laslab)  # End of the right approach slab
y1_right = vpos(rtl)  # Top of the deck slab, same as RTL
y2_right = vpos(rtl - apthk)  # Bottom of the approach slab, considering thickness
# Draw Right Approach Slab with Expansion Joint (25 mm gap between)
pta1_right = [x1_right, y1_right]
pta2_right = [x2_right, y2_right]
msp.add_lwpolyline([pta1_right, [pta2_right[0], pta1_right[1]], pta2_right, [pta1_right[0], pta2_right[1]], pta1_right], close=True)
# Draw the continuous wearing course (across all slabs)
# Ensure the thickness of the expansion joint (25 mm = 0.025 m)
expansion_joint_thickness = 25 / 1000  # Convert 25 mm to meters (0.025 m)
# Read the wearing course thickness from the Excel file (already in meters)
# Ensure wearing course thickness (wcth) is set correctly
if wcth != 0.075:
    print(f"Warning: Expected wearing course thickness of 75 mm (0.075 m), but found {wcth} meters.")

# Convert the expansion joint thickness to meters (25 mm = 0.025 m)
expansion_joint_thickness = 25 / 1000  # 25 mm = 0.025 m

# Coordinates for the Wearing Course (continuous from left to right approach slabs)
wearing_course_start_x = hpos(abtl - expansion_joint_thickness - laslab)  # Left end of wearing course
wearing_course_end_x = hpos(abtl + (nspan * span1) + laslab + expansion_joint_thickness)  # Right end of wearing course

# Adjust the Y-coordinates based on the wearing course thickness (WCTH)
wearing_course_y1 = vpos(rtl)  # Top of the deck slab and approach slabs
wearing_course_y2 = vpos(rtl+wcth)   # Bottom of the wearing course (adjusted by WCTH)

# Print the Y-coordinates for debugging
print("Wearing Course Start X:", wearing_course_start_x)
print("Wearing Course End X:", wearing_course_end_x)
print("Wearing Course Y1:", wearing_course_y1)
print("Wearing Course Y2:", wearing_course_y2)

# Draw the continuous wearing course from left to right approach slabs
if wearing_course_start_x < wearing_course_end_x:
    msp.add_lwpolyline([[wearing_course_start_x, wearing_course_y1], [wearing_course_end_x, wearing_course_y1]], close=False)
    msp.add_lwpolyline([[wearing_course_start_x, wearing_course_y2], [wearing_course_end_x, wearing_course_y2]], close=False)
else:
    print("Invalid coordinates: Wearing course not drawn")
    
msp.add_line((wearing_course_start_x, wearing_course_y1), 
              (wearing_course_start_x, wearing_course_y2))

msp.add_line((wearing_course_start_x, wearing_course_y1), 
              (wearing_course_end_x, wearing_course_y1))

msp.add_line((wearing_course_end_x, wearing_course_y1), 
              (wearing_course_end_x, wearing_course_y2))
# END OF SECTION 5.3
###########################################################################################  
# pier caps in elevation
lspan = span1
nspan = int(nspan)  # Convert dynamically if it's not already an integer
#############################################
def generate_pier_caps(abtl, lspan, capw, c, capt, capb, nspan, hhs):   
    # Calculate x1 and x2 for the rectangle (cap width)
    lspan = span1
    x1 = abtl + lspan  # Starting position for the first span
    capwsq = capw / c  # Cap width adjusted by divisor
    x1 = x1 - (capwsq / 2)  # Adjust x1 for cap center alignment
    x2 = x1 + capwsq  # Calculate x2
    # Convert x1 and x2 to horizontal positions
    x1 = hpos(x1)
    x2 = hpos(x2)
    # Convert capt and capb to vertical positions
    y1 = vpos(capt)  # Top position of the cap
    y2 = vpos(capb)  # Bottom position of the cap
    # Define rectangle corners
    pta1 = (x1, y1)  # Top-left corner
    pta2 = (x2, y2)  # Bottom-right corner
    # Draw rectangle to represent the cap in elevation
    rect = msp.add_lwpolyline([
        (pta1[0], pta1[1]),
        (pta2[0], pta1[1]),
        (pta2[0], pta2[1]),
        (pta1[0], pta2[1])
    ], close=True)
    # Get the last entity (rectangle) for arraying
    g2 = rect
    # Create an array of spans
    for i in range(1,(nspan-1)):
        dx = i * lspan * hhs  # Horizontal offset for each span
        msp.add_lwpolyline([
            (pta1[0] + dx, pta1[1]),
            (pta2[0] + dx, pta1[1]),
            (pta2[0] + dx, pta2[1]),
            (pta1[0] + dx, pta2[1])
        ], close=True)
# Generate the pier caps
generate_pier_caps(abtl, lspan, capw, c, capt, capb, nspan, hhs)
#######################################################################################
# Drawing piers in elevation
# Start drawing piers Start drawing piers Start drawing piers Start drawing piers Start drawing piers Start drawing piers
# Start drawing pier caps
capwsb = capb / cos(radians(skew))
capwsq = capw / c  # Cap width adjusted by divisor
xc = spane
piertwsq = piertw / c ##### EARLIER IT WAS WRITTER AS pierstwsq = pierst
x1 = xc - piertwsq / 2 # left point of pier top
y1 = vpos(capt)
x3 = x1 + piertwsq      # right point of pier top
y2 = futrl + futd       #   pier bottom = footing RL + depth of foot
ofset = (capb - y2) / battr     # pier bw = ht/batter
from math import cos, radians
ofsetsq = ofset / cos(radians(skew))
x2 = x1 - ofsetsq
x4 = x3 + ofsetsq
y4 = y2
pta1 = [hpos(x1), vpos(capb)]
pta2 = [hpos(x2), vpos(y2)]
pta3 = [hpos(x3), vpos(capb)]
pta4 = [hpos(x4), vpos(y4)]
# draw first pier in elevation # Draw slant/ vertical lines to represent the  in elevation
msp.add_line(pta1, pta2)
msp.add_line(pta3, pta4)
ptaa1 = [hpos(x2) + 50, vpos(y2) - 300]

# Add a linear dimension
dim = msp.add_linear_dim(
    base=ptaa1,
    p1=pta2,
    p2=pta4,
    angle=0
)
dim.render()  # Render the dimension for display
# Draw rectangle to represent the cap in elevation
rect = msp.add_lwpolyline([
        pta2,
        pta1,
        pta3,
        pta4,
        pta2
    ], close=True)
    # Get the last entity (rectangle) for arraying
g2 = rect
    # Create an array of spans
for i in range(1, (nspan-1)):
        dx = i * lspan * hhs  # Horizontal offset for each span ###### RAJKUMAR THIS IS IMPORTANT
        msp.add_lwpolyline([
        (pta2[0] + dx, pta2[1]),
        (pta1[0] + dx, pta1[1]),
        (pta3[0] + dx, pta3[1]),
        (pta4[0] + dx, pta4[1])
        ], close=True)
# PIER IN ELEVATION COMPLETE ......SAME FOOTING LEVEL
#################################################
# 5.2 Start drawing footings in elevation
###################################################
def generate_pier_footings(futw, futd, futrl, nspan):   
    # Calculate x5 and x6 for the rectangle (footing width)
    from math import cos, radians
futwsq = futw / cos(radians(skew))
x5 = xc - futwsq / 2
x6 = x5 + futwsq
y6 = futrl
y5 = y4
pta5 = [hpos(x5), vpos(y5)]
pta6 = [hpos(x6), vpos(y6)]
# Convert x5 and x6 to horizontal positions
x5 = hpos(x5)
x6 = hpos(x6)
y5 = futrl
y6 = futd + futrl
    # Convert futrl and futd to vertical positions
y5 = vpos(y5)  # Top position of the footing
y6 = vpos(y6)  # Bottom position of the footing
    # Define rectangle corners
pta1 = (x5, y5)  # Top-left corner
pta2 = (x6, y6)  # Bottom-right corner
# Draw rectangle to represent the cap in elevation
rect = msp.add_lwpolyline([
        (pta1[0], pta1[1]),
        (pta2[0], pta1[1]),
        (pta2[0], pta2[1]),
        (pta1[0], pta2[1])
    ], close=True)
    # Get the last entity (rectangle) for arraying
g2 = rect
    # Create an array of spans
for i in range(1, (nspan-1)):
        dx = i * lspan * hhs  # Horizontal offset for each span
        msp.add_lwpolyline([
            (pta1[0] + dx, pta1[1]),
            (pta2[0] + dx, pta1[1]),
            (pta2[0] + dx, pta2[1]),
            (pta1[0] + dx, pta2[1])
        ], close=True)
# Generate the pier caps
generate_pier_footings(futw, futd, futrl, nspan)
##########################################################
# 5.5 drawing Piers in plan
###########################################################
def vpos(a):
    """Converts vertical position based on datum and scaling factor."""
    return datum + vvs * (a - datum)

def hpos(a):
    """Converts horizontal position based on left reference and scaling factor."""
    return left + hhs * (a - left)

def pt(a, b):
    """Converts given point (a, b) into a transformed graph point."""
    return (hpos(a), vpos(b))

x7 = xc - futw / 2 # left top point of footing ( as if  bridge is normal) footing will be drawn as if bridge is normal and then roteted
x8 = x7 + futw
yc = datum - 30.0
y7 = yc + futl / 2 # Right top point of footing
y8 = y7 - futl
######################################################################            
global pta7, pta8  # Access the global variable
pta7 = None  # Declare pt19 as a global variable

pta7 = pt(x7, y7) # Top-left ..
pta8 = pt(x8, y8) # Bottom-right.
# Calculate the other two points of the rectangle
pta7x = (pta7[0], pta8[1])  # Bottom -left ..... ADDITION BY RAJKUMAR
pta8x = (pta8[0], pta7[1])  # Top-right..... ADDITION BY RAJKUMAR
# Add the rectangle as a polyline
#############################################################################################
# Define functions for each line FOR FOOTING IN PLAN
def gr1(msp, dx):
    line = msp.add_line((pta7[0], pta7[1]), (pta8x[0], pta8x[1]))
    return line
def gr2(msp, dx):
    line = msp.add_line((pta8x[0], pta8x[1]), (pta8[0], pta8[1]))
    return line
def gr3(msp, dx):
    line = msp.add_line((pta8[0], pta8[1]), (pta7x[0], pta7x[1]))
    return line
def gr4(msp, dx):
    line = msp.add_line((pta7x[0], pta7x[1]), (pta7[0], pta7[1]))
    return line
# Array of drawing functions (lines)
drawing_functions = [gr1, gr2, gr3, gr4]
# Loop to draw elements for each span
for i in range(1, nspan):
    dx = i * lspan * hhs
    for draw_func in drawing_functions:
        draw_func(msp, dx)
###################################################################
pt1 = [hpos(x7), vpos(y8)]  # FOOTING PLAN LEFT BOTTOM CORNER
pt2 = pta8                  # FOOTING PLAN LEFT BOTTOM CORNER
pt3 = [hpos(x7) + 100, vpos(y8) - 600]
dimstyle = doc.dimstyles.get('Standard')  # Get the default dimension style
dimstyle.dxf.dimexe = 200  # Set extension line extension
dimstyle.dxf.dimexo = 400  # Set extension line offset
##########RAJKUMAR SHORT***************************
# Add a horizontal linear DIMENSION entity:
dim = msp.add_linear_dim(
    base = pt1, # location of the dimension line
    p1 = pt2,  # 1st measurement point
    p2 = pt3,  # 2nd measurement point
    dimstyle="EZDXF",  # default dimension style
)
dim.render()
msp.add_linear_dim(base = pt1, p1 = pt2, p2 = pt3, angle= 0).render()
g3 = dim
##########RAJKUMAR SHORT***************************   
pt1 = [hpos(x8), vpos(y7)]  
pt2 = pta8  
pt3 = [hpos(x8) + 700, vpos(y7) - 100]  
##########RAJKUMAR SHORT***************************
# Add a horizontal linear DIMENSION entity:
dim = msp.add_linear_dim(
    base = pt1, # location of the dimension line
    p1=pt2,  # 1st measurement point
    p2=pt3,  # 2nd measurement point
    dimstyle="EZDXF",  # default dimension style
)
dim.render()
msp.add_linear_dim(base = pt1, p1 = pt2, p2 = pt3, angle= 0).render()
g4 = dim
##########RAJKUMAR SHORT*************************** 
ptc = pt(xc, yc)
from math import radians, cos, sin
# Function to rotate points around a given center
def rotate_point(x, y, cx, cy, angle):
    angle = radians(angle)
    x_new = (x - cx) * cos(angle) - (y - cy) * sin(angle) + cx
    y_new = (x - cx) * sin(angle) + (y - cy) * cos(angle) + cy
    return x_new, y_new

# Calculate pier st length in skew
pierstsq = (pierst / c) + abs(piertw * tn)

# Compute pier top and bottom points
x1 = (xc - (piertw / 2)) # ; left point of pier top ( as if  bridge is normal) pier
x3 = (x1 + piertw) # right point of pier top ( as if  bridge is normal)
x2 = (x1 - ofset) # left point of pier bottom( as if  bridge is normal)
x4 = (x3 + ofset) # right point of pier bottom ( as if  bridge is normal)
y9 = (yc + (pierstsq / 2))
y10 = (y9 - pierstsq)
# Define points

pta9 = pt(x2, y9)  # LEFT TOP PIER POINT (DENOTING BOTTOM WIDTH IN PLAN)
pta10 = pt(x2, y10)  # LEFT BOTTOM PIER POINT (DENOTING BOTTOM WIDTH IN PLAN)
pta11 = pt(x1, y9) # RIGHT TOP PIER POINT (DENOTING BOTTOM WIDTH IN PLAN)
pta12 = pt(x1, y10) # RIGHT BOTTOM PIER POINT (DENOTING BOTTOM WIDTH IN PLAN)

pta13 = pt(x3, y9)
pta14 = pt(x3, y10)
pta15 = pt(x4, y9)
pta16 = pt(x4, y10)


msp.add_line(pta9, pta10)
msp.add_line(pta11, pta12)

msp.add_line(pta13, pta14)
msp.add_line(pta15, pta16)

# Draw pier lines
g1 = msp.add_line(pta9, pta10)
g2 = msp.add_line(pta11, pta12)
g3 = msp.add_line(pta13, pta14)
g4 = msp.add_line(pta15, pta16)

# Compute additional points
y17 = y9 + (piertw / 2)
y18 = y9 - ofset
y19 = y10 - (piertw / 2)
y20 = y19 - ofset

pta17 = pt(xc, y17)
pta18 = pt(xc, y18)
pta19 = pt(xc, y19)
pta20 = pt(xc, y20)
##############################################################################################
# Generate the FOOTING pier in plan
x17 = xc - piertw / 2
x18 = x17 + piertw
yc = datum - 30.0
y17 = yc + pierst / 2
y18 = y17 - pierst
pta17a = [hpos(x17), vpos(y17)] # PIER LEFT TOP CORNER IN PLAN
pta17b = [hpos(x17 + piertw), vpos(y17)] # PIER RIGHT TOP CORNER IN PLAN

pta18a = [hpos(x18 - piertw), vpos(y18)] # PIER LEFT BOTTOM CORNER IN PLAN
pta18b = [hpos(x18), vpos(y18)] # PIER RIGHT BOTTOM CORNER IN PLAN

msp.add_line(pta17a, pta18a) # PIER LEFT LINE
msp.add_line(pta17b, pta18b) # PIER RIGHT LINE

# Define points pt1, pt2, pt3 for the first section

pt1a = (hpos(x7), vpos(y8 + futl))  # PIER-FOOTING LEFT top CORNER IN PLAN
pt2a = [hpos(x7 + futw) , pt1a[1]]               # PIER-FOOTING RIGHT top CORNER IN PLAN
pt1b = (hpos(x7), vpos(y8))  # PIER-FOOTING LEFT BOTTOM CORNER IN PLAN
pt2b = [pt2a[0]  , pt1b[1]]              # PIER-FOOTING RIGHT BOTTOM CORNER IN PLAN
msp.add_lwpolyline([pt1a, pt1b, pt2b, pt2a, pt1a]) # pier footing
#########################################################################################
import math

###############################################################################################################
def g5(msp, dx):    
    # Calculate the center and radius for the arc
    center_x = (pta9[0] + dx + pta15[0] + dx) / 2
    center_y = (pta9[1] + pta15[1]) / 2
    center = (center_x, center_y)
    
    radius = sqrt((pta15[0] - pta9[0]) ** 2 + (pta15[1] - pta9[1]) ** 2) / 2
    
    start_angle = atan2(pta9[1] - center_y, pta9[0] + dx - center_x) * 180 / pi
    end_angle = atan2(pta15[1] - center_y, pta15[0] + dx - center_x) * 180 / pi
    
    if start_angle > end_angle:
        start_angle, end_angle = end_angle, start_angle

    # Add the arc to the DXF drawing
    msp.add_arc(center, radius, start_angle, end_angle)
#####################################

#####################################
def g6(msp, dx):
    # Calculate the center and radius for the arc
    center_x = (pta11[0] + dx + pta13[0] + dx) / 2
    center_y = (pta11[1] + pta13[1]) / 2
    center = (center_x, center_y)
    
    radius = sqrt((pta13[0] - pta11[0]) ** 2 + (pta13[1] - pta11[1]) ** 2) / 2
    
    start_angle = atan2(pta11[1] - center_y, pta11[0] + dx - center_x) * 180 / pi
    end_angle = atan2(pta13[1] - center_y, pta13[0] + dx - center_x) * 180 / pi
    
    if start_angle > end_angle:
        start_angle, end_angle = end_angle, start_angle
    
    arc = msp.add_arc(center, radius, start_angle, end_angle)
    return arc

def g7(msp, dx):
    # Calculate the center and radius for the arc
    center_x = (pta12[0] + dx + pta14[0] + dx) / 2
    center_y = (pta12[1] + pta14[1]) / 2
    center = (center_x, center_y)
    
    radius = sqrt((pta14[0] - pta12[0]) ** 2 + (pta14[1] - pta12[1]) ** 2) / 2
    
    start_angle = atan2(pta12[1] - center_y, pta12[0] + dx - center_x) * 180 / pi
    end_angle = atan2(pta14[1] - center_y, pta14[0] + dx - center_x) * 180 / pi
    
    if start_angle < end_angle:
        start_angle, end_angle = end_angle, start_angle
    
    arc = msp.add_arc(center, radius, start_angle, end_angle)
    return arc
# Arc 4 (g8)
def g8(msp, dx):
    # Calculate the center and radius for the arc
    center_x = (pta10[0] + dx + pta16[0] + dx) / 2
    center_y = (pta10[1] + pta16[1]) / 2
    center = (center_x, center_y)
    
    radius = sqrt((pta16[0] - pta10[0]) ** 2 + (pta16[1] - pta10[1]) ** 2) / 2
    
    start_angle = atan2(pta10[1] - center_y, pta10[0] + dx - center_x) * 180 / pi
    end_angle = atan2(pta16[1] - center_y, pta16[0] + dx - center_x) * 180 / pi
    
    if start_angle < end_angle:
        start_angle, end_angle = end_angle, start_angle
    
    arc = msp.add_arc(center, radius, start_angle, end_angle)
    return arc

# Array of drawing functions (arcs)
arc_functions = [g5, g6, g7, g8]

# Loop to draw elements for each span
for i in range(nspan-1):
    dx = i * lspan * hhs
    for arc_func in arc_functions:
        print(f"Drawing arc with function {arc_func.__name__}")
        arc = arc_func(msp, dx)
        
##############################################################################

#######################################################################################################################
####### ARRAY FOR ALL SPANS PLAN OF PIER AND FOOTING #################################################################
# Array of drawing functions (G1 to G8)
# Define each drawing function (g1 to g8) using msp (model space) and dx (horizontal offset)
# Loop to draw elements for each span
for i in range(nspan-1):
    dx = i * lspan * hhs
    for draw_func in drawing_functions:
        draw_func(msp, dx)
def gr1(msp, dx):
    gr1 = msp.add_line((pta7[0] + dx, pta7[1]), (pta8x[0] + dx, pta8x[1]))
    return gr1

def gr2(msp, dx):
    gr2 = msp.add_line((pta8x[0] + dx, pta8x[1]), (pta8[0] + dx, pta8[1]))
    return gr2

def gr3(msp, dx):
    gr3 = msp.add_line((pta8[0] + dx, pta8[1]), (pta7x[0] + dx, pta7x[1]))
    return gr3

def gr4(msp, dx):
    gr4 = msp.add_line((pta7x[0] + dx, pta7x[1]), (pta7[0] + dx, pta7[1]))
    return gr4
        
def g1(msp, dx):
    rectg1 = msp.add_line((pta9[0] + dx, pta9[1]), (pta10[0] + dx, pta10[1]))
    return g1
# g2: Line (example)
def g2(msp, dx):
    g2 = msp.add_line((pta11[0] + dx, pta11[1]), (pta12[0] + dx, pta12[1]))
    return g2
# g3: Line (example)
def g3(msp, dx):
    g3 = msp.add_line((pta13[0] + dx, pta13[1]), (pta14[0] + dx, pta14[1]))
    return g3
# g4: Line (example)
def g4(msp, dx):
    g4 = msp.add_line((pta15[0] + dx, pta15[1]), (pta16[0] + dx, pta16[1]))
    return g4

# Define the function for each arc
def draw_arc(msp, pta_start, pta_end, dx):
    # Calculate center and radius for the arc
    center = ((pta_start[0] + pta_end[0]) / 2 + dx, (pta_start[1] + pta_end[1]) / 2)
    radius = sqrt((pta_end[0] - pta_start[0]) ** 2 + (pta_end[1] - pta_start[1]) ** 2) / 2
    
    # Compute angles for counterclockwise semicircle
    start_angle = atan2(pta_start[1] - center[1], pta_start[0] - center[0]) * 180 / pi
    end_angle = atan2(pta_end[1] - center[1], pta_end[0] - center[0]) * 180 / pi
    
    # Ensure correct counterclockwise order
    if start_angle > end_angle:
        start_angle, end_angle = end_angle, start_angle
    
    # Add the arc to the DXF drawing
    arc = msp.add_arc(center, radius, start_angle, end_angle)
    return arc
###############################################################################################################

    


# Array of drawing functions (arcs)
arc_functions = [g5, g6, g7, g8]
# Array of drawing functions (g1 to g8)
drawing_functions = [g1, g2, g3, g4, gr1, gr2, gr3, gr4, g5, g6, g7, g8]
# Loop to draw elements for each span
for i in range(1, nspan):  # Looping through spans, nspan - 1 intervals
    dx = (i - 1) * lspan * hhs  # Calculate the horizontal offset for the current span
    # Loop through each drawing function in the array and draw the element
    for draw_func in drawing_functions:
        draw_func(msp, dx)

####################################################################

#########################################################################################################################
# 5.5  drawing SS of last span
# Last span drawing
x1 = hpos(spane)
y1 = vpos(rtl)
x2 = hpos(abtl + lbridge)
y2 = vpos(sofl)
pta1 = (x1 + 25.0, y1)
pta2 = (x2 - 25.0, y2)
# Draw last span rectangle
msp.add_lwpolyline([pta1, (pta1[0], pta2[1]), pta2, (pta2[0], pta1[1]), pta1]) #completed drwing  reactangle to represent SS last span
x4 = (x1 * 2)
pta1 = (x1, y1)
pta2 = (x4, y1)
# Add dimension for last span
ptaa1 = (x1 + span1 /2, y1 + 200)

### SPAN DIMENSION SHOWING BELOW
# Add a linear dimension
dim = msp.add_linear_dim(
    base=ptaa1,
    p1=pta1,
    p2=pta2,
    angle=0,    
)
dim.render()  # Render the dimension for display
    # Create an array of spans
for i in range(1, (nspan-1)):
        dx = i * lspan * hhs  # Horizontal offset for each span
        msp.add_lwpolyline([
            (pta1[0] + dx, pta1[1]),
            (pta2[0] + dx, pta1[1]),
            (pta2[0] + dx, pta2[1]),
            (pta1[0] + dx, pta2[1])
        ], close=True)
# Super Structure in Elevation complete.
###########################################################




####################################################################################################################################

#########################################################################################################################################
#5.6  NOW DRAWiNG ELEVATION AND SECTION YY OF PIER IN DOUBLE OR SCALE1/SCALE2 SCALE. ; 
#SIDE VIEW MODIFIED FOR HPOS VPOS BY RAJKUMAR 
##### offset_x = 45000 - xp  # MENTIONED AT RELEVANT PLACE
#### offset_y = 90000 - yp  # MENTIONED AT RELEVANT PLACE
##########################################################################
##### ADD OFFSET SIDE ELEVATION
# Define the translation offset
rtl2 = rtl - (30 * sc) #this the level used as RTL in  drawing section. i.e. dist btween datum level and sections top on paper is 15m
xp = left + span1 * nspan
yp = rtl2
r = 2 * span1 * nspan * scale1
offset_x = r - xp  # Adjust this based on your reference point
offset_y =  r - yp  # Adjust this based on your reference point
#########################################################################
import pandas as pd
def get_value(df, variable_name):
    return df.loc[df['Variable'] == variable_name, 'Value'].values[0]
# Retrieve specific variables
capw = get_value(df, 'CAPW')
ccbr = get_value(df, 'CCBR')
kerbw = get_value(df, 'KERBW')
lbridge = get_value(df, 'LBRIDGE')
nspan = get_value(df, 'NSPAN')
span1 = get_value(df, 'SPAN1')
slbthe = get_value(df, 'SLBTHE')
slbtht = get_value(df, 'SLBTHT')
kerbd = get_value(df, 'KERBD')
# Print values for validation
print(f"CAPW: {capw}, CCBR: {ccbr}, KERBW: {kerbw}, LBRIDGE: {lbridge}, NSPAN: {nspan}, SPAN1: {span1}, SLABTHE: {slbthe}, SLABTHT: {slbtht}")  
import math
def vpos(a):
    return datum + vvs * (a - datum)   
def hpos(a):
    return left + hhs * (a - left)
# Define the pt function
def pt(a, b, z):
    
    # Convert x-coordinate to graph position
    aa = hpos(a)

    # Convert y-coordinate to graph position
    bb = vpos(b)

    # Create a list with the converted x and y coordinates
    z = [aa, bb]

    return z  # Return the converted point

# Define values for a, b, and z
#xd = left + span1 * nspan
#yd = rtl
#pta1 =(xd, yd)
pta1 = (100,0)
nn1 = pta1
# Assign nn1 values to a and b
a = nn1[0]  # First element of nn1
b = nn1[1]  # Second element of nn1
z = None  # Placeholder for the result
# Call the pt function with valid arguments
z = pt(a, b, z)
pta1 = pt(nn1[0], nn1[1], pta1)
#########################################################
def p2t(a, b, z):
    
    # Set aa to the value of a
    aa = a

    # Convert x-coordinate to graph position using h2pos
    aa = h2pos(aa)

    # Set bb to the value of b
    bb = b

    # Convert y-coordinate to graph position using v2pos
    bb = v2pos(bb)

    # Create a list with the converted x and y coordinates
    z = [aa, bb]

    return z  # Return the converted point
# End of p2t function
pta2 = None  # Placeholder for the resulting converted point
pta2 = p2t(nn1[0], nn1[1], pta2)
# Output the result
print(f"Converted point: {pta2}")  # Output: Converted point: [converted_x, converted_y]
###################################################
# pta1 is last span deck slab point 
ptnn1 = pta1 ############## very imprortant

pta1 = (0,0)
ptnn1 = pta1 ############## very imprortant
pta1 = pt(nn1[0], nn1[1], pta1)                     #(setq pta1 (pt (car nn1) (cadr nn1) pta1))
rtl2 = rtl - (30 * sc) #this the level used as RTL in  drawing section. i.e. dist btween datum level and sections top on paper is 15m
# xp and yp are defined above ##
ccbrsq = ccbr / c
xp1 = xp + ccbrsq / 2
yp1 = yp
ppt1 = (xp1, yp1)
ppt1 = p2t(xp1, yp1, ppt1)
xp2 = xp + ccbrsq
yp2 = yp
ppt2 = [xp2, yp2]
ppt2 = p2t(xp2, yp2, ppt2)
kerbwsq = kerbw / c

xp3 = xp + ccbrsq + kerbwsq
yp3 = yp + slbthe - slbtht
ppt3 = (xp3, yp3)
ppt3 = p2t(xp3, yp3, ppt3)

xp4 = xp + ccbrsq + kerbwsq
yp4 = yp + slbthe
ppt4 = (xp4, yp4)
ppt4 = p2t(xp4, yp4, ppt4)

xp5 = xp + ccbrsq + kerbwsq
yp5 = yp + slbthe + kerbd
ppt5 = (xp5, yp5)
ppt5 = p2t(xp5, yp5, ppt5)

k1 = 0.05 /c  #####50 and 25 mm dist is converted  into skew direction
k2 = 0.025 / c

xp6 = xp + ccbrsq + k1
yp6 = yp + slbthe + kerbd
ppt6 = (xp6, yp6)
ppt6 = p2t(xp6, yp6, ppt6)

xp7 = xp + ccbrsq + k2
yp7 = yp + slbthe + kerbd - 0.025
ppt7 = (xp7, yp7)
ppt7 = p2t(xp7, yp7, ppt7)

xp8 = xp + ccbrsq
yp8 = yp + slbthe
ppt8 = (xp8, yp8)
ppt8 = p2t(xp8, yp8, ppt8)

xp9 = xp + ccbrsq / 2
yp9 = yp + slbthe
ppt9 = (xp9, yp9)
ppt9 = p2t(xp9, yp9, ppt9)

xp10 = xp
yp10 = yp + slbthe
ppt10 = (xp10, yp10)
ppt10 = p2t(xp10, yp10, ppt10)

xp11 = xp - k2
yp11 = yp + slbthe + kerbd - 0.025
ppt11 = (xp11, yp11)
ppt11 = p2t(xp11, yp11, ppt11)

xp12 = xp - k1
yp12 = yp + slbthe + kerbd
ppt12 = (xp12, yp12)
ppt12 = p2t(xp12, yp12, ppt12)

xp13 = xp - kerbwsq
yp13 = yp + slbthe + kerbd
ppt13 = (xp13, yp13)
ppt13 = p2t(xp13, yp13, ppt13)

ppt14 = (ppt13[0], ppt4[1]) # NO p2t function required for ppt 14 and 15. PLEASE NOTE
ppt15 = (ppt13[0], ppt3[1])
#########################################################

diff = (pierstsq - ccbrsq) 
diff = diff / 2
xp = xp - diff
pedstl = sofl - capt
yp = yp - pedstl
xp16 = xp
yp16 = yp
ppt16 = (xp16, yp16)
ppt16 = p2t(xp16, yp16, ppt16)

capd = capt - capb
xp17 = xp - capw / 2
yp17 = yp
ppt17 = (xp17, yp17)
ppt17 = p2t(xp17, yp17, ppt17)

xp18 = xp + pierstsq + capw / 2
yp18 = yp
ppt18 = (xp18, yp18)
ppt18 = p2t(xp18, yp18, ppt18)

xp19 = xp - capw / 2
yp19 = yp - capd
ppt19 = (xp19, yp19)
ppt19 = p2t(xp19, yp19, ppt19)

xp20 = xp + pierstsq + capw / 2
yp20 = yp - capd
ppt20 = (xp20, yp20)
ppt20 = p2t(xp20, yp20, ppt20)
######################################################

xp21 = xp - piertw / 2
yp21 = yp - capd
ppt21 = (xp21, yp21)
ppt21 = p2t(xp21, yp21, ppt21)

xp22 = xp
yp22 = yp - capd
ppt22 = (xp22, yp22)
ppt22 = p2t(xp22, yp22, ppt22)

xp23 = xp + pierstsq
yp23 = yp - capd
ppt23 = (xp23, yp23)
ppt23 = p2t(xp23, yp23, ppt23)

xp24 = xp + pierstsq + piertw / 2
yp24 = yp - capd
ppt24 = (xp24, yp24)
ppt24 = p2t(xp24, yp24, ppt24)

xpc = xp + pierstsq / 2
pierht = capb - futrl - futd
pierbw = pierht / battr
pierbw += pierbw + piertw
h1 = yp - pierht + capd

xpc25 = xpc - futl / 2
h125 = h1
ppt25 = (xpc25, h125)
ppt25 = p2t(xpc25, h125, ppt25)

xp26 = xp - pierbw / 2
h126 = h1
ppt26 = (xp26, h126)
ppt26 = p2t(xp26, h126, ppt26)

xp27 = xp
h127 = h1
ppt27 = (xp27, h127)
ppt27 = p2t(xp27, h127, ppt27)

xp28 = xp + pierstsq
h128 = h1
ppt28 = (xp28, h128)
ppt28 = p2t(xp28, h128, ppt28)

xp29 = xp + pierstsq + pierbw / 2
h129 = h1
ppt29 = (xp29, h129)
ppt29 = p2t(xp29, h129, ppt29)

xpc30 = xpc + futl / 2
h130 = h1
ppt30 = (xpc30, h130)
ppt30 = p2t(xpc30, h130, ppt30)



h2 = h1 - futd
xpc31 = xpc - futl / 2
h231 = h2
ppt31 = (xpc31, h231)
ppt31 = p2t(xpc31, h231, ppt31)

xpc32 = xpc
h232 = h2
ppt32 = (xpc32, h232)
ppt32 = p2t(xpc32, h232, ppt32)

xpc33 = xpc + futl / 2
h233 = h2
ppt33 = (xpc33, h233)
ppt33 = p2t(xpc33, h233, ppt33)

xp2 = xp + ccbrsq + diff + diff
yp2 = yp
ppt2 = (xp2, yp2)
ppt2 = p2t(xp2, yp2, ppt2) # NO p2t function required for ppt2 AGAIN. PLEASE NOTE

#########################################################
# Adjust all points by the offset
def translate_point(point, offset_x, offset_y):
    return (point[0] + offset_x, point[1] + offset_y)
# Translate points
ppt1 = translate_point(ppt1, offset_x, offset_y)
ppt2 = translate_point(ppt2, offset_x, offset_y)
ppt3 = translate_point(ppt3, offset_x, offset_y)
ppt4 = translate_point(ppt4, offset_x, offset_y)
ppt5 = translate_point(ppt5, offset_x, offset_y)
ppt6 = translate_point(ppt6, offset_x, offset_y)
ppt7 = translate_point(ppt7, offset_x, offset_y)
ppt8 = translate_point(ppt8, offset_x, offset_y)
ppt9 = translate_point(ppt9, offset_x, offset_y)
ppt10 = translate_point(ppt10, offset_x, offset_y)
ppt11 = translate_point(ppt11, offset_x, offset_y)
ppt12 = translate_point(ppt12, offset_x, offset_y)
ppt13 = translate_point(ppt13, offset_x, offset_y)
ppt14 = translate_point(ppt14, offset_x, offset_y)
ppt15 = translate_point(ppt15, offset_x, offset_y)
ppt16 = translate_point(ppt16, offset_x, offset_y)
# Drawing kerb and carriage way in cross section
# DRAWING KERB AND CARRIAGE WAY IN CROSS SECTION
msp.add_lwpolyline([ppt16, ppt1, ppt2, ppt3, ppt4, ppt5, ppt6, ppt7, ppt8, ppt9, ppt10, ppt11, ppt12, ppt13, ppt14, ppt15, ppt16], close=True)
msp.add_line(ppt14, ppt10)
msp.add_line(ppt8, ppt4)

ppt17 = translate_point(ppt17, offset_x, offset_y)
ppt18 = translate_point(ppt18, offset_x, offset_y)
ppt19 = translate_point(ppt19, offset_x, offset_y)
ppt20 = translate_point(ppt20, offset_x, offset_y)
ppt21 = translate_point(ppt21, offset_x, offset_y)
ppt22 = translate_point(ppt22, offset_x, offset_y)
ppt23 = translate_point(ppt23, offset_x, offset_y)
ppt24 = translate_point(ppt24, offset_x, offset_y)
ppt25 = translate_point(ppt25, offset_x, offset_y)
ppt26 = translate_point(ppt26, offset_x, offset_y)
ppt27 = translate_point(ppt27, offset_x, offset_y)
ppt28 = translate_point(ppt28, offset_x, offset_y)
ppt29 = translate_point(ppt29, offset_x, offset_y)
ppt30 = translate_point(ppt30, offset_x, offset_y)
ppt31 = translate_point(ppt31, offset_x, offset_y)
ppt32 = translate_point(ppt32, offset_x, offset_y)
ppt33 = translate_point(ppt33, offset_x, offset_y)

msp.add_lwpolyline([ppt17, ppt18, ppt20, ppt19, ppt17], close=True)
# LEFT AND RIGHT LINES OF PIER ARE AS BELOW ..... rajkumar debugs
# DRAWING PIER SIDE ELEVATION (SUB-STRUCTURE PART)
msp.add_line(ppt21, ppt26)
msp.add_line(ppt16, ppt27)
msp.add_line(ppt2, ppt28)
msp.add_line(ppt24, ppt29)
msp.add_lwpolyline([ppt25, ppt30, ppt33, ppt31, ppt25], close=True)
msp.add_line(ppt9, ppt32)
msp.add_line(ppt26, ppt29) ## RAJKUMAR TRIAL ERROR - bottom close.
###################################################################################################
import math
# Define the position functions
def vpos(a):
    return datum + vvs * (a - datum)
def hpos(a, left):  # Add 'left' as a parameter
    return left + hhs * (a - left)
def v2pos(a):
    return datum + sc * vvs * (a - datum)
def h2pos(a):
    return left + sc * hhs * (a - left)
#################################################
# Abutment drawing calculation
def abt1(datum, vvs, left, hhs, sc):
    # Input values
    # Calculations
    abtlen = ccbrsq + kerbwsq + kerbwsq
    x1 = abtl
    alcwsq = alcw / 1   # c changed to 1 
    x3 = x1 + alcwsq
    capb = capt - alcd
    p1 = (capb - alfbl) / alfb
    p1sq = p1 / 1        # c changed to 1 
    x5 = x3 + p1sq
    p2 = (alfbl - altbl) / altb
    p2sq = p2 / 1            # c changed to 1 
    x6 = x5 + p2sq
    alfosq = alfo / 1    # c changed to 1 
    x7 = x6 + alfosq
    y8 = altbl - alfd
    dwthsq = dwth / 1    # c changed to 1
    x14 = x1 - dwthsq
    p3 = (capb - albbl) / albb
    p3sq = p3 / 1        # c changed to 1
    x12 = x14 - p3sq
    rt1s = x12            #chainage where left return starts in elevation
    x10 = x12 - alfosq
    # 6.3 gives various points on elevation of abutment
    # Adjust positions using hpos and vpos functions
    print("x1:", x1)
    pt1 = (hpos(x1, left), vpos(rtl+ apthk - slbtht)) 
    pt2 = (hpos(x1, left), vpos(capt))
    pt3 = (hpos(x3, left), vpos(capt))
    pt4 = (hpos(x3, left), vpos(capb))
    pt5 = (hpos(x5, left), vpos(alfbl))
    pt6 = (hpos(x6, left), vpos(altbl))
    pt7 = (hpos(x7, left), vpos(altbl))
    pt8 = (hpos(x7, left), vpos(y8))
    pt9 = (hpos(x10, left), vpos(y8))
    pt10 = (hpos(x10, left), vpos(altbl))
    pt11 = (hpos(x12, left), vpos(altbl))
    pt12 = (hpos(x12, left), vpos(albbl))
    pt13 = (hpos(x14, left), vpos(capb))
    pt14 = (hpos(x14, left), vpos(rtl+ apthk - slbtht)) 
    pt15 = (hpos(x12, left), vpos(rtl+ apthk - slbtht)) 
# Print coordinates of PT1 and PT2
    print(f"Coordinates of PT1: {pt1}")
    print(f"Coordinates of PT2: {pt2}") 
    # Draw the abutment
    msp.add_lwpolyline([pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8, pt9, pt10, pt11, pt12, pt13, pt14, pt1], close=True)
    msp.add_line(pt13, pt4)
    msp.add_line(pt10, pt7)
    # note this is VERTICAL LINE EXTREME LEFT DENOTING RETURN WALL EXTENT
    msp.add_line(pt12, pt15)  # Corrected line addition PT12 IS LOWER POINT PT15 IS UPPER ****** by rajkumar ******
    msp.add_line(pt15, pt14)  # Corrected line addition # PT1 IS DIRT WALL EDGE ON RIVER SIDE ****** by rajkumar ******
#####################################################################
    # 6.4 ; drawing abutment left in plan
    print(pt1, pt2, pt3, pt4, "line1")
    print(pt4, pt6, pt7, pt8, "line5")
    print(pt9, pt10, pt11, pt12, "line9")

    
    yc = datum - 30.0
    y20 = yc + (abtlen / 2)   # gives Y ordinate on D/S of abt 
    y21 = y20 - abtlen          # gives y ordinate on u/s of abt 
    y16 = y20 + 0.15            #  gives Y ordinate on D/S of footing 
    y17 = y21 - 0.15            #  gives Y ordinate on U/S of footing 
    # Footing calculations
    footl = (y16 - y17)
    footl = footl / 2       #  EARLIER IGNORED
    x = footl * s
    y = footl * (1 - c)
    # Define points for abutment footing in plan
    pt16 = (hpos(x10 - x, left), vpos(y16) - y)
    pt17 = (hpos(x10 + x, left), vpos(y17) + y)
    pt18 = (hpos(x7 - x, left), vpos(y16) - y)
    pt19 = (hpos(x7 + x, left), vpos(y17) + y)
    ################################################################

    ################################################################
    # Draw abutment footing in plan
    msp.add_lwpolyline([pt16, pt17, pt19, pt18, pt16], close=True) 
    # Skew adjustments for other points
    xx = abtlen / 2 # due to skew, the X and Y ordinates of any point are shifted 
    x = xx * s
    y = xx * (1 - c)
    print(x, "raj")
    print(y, "raj")
    print(s, c, "raj")
    y20 = y20 - y
    y21 = y21 + y
    pt20 = (hpos(x12 - x, left), vpos(y20))
    pt21 = (hpos(x12 + x, left), vpos(y21))
    pt22 = (hpos(x14 - x, left), vpos(y20))
    pt23 = (hpos(x14 + x, left), vpos(y21))     
    pt24 = (hpos(x1 - x, left), vpos(y20))  # Point 24
    pt25 = (hpos(x1 + x, left), vpos(y21))  # Point 25
    pt26 = (hpos(x3 - x, left), vpos(y20))  # Point 26
    pt27 = (hpos(x3 + x, left), vpos(y21))  # Point 27
    pt28 = (hpos(x5 - x, left), vpos(y20))  # Point 28
    pt29 = (hpos(x5 + x, left), vpos(y21))  # Point 29
    pt30 = (hpos(x6 - x, left), vpos(y20))  # Point 30
    pt31 = (hpos(x6 + x, left), vpos(y21))  # Point 31
    print(pt13, pt14, pt15, pt16, "line13")
    print(pt17, pt18, pt19, pt20, "line17")
    print(pt21, pt22, pt23, pt24, "line21")
    print(pt25, pt26, pt27, pt28, "line25")
    print(pt29, pt30, pt31, "line29")   
    # Final lines to connect the points
    # Add lines using the MSP (Model Space) object from ezdxf
    msp.add_line(pt20, pt21)  # Line from pt20 to pt21
    msp.add_line(pt22, pt23)  # Line from pt22 to pt23
    msp.add_line(pt24, pt25)  # Line from pt24 to pt25
    msp.add_line(pt26, pt27)  # Line from pt26 to pt27
    msp.add_line(pt28, pt29)  # Line from pt28 to pt29
    msp.add_line(pt30, pt31)  # Line from pt30 to pt31
    msp.add_line(pt21, pt31)  # Line from pt21 to pt31
    msp.add_line(pt20, pt30)  # Line from pt20 to pt30
# completed drawing plan abutment left
    
abt1(datum, vvs, left, hhs, sc)
########################################################################################################
# ABUTMENT RIGHT
########################################################################################################
def abt2(datum, vvs, left, hhs, sc, alcwr):  
    # Calculate points for the right abutment
    abtlen = ccbrsq + kerbwsq + kerbwsq   
    x1 = abtl
    alcwsq = alcw / 1  # c changed to 1 
    x3 = x1 + alcwsq
    capb = capt - alcd
    yc = datum - 30.0
    p1 = (capb - alfbr) / alfb 
    p1sq = p1 / 1  # c changed to 1 
    x5 = x3 + p1sq
    p2 = (alfbr - altbr) / altb
    p2sq = p2 / 1  # c changed to 1 
    x6 = x5 + p2sq
    alfosq = alfo / 1  # c changed to 1 
    x7 = x6 + alfosq
    y8 = altbr - alfd
    dwthsq = dwth / 1  # c changed to 1
    x14 = x1 - dwthsq
    p3 = (capb - albbr) / albb
    p3sq = p3 / 1  # c changed to 1 
    x12 = x14 - p3sq
    rt1s = x12  # chainage where left return starts in elevation
    x10 = x12 - alfosq
    right_edge = left + lbridge
# Debugging statements
    print(f"Left abutment position: {left}")
    print(f"Bridge length (LBRIDGE): {lbridge}")
    print(f"Right abutment edge: {right_edge}")
    # Adjust positions using hpos and vpos functions
    # Note: We need to calculate the 'right' position 
    # by subtracting the distance from the 'right' edge of the bridge 
    pt1 = (hpos(right_edge - x1, left), vpos(rtl+ apthk - slbtht)) 
    pt2 = (hpos(right_edge - x1, left), vpos(capt))
    pt3 = (hpos(right_edge - x3, left), vpos(capt))
    pt4 = (hpos(right_edge - x3, left), vpos(capb))
    pt5 = (hpos(right_edge - x5, left), vpos(alfbr)) 
    pt6 = (hpos(right_edge - x6, left), vpos(altbr)) 
    pt7 = (hpos(right_edge - x7, left), vpos(altbr)) 
    pt8 = (hpos(right_edge - x7, left), vpos(y8)) 
    pt9 = (hpos(right_edge - x10, left), vpos(y8)) 
    pt10 = (hpos(right_edge - x10, left), vpos(altbr)) 
    pt11 = (hpos(right_edge - x12, left), vpos(altbr)) 
    pt12 = (hpos(right_edge - x12, left), vpos(albbr)) 
    pt13 = (hpos(right_edge - x14, left), vpos(capb)) 
    pt14 = (hpos(right_edge - x14, left), vpos(rtl+ apthk - slbtht)) 
    pt15 = (hpos(right_edge - x12, left), vpos(rtl+ apthk - slbtht)) 
    ptplan1 = pt9
    #ptplan1 = computed_value["ptplan1"]
    
# Draw the abutment
    msp.add_lwpolyline([pt1, pt2, pt3, pt4, pt5, pt6, pt7, pt8, pt9, pt10, pt11, pt12, pt13, pt14, pt1], close=True)
    msp.add_line(pt13, pt4)
    msp.add_line(pt10, pt7)
    # Fix the add_line to pass two points, not three 
    # note this is VERTICAL LINE EXTREME LEFT DENOTING RETURN WALL EXTENT
    msp.add_line(pt12, pt15)  # Corrected line addition PT12 IS LOWER POINT PT15 IS UPPER ****** by rajkumar ******
    msp.add_line(pt15, pt14)  # Corrected line addition # PT1 IS DIRT WALL EDGE ON RIVER SIDE ****** by rajkumar ******
    # Calculate remaining points for the right abutment
    yc = datum - 30.0
    y20 = yc + (abtlen / 2)   # gives Y ordinate on D/S of abt 
    y21 = y20 - abtlen          # gives y ordinate on u/s of abt 
    y16 = y20 + 0.15            #  gives Y ordinate on D/S of footing 
    y17 = y21 - 0.15            #  gives Y ordinate on U/S of footing 
    # Footing calculations
    footl = (y16 - y17)
    footl = footl / 2       #  EARLIER IGNORED
    x = footl * s
    y = footl * (1 - c)
    pt20 = (hpos(right_edge - x12 - x, left), vpos(y20)) 
    pt21 = (hpos(right_edge - x12 + x, left), vpos(y21)) 
    pt22 = (hpos(right_edge - x14 - x, left), vpos(y20)) 
    pt23 = (hpos(right_edge - x14 + x, left), vpos(y21)) 
    ptplan4 = pt21
    
    ################################################
    # Calculate footing points
    footl = (y16 - y17) / 2
    x = footl * s
    y = footl * (1 - c)
    pt16 = (hpos(right_edge - x10 - x, left), vpos(y16) - y) 
    pt17 = (hpos(right_edge - x10 + x, left), vpos(y17) + y) 
    pt18 = (hpos(right_edge - x7 - x, left), vpos(y16) - y) 
######################################################################            
    global pt19  # Access the global variable
    pt19 = None  # Declare pt19 as a global variable
    pt19 = (hpos(right_edge - x7 + x, left), vpos(y17) + y)

    
    # Draw abutment footing in plan
    msp.add_lwpolyline([pt16, pt17, pt19, pt18, pt16], close=True) 
    # Calculate remaining points
    pt24 = (hpos(right_edge - x1 - x, left), vpos(y20))  # Point 24
    pt25 = (hpos(right_edge - x1 + x, left), vpos(y21))  # Point 25
    pt26 = (hpos(right_edge - x3 - x, left), vpos(y20))  # Point 26
    pt27 = (hpos(right_edge - x3 + x, left), vpos(y21))  # Point 27
    pt28 = (hpos(right_edge - x5 - x, left), vpos(y20))  # Point 28
    pt29 = (hpos(right_edge - x5 + x, left), vpos(y21))  # Point 29
    pt30 = (hpos(right_edge - x6 - x, left), vpos(y20))  # Point 30
    pt31 = (hpos(right_edge - x6 + x, left), vpos(y21))  # Point 31

    # Final lines to connect the points
    msp.add_line(pt20, pt21)  # Line from pt20 to pt21
    msp.add_line(pt22, pt23)  # Line from pt22 to pt23
    msp.add_line(pt24, pt25)  # Line from pt24 to pt25
    msp.add_line(pt26, pt27)  # Line from pt26 to pt27
    msp.add_line(pt28, pt29)  # Line from pt28 to pt29
    msp.add_line(pt30, pt31)  # Line from pt30 to pt31
    msp.add_line(pt21, pt31)  # Line from pt21 to pt31
    msp.add_line(pt20, pt30)  # Line from pt20 to 
    # completed drawing plan abutment Right
# Save drawing to file
#####Boundary References
abt1(datum, vvs, left, hhs, sc)  # Generate left abutment
abt2(datum, vvs, left, hhs, sc, alcw)  # Generate right abutment
#################################################################################
### ABUTMENT PARTS COMPLETE
#################################################################################
# Set up the dimension style
st(doc)
###################################################################################################################################
##### drawing block boundary B01- ELEVATION
# Initial Definitions
pb1 = [wearing_course_start_x, wearing_course_y1]  # Left Top
pb2 = [wearing_course_end_x, wearing_course_y1]    # Right Top
pb3 = prb3
pb4 = prb4
drawn_width = [pb3[0] - pb1[0]]
drawn_height = [pb1[1] - pb4[1]]
# Calculate 50 mm offsets with scaling
hor_offset = 15 * scale1  # Horizontal offset in the drawing
ver_offset = 15 * scale2  # Vertical offset in the drawing

# Adjusted Coordinates for 50 mm clear boundary
pb1_adjusted = [pb1[0] - hor_offset, pb1[1] + ver_offset]  # Left Top (adjusted for clearance)
pb2_adjusted = [pb2[0] + hor_offset, pb2[1] + ver_offset]  # Right Top (adjusted for clearance)
pb4_adjusted = [pb1[0] - hor_offset, pb3[1] - ver_offset]   # Bottom Left (adjusted for clearance)
pb3_adjusted = [pb2[0] + hor_offset, pb3[1] - ver_offset]   # Bottom Right (adjusted for clearance)

#mid point pb3, pb4#
# Midpoint coordinates
midpoint_x = (pb4_adjusted[0] + pb3_adjusted[0]) / 2
midpoint_y = (pb4_adjusted[1] + pb3_adjusted[1]) / 2

midpoint = [midpoint_x, midpoint_y]
pm1 = midpoint
# Add polyline with adjusted boundary points
msp.add_lwpolyline([pb1_adjusted, pb2_adjusted, pb3_adjusted, pb4_adjusted, pb1_adjusted], close=True)

##############################################################################################################
##### drawing block boundary B02- PLAN
# Initial Definitions
x1 = pb1_adjusted[0]# LEFT POINT
x2 = pb2_adjusted[0]    # RIGHT POINT
y1 = pta7[1] # PIER FOOTING IN PLAN TOP LEVEL >>>>>> EARLIER DECLARED GLOBAL
y2 = pta8[1] # PIER FOOTING IN PLAN BOTTOM LEVEL >>>>>> EARLIER DECLARED GLOBAL
### top boundary line offset
t1 = y2 - (30 + futl / 2) * scale2
t2 = futl * scale2
print(t1, "t1")
pb1 = (x1, y1)
pb4 = (x1, y2)
pb2 = (x2, pb1[1])
pb3 = (x1, pb4[1])
# Dictionary to store computed values of points
# Calculate 50 mm offsets with scaling
hor_offset = 0 * scale1  # Horizontal offset in the drawing
ver_offset = 15 * scale2  # Vertical offset in the drawing

# Adjusted Coordinates for 50 mm clear boundary
pb1_adjusted = [pb1[0] - hor_offset, pb1[1] + ver_offset]  # Left Top (adjusted for clearance)
pb2_adjusted = [pb2[0] + hor_offset, pb2[1] + ver_offset]  # Right Top (adjusted for clearance)
pb4_adjusted = [pb1[0] - hor_offset, pb3[1] - ver_offset]   # Bottom Left (adjusted for clearance)
pb3_adjusted = [pb2[0] + hor_offset, pb3[1] - ver_offset]   # Bottom Right (adjusted for clearance)
print(pb1_adjusted, pb2_adjusted, pb3_adjusted, pb4_adjusted, "AAA")
#mid point pb3, pb4#
# Midpoint coordinates
midpoint_x = (pb4_adjusted[0] + pb3_adjusted[0]) / 2
midpoint_y = (pb4_adjusted[1] + pb3_adjusted[1]) / 2
midpoint = [midpoint_x, midpoint_y]
pm2 = midpoint
# Add polyline with adjusted boundary points
msp.add_lwpolyline([pb1_adjusted, pb2_adjusted, pb3_adjusted, pb4_adjusted, pb1_adjusted], close=True)
###############################################################################################################################
###################################################################################################################################
import ezdxf

def create_dxf_with_text():
    # Get the modelspace
    msp = doc.modelspace()

    # Iterate through each point and text content and create the MText entity
    for point, text_content in zip(points, text_contents):
        msp.add_mtext(
            text=text_content,
            dxfattribs={
                "insert": point,  # Insertion point (x, y)
                "char_height": text_height,  # Text height
                "width": text_width,  # Width factor for fitting
                "style": text_style_name,  # Use the bold text style
            },
        )

# Main DXF creation
if __name__ == "__main__":
    
    # Define text style
    text_style_name = "PMB100"
    if text_style_name not in doc.styles:
        style = doc.styles.new(name=text_style_name)
        style.dxf.font = "arialbd.ttf"  # Set the font to Arial Bold

    # Define common text attributes
    text_height = 500  # Text height in mm
    text_width = 30000  # Width of the text box in mm

    # Define points for the text articles
    datum = 0  # Assuming datum line at Y=0 in drawing
    scale_factor = 1000  # Assuming scale factor
    lbridge = 40 * scale_factor  # Bridge length (scaled)

    # Define insertion points
    points = [
        (pm1[0], pm1[1] + ver_offset / 2 ),
        (pm2[0], pm2[1] + ver_offset / 2),
        (3 * lbridge / 4, datum - 120),
        (lbridge / 2, datum - 160),
        (lbridge / 2, datum - 200),
    ]

    # Define text contents
    text_contents = [
        "T1: GENERAL ARRANGEMENT DRAWING",
        "T2: FOOTING PLAN",
        "T3: SECTIONAL PLAN",
        "T4: GENERAL NOTES",
        "T5: DESIGN PARAMETERS",
    ]

    # Call the function to create text articles
    

    # Call the function to create text articles
    create_dxf_with_text()
####################################################################################################################################    


###################################################################################################################################
directory = r"F:\LISP 2005\P1"
filename = "SUPER STRUCTURE.DXF"
file_path = os.path.join(directory, filename)  # Define the file_path
#f = open(file_path, "r")
############### Save in Specified Directory Filename ####################
doc.saveas(os.path.join(directory, filename))
doc.saveas("combined_drawing.dxf")
print("\nFile combined_drawing.dxf saved in user successfully.")
#########################################################################
###############################################################
def generate_tender_report(input_file, output_pdf):
    """Generate tender analysis report in PDF format (single file)."""
    try:
        # assume the sheet is called 'Bid Summary'
        df = pd.read_excel(input_file, sheet_name='Bid Summary')

        doc = SimpleDocTemplate(output_pdf, pagesize=landscape(letter))
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'Title', parent=styles['Heading1'], fontSize=16,
            spaceAfter=20, alignment=1)
        elements.append(Paragraph("TENDER ANALYSIS REPORT", title_style))

        table_data = [df.columns.tolist()] + df.values.tolist()
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR',  (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE',   (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID',       (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)

        doc.build(elements)
        print(f"Tender report generated: {output_pdf}")

    except Exception as e:
        print(f"Error generating tender report: {e}")
# Example usage:
# generate_tender_report("tender_data.xlsx", "tender_analysis.xlsx", "tender_report.pdf")

# [Rest of the goodfor4.py contents would go here...]

# ===========================================
# 7. MAIN EXECUTION BLOCK
# ===========================================
if __name__ == "__main__":
    import sys
    
    # Check if running with Streamlit
    if 'streamlit' in sys.modules:
        run_streamlit_app()
    else:
        # Command-line execution
        print("Running in command-line mode")
        
        # Example file paths
        input_file = "input.xlsx"
        output_dxf = "bridge_design.dxf"
        output_report = "tender_analysis.pdf"
        
        try:
            # Read variables from Excel
            df = read_variables(input_file)
            if df is not None:
                # Process variables and generate design
                # [Add your main processing logic here]
                
                # Save the DXF file
                doc.saveas(output_dxf)
                print(f"DXF file generated: {output_dxf}")
                
                # Generate tender report
                generate_tender_report(input_file, output_report)
                
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
# ---------------------------------------------------------
# 16. SCREEN-MODIFY INPUT MODE  (python bridge_gad_app.py)
# ---------------------------------------------------------
if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    import os

    def draw_bridge():
        """Regenerate DXF + PDF with current entries."""
        try:
            # 1. Build new DataFrame from GUI
            new_df = pd.DataFrame(
                [(float(v.get()), k, "") for k, v in entries.items()],
                columns=["Value", "Variable", "Description"]
            )
            global df
            df = new_df

            # 2. Re-read variables
            vars = dict(zip(df['Variable'], df['Value']))
            abtl   = float(vars.get('ABTL', 0))
            lspan  = float(vars.get('SPAN1', 10))
            nspan  = int(vars.get('NSPAN', 2))
            capw   = float(vars.get('CAPW', 1.2))
            capt   = float(vars.get('CAPT', 110))
            capb   = float(vars.get('CAPB', 109.4))
            futw   = float(vars.get('FUTW', 4.5))
            futd   = float(vars.get('FUTD', 1.5))
            futrl  = float(vars.get('FUTRL', 100))
            hhs    = 1

            # 3. Clear previous drawing & re-draw
            doc.entities.clear()
            generate_pier_caps(abtl, lspan, capw, capt, capb, nspan, hhs)
            generate_pier_footings(futw, futd, futrl, nspan)

            # 4. Save files
            dxf_path = filedialog.asksaveasfilename(
                title="Save DXF",
                defaultextension=".dxf",
                filetypes=[("DXF files", "*.dxf")]
            )
            if dxf_path:
                doc.saveas(dxf_path)
            pdf_path = filedialog.asksaveasfilename(
                title="Save Tender PDF",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")]
            )
            if pdf_path:
                generate_tender_report("input.xlsx", pdf_path)
            messagebox.showinfo("Done", "Files saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Create Tkinter window
    root = tk.Tk()
    root.title("Bridge Parameter Modifier")
    root.geometry("400x800")

    # Read original variables (or use defaults)
    try:
        df = read_variables("input.xlsx")
    except:
                df = pd.DataFrame([
            [186, "SCALE1", "Scale1"],
            [12.00, "ABTLEN", "Length Of Abutment Along Current Direction at cap level"],
            [0.30, "DWTH", "Dirtwall Thickness"],
            [0.75, "ALCW", "Abutment Left Cap Width Excluding D/W"],
            [100.00, "ALFL", "Abutment Left Footing Level"],
            [100.75, "ARFL", "Abutment RIGHT Footing Level"],
            [1.20, "ALCD", "Abutment Left Cap Depth"],
            [10.00, "ALFB", "Abt Left Front Batter (1 HOR : 10 VER)"],
            [101.00, "ALFBL", "Abt Left Front Batter RL"],
            [100.75, "ALFBR", "Abt RIGHT Front Batter RL"],
            [10.00, "ALTB", "Abt Left Toe Batter (1 HOR : 5 VER)"],
            [101.00, "ALTBL", "Abt Left Toe Batter Level Footing Top"],
            [100.75, "ALTBR", "Abt RIGHT Toe Batter Level Footing Top"],
            [1.50, "ALFO", "Abutment Left Front Offset To Footing"],
            [1.00, "ALFD", "Abt Left Footing Depth"],
            [3.00, "ALBB", "Abt Left Back Batter"],
            [101.00, "ALBBL", "Abt Left Back Batter RL"],
            [100.75, "ALBBR", "Abt RIGHT Back Batter RL"],
            [100, "SCALE2", "Scale2"],
            [0.00, "SKEW", "Degree Of Skew In Plan Of The Bridge"],
            [100.00, "DATUM", "Datum"],
            [110.98, "TOPRL", "Top RL Of The Bridge"],
            [0.00, "LEFT", "Left Most Chainage Of The Bridge"],
            [43.20, "RIGHT", "Right Most Chainage Of The Bridge"],
            [10.00, "XINCR", "Chainage Increment In X Direction"],
            [1.00, "YINCR", "Elevation Increment In Y Direction"],
            [21, "NOCH", "Total No. Of Chainages On C/S"],
            [4, "NSPAN", "Number of Spans"],
            [43.20, "LBRIDGE", "Length Of Bridge"],
            [0.00, "ABTL", "Read Chainage Of Left Abutment"],
            [110.98, "RTL", "Road Top Level"],
            [110.00, "SOFL", "Soffit Level"],
            [0.23, "KERBW", "Width Of Kerb At Deck Top"],
            [0.23, "KERBD", "Depth Of Kerb Above Deck Top"],
            [11.10, "CCBR", "Clear Carriageway Width Of Bridge"],
            [0.90, "SLBTHC", "Thickness Of Slab At Centre"],
            [0.75, "SLBTHE", "Thickness Of Slab At Edge"],
            [0.75, "SLBTHT", "Thickness Of Slab At Tip"],
            [110.00, "CAPT", "Pier Cap Top RL"],
            [109.40, "CAPB", "Pier Cap Bottom RL = Pier Top"],
            [1.20, "CAPW", "Cap Width"],
            [1.20, "PIERTW", "Pier Top Width"],
            [10.00, "BATTR", "Pier Batter"],
            [12.00, "PIERST", "Straight Length Of Pier"],
            [1.00, "PIERN", "Sr No Of Pier"],
            [10.80, "SPAN1", "Span Individual Length"],
            [100.00, "FUTRL", "Founding RL Of Pier Found"],
            [1.00, "FUTD", "Depth Of Footing"],
            [4.50, "FUTW", "Width Of Rect Footing"],
            [12.00, "FUTL", "Length Of Footing Along Current Direction"],
            [12.00, "ABTLEN", "Length Of abutment Along Current Direction"],
            [3.50, "LASLAB", "Length of approach slab"],
            [12.00, "APWTH", "Width of approach slab"],
            [0.38, "APTHK", "Thickness of approach slab"],
            [0.08, "WCTH", "Thickness of wearing course"]
        ], columns=["Value", "Variable", "Description"])

    entries = {}
    entries = {}
    for idx, (_, row) in enumerate(df.iterrows()):
        var = row["Variable"]
        val = row["Value"]
        desc = row["Description"]
        
        # Create label for Variable
        ttk.Label(root, text=var).grid(row=idx, column=0, sticky="e", padx=5, pady=2)
        
        # Create entry for Value
        val_entry = ttk.Entry(root, width=15)
        val_entry.insert(0, str(val) if pd.notnull(val) else "")
        val_entry.grid(row=idx, column=1, padx=5, pady=2)
        
        # Create label for Description (non-editable)
        ttk.Label(root, text=desc if pd.notnull(desc) else "").grid(row=idx, column=2, sticky="w", padx=5, pady=2)
        
        # Store the Value entry
        entries[var] = val_entry

    # Add the Draw & Save button
    ttk.Button(root, text="Draw & Save", command=draw_bridge).grid(row=len(df), column=0, columnspan=2, pady=15)

    root.mainloop()