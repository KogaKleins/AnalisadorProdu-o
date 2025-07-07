"""
Efficiency calculations and metrics module.
Contains functions for calculating and analyzing efficiency metrics.
"""

from core.config.setup_config import TEMPOS_SETUP as tempos_setup, get_setup_time

def calculate_general_metrics(grupos_para_analise, ops_analise, tempo_disponivel, df=None):
    """Calculate general metrics with new formulas (corrigido para considerar ganhos de tempo nas OPs e médias corretas)"""
    metrics = {
        'tempo_total_producao': 0.0,
        'tempo_total_acerto': 0.0,
        'qtd_total_produzida': 0.0,
        'tempo_total_perdido_ganho': 0.0,
        'eficiencia_producao': 0.0,
        'eficiencia_acerto': 0.0,
        'eficiencia_tempo_geral': 0.0,
        'tempo_ocioso': 0.0,
        'tempo_total_ganho': 0.0,
    }
    tempo_total_producao = 0
    tempo_total_acerto = 0
    qtd_total_produzida = 0
    for dados in grupos_para_analise.values():
        for detalhe in dados.get('detalhes_eventos', []):
            if detalhe.get('is_producao'):
                tempo_total_producao += detalhe.get('tempo_producao', 0)
                qtd_total_produzida += detalhe.get('qtd_produzida', 0)
            if detalhe.get('is_acerto'):
                tempo_total_acerto += detalhe.get('tempo_producao', 0)
    metrics['tempo_total_producao'] = tempo_total_producao
    metrics['tempo_total_acerto'] = tempo_total_acerto
    metrics['qtd_total_produzida'] = qtd_total_produzida
    tempo_total_ganho = 0
    eficiencia_producao_list = []
    eficiencia_acerto_list = []
    if ops_analise:
        for grupos_op in ops_analise.values():
            dados_op = consolidar_dados_op(grupos_op, df)
            # Ganho de produção
            if dados_op.get('ganho_producao', 0) > 0:
                tempo_total_ganho += dados_op['ganho_producao']
            # Ganho de setup (apenas se válido)
            if dados_op.get('ganho_setup', 0) > 0 and not dados_op.get('acerto_sem_producao', False):
                tempo_total_ganho += dados_op['ganho_setup']
            # Eficiência de produção (apenas OPs com produção)
            if dados_op.get('tem_producao') and dados_op.get('tempo_total_producao', 0) > 0 and dados_op.get('tempo_programado_producao', 0) > 0:
                eficiencia = (dados_op['tempo_programado_producao'] / dados_op['tempo_total_producao']) * 100
                eficiencia_producao_list.append(eficiencia)
            # Eficiência de acerto (apenas OPs com produção e acerto válido)
            if dados_op.get('tem_producao') and dados_op.get('tem_acerto') and dados_op.get('tempo_setup', 0) > 0 and dados_op.get('tempo_setup_programado', 0) > 0:
                eficiencia = (dados_op['tempo_setup_programado'] / dados_op['tempo_setup']) * 100
                eficiencia_acerto_list.append(eficiencia)
    metrics['tempo_total_ganho'] = int(round(tempo_total_ganho))
    # Tempo ocioso: tempo disponível menos produção e acerto (NÃO descontar ganhos)
    metrics['tempo_ocioso'] = int(max(0, round(tempo_disponivel - (tempo_total_producao + tempo_total_acerto))))
    if ops_analise:
        metrics.update(_calculate_ops_metrics(ops_analise, tempo_disponivel, df))
        if eficiencia_producao_list:
            metrics['eficiencia_producao'] = float(sum(eficiencia_producao_list)) / float(len(eficiencia_producao_list))
        if eficiencia_acerto_list:
            metrics['eficiencia_acerto'] = float(sum(eficiencia_acerto_list)) / float(len(eficiencia_acerto_list))
        if tempo_disponivel > 0:
            metrics['eficiencia_tempo_geral'] = ((tempo_total_producao + tempo_total_acerto + tempo_total_ganho) / tempo_disponivel) * 100
    return metrics

def _calculate_ops_metrics(ops_analise, tempo_disponivel, df=None):
    """Calculate metrics related to OPs"""
    metrics = {}
    soma_atraso_ops = 0
    count_ops = 0
    
    for grupos_op in ops_analise.values():
        dados_op = consolidar_dados_op(grupos_op, df)
        
        if dados_op['velocidade_nominal'] > 0 and dados_op['qtd_produzida'] > 0:
            tempo_programado = (dados_op['qtd_produzida'] / dados_op['velocidade_nominal']) * 60
            atraso = dados_op['tempo_total_producao'] - tempo_programado
            soma_atraso_ops += atraso
            count_ops += 1
    
    metrics['tempo_total_perdido_ganho'] = soma_atraso_ops
    return metrics

