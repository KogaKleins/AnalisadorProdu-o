import pandas as pd

def limpar_setup_op_sem_acerto(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove o tempo de setup de todas as linhas de uma OP se não houver nenhum evento de acerto para aquela OP.
    Funciona para qualquer máquina.
    """
    if 'Tempo Setup' not in df.columns or ('OS' not in df.columns and 'OP' not in df.columns) or 'Evento' not in df.columns:
        return df
    op_col = 'OS' if 'OS' in df.columns else 'OP'
    ops = df[op_col].unique()
    for op in ops:
        mask_op = df[op_col] == op
        eventos = df.loc[mask_op, 'Evento'].astype(str).str.lower()
        tem_acerto = eventos.str.contains('acerto').any()
        if not tem_acerto:
            df.loc[mask_op, 'Tempo Setup'] = ''
    return df 