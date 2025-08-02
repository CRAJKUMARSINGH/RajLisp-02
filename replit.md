# Overview

RajLisp is a comprehensive structural design suite built with Streamlit for designing various concrete structural elements and road infrastructure. The application provides engineers with tools to design columns, beams, footings, staircases, sunshades, and road sections with automated calculations and DXF drawing generation. It serves as a digital assistant for structural engineers working on building and infrastructure projects, particularly following Indian standards and PMGSY specifications for rural roads.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit-based web application with a modular page structure
- **Layout**: Multi-column responsive design with tabbed interfaces for complex forms
- **Navigation**: Sidebar-based module selection with expandable state
- **Styling**: Custom CSS with engineering-themed gradients and card layouts
- **Form Handling**: Streamlit forms with real-time input validation and step-based increments

## Application Structure
- **Modular Design**: Each structural element is implemented as a separate module in the `modules/` directory
- **Page Components**: Individual modules for specific design tasks (columns, beams, footings, roads, etc.)
- **Utility Functions**: Centralized calculation and DXF generation utilities
- **Import Management**: Centralized module imports through `__init__.py` for easier maintenance

## Design Modules
The application is organized into structural and infrastructure design categories:

**Structural Elements**:
- Circular and rectangular columns with reinforcement design
- Column footings (circular and rectangular) with soil bearing calculations
- T-beams and L-beams with flange and web reinforcement
- Lintels for doors and windows
- Sunshades with cantilever design
- Staircases with step geometry and reinforcement

**Road Infrastructure**:
- PMGSY rural road design following government specifications
- Road longitudinal sections with gradient calculations
- Road plan layout with horizontal alignment
- Road cross-sections with pavement layers and drainage

## Calculation Engine
- **Structural Calculations**: Load capacity, moment calculations, and reinforcement design
- **Code Compliance**: Adherence to Indian standards for concrete design
- **Material Properties**: Support for various concrete grades (M20-M45) and steel grades (Fe415-Fe550)
- **Safety Factors**: Built-in safety considerations for structural design

## Drawing Generation
- **DXF Output**: Automated generation of technical drawings using ezdxf library
- **Dimensioning**: Automatic dimension addition for construction drawings
- **Layered Drawings**: Organized CAD layers for different drawing elements
- **File Handling**: Temporary file generation for download functionality

## Input Validation
- **Range Constraints**: Minimum and maximum value validation for all inputs
- **Engineering Standards**: Default values based on common engineering practices
- **Real-time Feedback**: Immediate calculation updates and gradient displays
- **Help System**: Contextual help text for all input parameters

# External Dependencies

## Core Framework
- **Streamlit**: Primary web application framework for user interface
- **NumPy**: Mathematical calculations and array operations for structural analysis

## Drawing and CAD
- **ezdxf**: DXF file generation for technical drawings and construction details
- **tempfile**: Temporary file handling for drawing downloads

## File Management
- **os**: Operating system interface for file path management
- **sys**: System-specific parameters for module path manipulation

## Utility Modules
- **utils.dxf_utils**: Custom utilities for DXF drawing creation and dimensioning
- **utils.calculations**: Structural engineering calculation functions for capacity and design verification

## Potential Integrations
The architecture supports future integration with:
- Database systems for project data storage
- External calculation engines for advanced structural analysis
- PDF generation for reports and documentation
- Material cost estimation APIs
- Building Information Modeling (BIM) export capabilities