def consolidar_dados_op(grupos_op, df):
    """Consolida dados de múltiplos grupos da mesma OP, somando tempos, quantidades e calculando médias e ganhos/perdas."""
    from src.core.data.data_processor import tempo_para_minutos
    from core.config.setup_config import get_setup_time
    import re
    dados_consolidados = {
        'tempo_total_producao': 0,
        'tempo_setup': 0,
        'qtd_produzida': 0,
        'velocidade_nominal': 0,
        'os': '',
        'cliente': '',
        'processo': '',
        'tem_acerto': False,
        'tem_producao': False,
        'linhas': [],
        'tempo_programado_producao': 0,
        'velocidade_real': 0,
        'ganho_producao': 0,
        'ganho_setup': 0,
        'acerto_sem_producao': False,
        'tempo_setup_programado': 0,
    }
    total_tempo_producao = 0
    total_tempo_setup = 0
    total_qtd_produzida = 0
    velocidade_nominal = 0
    linhas = []
    tempo_setup_programado = 0
    processo_str = ''
    entradas_distintas = set()
    setup_por_entrada = {}
    for nome_grupo, dados in grupos_op:
        linhas.extend(dados.get('linhas', []))
        if dados.get('tem_producao'):
            total_tempo_producao += dados.get('tempo_total_producao', 0)
            total_qtd_produzida += dados.get('qtd_produzida', 0)
            if dados.get('velocidade_nominal', 0) > 0:
                velocidade_nominal = dados['velocidade_nominal']
            dados_consolidados['tem_producao'] = True
        if dados.get('tem_acerto'):
            dados_consolidados['tem_acerto'] = True
            # Identificar entradas distintas e somar apenas um setup por entrada
            if 'linhas' in dados:
                for idx in dados['linhas']:
                    try:
                        row = df.iloc[idx]
                        evento = str(row.get('Evento', '')).lower()
                        processo = str(row.get('Processo', ''))
                        proc_norm = processo.lower().strip()
                        import re, unidecode
                        proc_norm_sem_acento = unidecode.unidecode(proc_norm)
                        # 1. Se contém 'entrada', usa como chave
                        if 'entrada' in proc_norm_sem_acento:
                            chave_entrada = proc_norm_sem_acento
                        else:
                            partes = re.split(r'\s*-\s*', proc_norm_sem_acento)
                            titulo = partes[0] if partes else proc_norm_sem_acento
                            sufixo = ''
                            if len(partes) > 1:
                                sufixo = partes[-1]
                            match_suf = re.search(r'(f|v|t/r|tr|fr|fv|vr|cmyk|preto|colorido|\(.*\))$', sufixo)
                            sufixo_final = match_suf.group(1) if match_suf else sufixo
                            chave_entrada = f"{titulo.strip()}|{sufixo_final.strip()}"
                        if chave_entrada not in entradas_distintas:
                            entradas_distintas.add(chave_entrada)
                            # Tempo real de setup
                            tempo_real = tempo_para_minutos(str(row.get('Tempo', '')))
                            setup_por_entrada[chave_entrada] = tempo_real
                            # Tempo programado de setup
                            tempo_setup_str = str(row.get('Tempo Setup', '')).strip()
                            if tempo_setup_str and tempo_setup_str != '':
                                tempo_prog = tempo_para_minutos(tempo_setup_str)
                            else:
                                tempo_prog = get_setup_time(processo)
                            setup_por_entrada[f"prog_{chave_entrada}"] = tempo_prog
                            if not processo_str:
                                processo_str = processo
                    except Exception:
                        pass
    # Soma apenas um setup por entrada distinta para o programado,
    # mas para o tempo real, some todos os tempos das linhas de acerto do mesmo grupo/entrada
    total_tempo_setup = 0
    for chave in entradas_distintas:
        # Para cada entrada distinta, some todos os tempos das linhas de acerto daquele grupo/entrada
        tempo_real_entrada = 0
        for nome_grupo, dados in grupos_op:
            if 'linhas' in dados:
                for idx in dados['linhas']:
                    try:
                        row = df.iloc[idx]
                        evento = str(row.get('Evento', '')).lower()
                        processo = str(row.get('Processo', ''))
                        proc_norm = processo.lower().strip()
                        import re, unidecode
                        proc_norm_sem_acento = unidecode.unidecode(proc_norm)
                        # 1. Se contém 'entrada', usa como chave
                        if 'entrada' in proc_norm_sem_acento:
                            chave_entrada = proc_norm_sem_acento
                        else:
                            partes = re.split(r'\s*-\s*', proc_norm_sem_acento)
                            titulo = partes[0] if partes else proc_norm_sem_acento
                            sufixo = ''
                            if len(partes) > 1:
                                sufixo = partes[-1]
                            match_suf = re.search(r'(f|v|t/r|tr|fr|fv|vr|cmyk|preto|colorido|\(.*\))$', sufixo)
                            sufixo_final = match_suf.group(1) if match_suf else sufixo
                            chave_entrada = f"{titulo.strip()}|{sufixo_final.strip()}"
                        # --- AJUSTE SAKURAI: soma 'acerto' e 'gravando tela' ---
                        is_sakurai = 'sakurai' in proc_norm_sem_acento
                        if chave_entrada == chave and (
                            'acerto' in evento or (is_sakurai and 'gravando tela' in evento)
                        ):
                            tempo_real_entrada += tempo_para_minutos(str(row.get('Tempo', '')))
                    except Exception:
                        pass
        total_tempo_setup += tempo_real_entrada
    tempo_setup_programado = sum(setup_por_entrada[k] for k in setup_por_entrada if k.startswith('prog_'))
    if not dados_consolidados['os'] and dados.get('os'):
        dados_consolidados['os'] = dados['os']
        dados_consolidados['cliente'] = dados.get('cliente', '')
        dados_consolidados['processo'] = dados.get('processo', '')
    dados_consolidados['tempo_total_producao'] = total_tempo_producao
    dados_consolidados['tempo_setup'] = total_tempo_setup
    dados_consolidados['qtd_produzida'] = total_qtd_produzida
    dados_consolidados['velocidade_nominal'] = velocidade_nominal
    dados_consolidados['linhas'] = linhas
    # Calcular velocidade real
    if total_tempo_producao > 0:
        dados_consolidados['velocidade_real'] = (total_qtd_produzida / total_tempo_producao) * 60
    # Calcular tempo programado de produção e ganho de produção para Bobst
    # Extrai média p/h do campo Processo
    media_ph = 0
    # Prioriza 'Média Produção' do DataFrame se existir
    if df is not None and len(linhas) > 0:
        for idx in linhas:
            try:
                row = df.iloc[idx]
                media_producao = str(row.get('Média Produção', '')).strip()
                if media_producao:
                    match = re.search(r'(\d{1,3}(?:\.\d{3})*,?\d*|\d+)\s*p/h', media_producao)
                    if match:
                        media_str = match.group(1).replace('.', '').replace(',', '.')
                        media_ph = float(media_str)
                        break
            except Exception:
                pass
    if not media_ph:
        if not processo_str:
            processo_str = dados_consolidados['processo']
        match = re.search(r'(\d{1,3}(?:\.\d{3})*,?\d*|\d+)\s*p/h', processo_str)
        if match:
            media_str = match.group(1).replace('.', '').replace(',', '.')
            try:
                media_ph = float(media_str)
            except Exception:
                media_ph = 0
    if media_ph > 0 and total_qtd_produzida > 0:
        qtd_por_minuto = media_ph / 60
        tempo_programado = total_qtd_produzida / qtd_por_minuto
        dados_consolidados['tempo_programado_producao'] = tempo_programado
        dados_consolidados['ganho_producao'] = tempo_programado - total_tempo_producao
    elif velocidade_nominal > 0 and total_qtd_produzida > 0:
        tempo_programado = (total_qtd_produzida / velocidade_nominal) * 60
        dados_consolidados['tempo_programado_producao'] = tempo_programado
        dados_consolidados['ganho_producao'] = tempo_programado - total_tempo_producao
    # Se não encontrou tempo programado nas linhas, usa padrão do processo
    if tempo_setup_programado == 0:
        from .efficiency import calculate_setup_time
        tempo_setup_programado = calculate_setup_time(dados_consolidados['processo'])
    dados_consolidados['tempo_setup_programado'] = tempo_setup_programado
    # Calcular ganho/perda de setup
    if total_tempo_setup > 0:
        if total_tempo_producao > 0:
            dados_consolidados['ganho_setup'] = tempo_setup_programado - total_tempo_setup
        else:
            if total_tempo_setup <= tempo_setup_programado:
                dados_consolidados['ganho_setup'] = 0
                dados_consolidados['acerto_sem_producao'] = True
            else:
                dados_consolidados['ganho_setup'] = tempo_setup_programado - total_tempo_setup
                dados_consolidados['acerto_sem_producao'] = True
    return dados_consolidados

