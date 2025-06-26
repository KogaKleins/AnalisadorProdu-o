"""
Setup configuration module.
Contains configuration for setup times and related functionality.
"""

# Setup times dictionary (in minutes)
TEMPOS_SETUP = {
    'berco': 180,          # Time for "berço" processes
    'colagem_bandeja': 130,  # Time for bandeja bonding
    'fundo_automatico_primeiro': 130,  # First automatic bottom
    'fundo_automatico_outros': 30,   # Other automatic bottoms
    'colagem_lateral_primeiro': 130,  # First lateral bonding
    'colagem_lateral_outros': 15,    # Other lateral bondings
    'default': 180         # Default time
}

def get_setup_time(process_type, is_first=True):
    """
    Get setup time for a specific process type.
    
    Args:
        process_type (str): Type of process
        is_first (bool): Whether this is the first setup of this type
        
    Returns:
        int: Setup time in minutes
    """
    process_type = process_type.lower()
    
    if "berço" in process_type or "berco" in process_type:
        return TEMPOS_SETUP['berco']
    
    if "fundo" in process_type and "automatic" in process_type.replace("ô", "o").replace("á", "a"):
        return TEMPOS_SETUP['fundo_automatico_primeiro'] if is_first else TEMPOS_SETUP['fundo_automatico_outros']
    
    if "colagem" in process_type:
        if "bandeja" in process_type:
            return TEMPOS_SETUP['colagem_bandeja']
        elif "lateral" in process_type:
            return TEMPOS_SETUP['colagem_lateral_primeiro'] if is_first else TEMPOS_SETUP['colagem_lateral_outros']
    
    return TEMPOS_SETUP['default']

def update_setup_time(process_type, time_minutes):
    """
    Update setup time for a specific process type.
    
    Args:
        process_type (str): Type of process to update
        time_minutes (int): New setup time in minutes
        
    Returns:
        bool: True if updated successfully, False if process type not found
    """
    if process_type in TEMPOS_SETUP:
        TEMPOS_SETUP[process_type] = time_minutes
        return True
    return False