def calculate_setup_time(processo):
    """Calculate programmed setup time based on process type"""
    return tempos_setup.get(processo.upper(), 45)  # Default 45 minutes if not found

def get_efficiency_classification(eficiencia):
    """Get emoji classification based on efficiency percentage"""
    if eficiencia >= 95:
        return "🌟 EXCELENTE"
    elif eficiencia >= 85:
        return "✨ ÓTIMO"
    elif eficiencia >= 75:
        return "👍 BOM"
    elif eficiencia >= 65:
        return "⚠️ REGULAR"
    else:
        return "❌ INSATISFATÓRIO"

def calculate_op_metrics(dados_op):
    """Calculate specific metrics for an OP"""
    metrics = {
        'atraso': 0,
        'eficiencia_producao': 0,
        'eficiencia_setup': 0
    }
    
    if dados_op['velocidade_nominal'] > 0 and dados_op['qtd_produzida'] > 0:
        tempo_programado = (dados_op['qtd_produzida'] / dados_op['velocidade_nominal']) * 60
        metrics['atraso'] = dados_op['tempo_total_producao'] - tempo_programado
        
        if tempo_programado > 0:
            metrics['eficiencia_producao'] = (tempo_programado / dados_op['tempo_total_producao']) * 100
            
        if dados_op['tem_acerto']:
            tempo_setup_programado = calculate_setup_time(dados_op['processo'])
            if tempo_setup_programado > 0:
                metrics['eficiencia_setup'] = (tempo_setup_programado / dados_op['tempo_setup']) * 100
    
    return metrics

def generate_detailed_general_averages(ops_analise):
    return ''
