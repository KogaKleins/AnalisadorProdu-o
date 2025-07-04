"""
OP analysis module.
Contains functions for generating the OP analysis section of the report.
"""

from .efficiency import (
    calculate_op_metrics,
    get_efficiency_classification,
    calculate_setup_time,
    consolidar_dados_op
)
import unidecode

def generate_ops_section(ops_analise, grupos_para_analise, df):
    """Generate OPs analysis section with corrected formulas and per-entry analysis"""
    from src.core.data.data_processor import to_float, tempo_para_minutos
    section = "🎯 ANÁLISE DETALHADA POR ORDEM DE PRODUÇÃO\n"
    section += "=" * 80 + "\n\n"
    
    for op_key, grupos_op in ops_analise.items():
        op_numero_original = extract_op_number_original(grupos_op)
        section += f"📋 OP {op_numero_original}\n"
        section += "─" * 60 + "\n"
        dados_op = consolidar_dados_op(grupos_op, df)
        section += f"Cliente: {dados_op['cliente']}\n"
        section += f"Processo: {dados_op['processo']}\n"
        # --- ANÁLISE POR ENTRADA ---
        # Ordenar os índices das linhas da OP para garantir agrupamento correto
        op_linhas = sorted(set([idx for nome_grupo, dados in grupos_op for idx in dados.get('linhas', [])]))
        entradas = []
        entradas_chaves = set()
        if df is not None and 'Processo' in df.columns and 'Evento' in df.columns:
            import re, unidecode
            for idx in op_linhas:
                row = df.iloc[idx]
                processo = str(row.get('Processo', '')).strip()
                evento = str(row.get('Evento', '')).strip().lower()
                if 'acerto' in evento and processo:
                    proc_norm = processo.lower().strip()
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
                    entradas.append((processo, idx, chave_entrada))
                    entradas_chaves.add(chave_entrada)
        # Só exibe ANÁLISE POR ENTRADA se houver mais de uma entrada distinta
        if len(entradas_chaves) > 1:
            section += "\n🔎 ANÁLISE POR ENTRADA:\n"
            for i, (processo, idx, chave_entrada) in enumerate(entradas, 1):
                row = df.iloc[idx]
                tempo_setup_programado = row.get('Tempo Setup', '')
                tempo_setup_real = row.get('Tempo', '')
                media_produzida = row.get('Média Produção', '')
                # Calcular velocidade real se possível
                qtd_produzida = row.get('Qtd. Produzida', 0)
                tempo_real_min = 0
                try:
                    tempo_real_min = tempo_para_minutos(tempo_setup_real)
                except Exception:
                    pass
                velocidade_real = None
                qtd_produzida_float = 0.0
                try:
                    qtd_produzida_float = to_float(qtd_produzida)
                except Exception:
                    pass
                if tempo_real_min > 0 and qtd_produzida_float > 0:
                    try:
                        velocidade_real = qtd_produzida_float / tempo_real_min * 60
                    except Exception:
                        velocidade_real = None
                # Calcular diferença entre programado e real (em minutos)
                tempo_prog_min = 0
                try:
                    tempo_prog_min = tempo_para_minutos(tempo_setup_programado)
                except Exception:
                    pass
                diff_min = tempo_real_min - tempo_prog_min
                # Extrair apenas o número da velocidade programada
                import re
                vel_prog_str = '—'
                vel_real_str = '0 p/h'
                def buscar_producao_vizinha(idx_atual, op_linhas):
                    for idx_next in op_linhas:
                        if idx_next > idx_atual:
                            row_next = df.iloc[idx_next]
                            evento_next = str(row_next.get('Evento', '')).strip().lower()
                            if 'producao' in unidecode.unidecode(evento_next):
                                return row_next
                    for idx_prev in reversed(op_linhas):
                        if idx_prev < idx_atual:
                            row_prev = df.iloc[idx_prev]
                            evento_prev = str(row_prev.get('Evento', '')).strip().lower()
                            if 'producao' in unidecode.unidecode(evento_prev):
                                return row_prev
                    return None
                if media_produzida:
                    match = re.search(r'(\d+[\.,]?\d*)', str(media_produzida))
                    if match:
                        vel_prog_str = f"{match.group(1).replace(',', '')} p/h"
                if vel_prog_str == '—':
                    prod_vizinha = buscar_producao_vizinha(idx, op_linhas)
                    if prod_vizinha is not None:
                        media_prod_vizinha = prod_vizinha.get('Média Produção', '')
                        if media_prod_vizinha:
                            match = re.search(r'(\d+[\.,]?\d*)', str(media_prod_vizinha))
                            if match:
                                vel_prog_str = f"{match.group(1).replace(',', '')} p/h"
                if vel_prog_str == '—':
                    for idx_op in op_linhas:
                        row_op = df.iloc[idx_op]
                        media_prod_op = row_op.get('Média Produção', '')
                        if media_prod_op:
                            match = re.search(r'(\d+[\.,]?\d*)', str(media_prod_op))
                            if match:
                                vel_prog_str = f"{match.group(1).replace(',', '')} p/h"
                                break
                match_entrada = re.match(r'(\d+ª entrada)', processo.lower())
                entrada_id = match_entrada.group(1) if match_entrada else ''
                vel_real_str = '0 p/h'
                idx_acerto = idx
                idx_prox_acerto = None
                for idx_next in op_linhas:
                    if idx_next > idx_acerto:
                        row_next = df.iloc[idx_next]
                        evento_next = str(row_next.get('Evento', '')).strip().lower()
                        processo_next = str(row_next.get('Processo', '')).strip().lower()
                        if 'acerto' in evento_next and processo_next != processo.lower():
                            idx_prox_acerto = idx_next
                            break
                def normaliza_proc(proc):
                    p = unidecode.unidecode(str(proc)).lower().replace('1°', '1a').replace('1ª', '1a').replace('2°', '2a').replace('2ª', '2a').replace('3°', '3a').replace('3ª', '3a').replace('4°', '4a').replace('4ª', '4a')
                    return ' '.join(p.split())
                proc_entrada = normaliza_proc(processo)
                qtd_total = 0.0
                tempo_total = 0.0
                encontrou_producao = False
                for idx_prod in op_linhas:
                    if idx_prod > idx_acerto and (idx_prox_acerto is None or idx_prod < idx_prox_acerto):
                        row_prod = df.iloc[idx_prod]
                        evento_prod = str(row_prod.get('Evento', '')).strip().lower()
                        evento_prod_norm = unidecode.unidecode(evento_prod)
                        if 'producao' in evento_prod_norm:
                            qtd_total += to_float(row_prod.get('Qtd. Produzida', 0))
                            if 'Tempo (min)' in row_prod and row_prod['Tempo (min)'] not in [None, '', 0]:
                                tempo_total += to_float(row_prod['Tempo (min)'])
                            else:
                                tempo_total += tempo_para_minutos(row_prod.get('Tempo', 0))
                            encontrou_producao = True
                if tempo_total > 0 and qtd_total > 0:
                    vel_real_str = f"{(qtd_total / tempo_total * 60):.0f} p/h"
                def format_diff(mins):
                    if mins == 0:
                        return '±00:00'
                    sinal = '-' if mins > 0 else '+'
                    mins_abs = abs(int(mins))
                    h = mins_abs // 60
                    m = mins_abs % 60
                    return f"{sinal}{h:02d}:{m:02d}"
                diff_str = format_diff(diff_min) if tempo_prog_min > 0 or tempo_real_min > 0 else '—'
                section += f"  {i}ª entrada: {processo}\n"
                section += f"    • Tempo acerto programado: {tempo_setup_programado}\n"
                section += f"    • Tempo acerto real: {tempo_setup_real}\n"
                section += f"    • Diferença: {diff_str}\n"
                section += f"    • Velocidade programada: {vel_prog_str}\n"
                section += f"    • Velocidade real: {vel_real_str}\n"
        # --- FIM ANÁLISE POR ENTRADA ---
        # Resumo geral da OP (como já existe)
        section += f"\nTempo Produção: {dados_op['tempo_total_producao']} min ({dados_op['tempo_total_producao']/60:.1f}h)\n"
        # Exibe tempo de setup programado apenas se houver acerto na OP
        tem_acerto_op = False
        if 'Evento' in df.columns:
            op_col = 'OS' if 'OS' in df.columns else 'OP'
            mask_op = df[op_col] == op_numero_original
            eventos_op = df.loc[mask_op, 'Evento'].astype(str).str.lower()
            tem_acerto_op = eventos_op.str.contains('acerto').any()
        if tem_acerto_op and dados_op['tempo_setup_programado'] > 0:
            section += f"Tempo de Setup Programado: {dados_op['tempo_setup_programado']} min\n"
            section += f"Tempo de Setup Utilizado: {dados_op['tempo_setup']:.0f} min\n"
        else:
            section += "Sem setup, apenas produção\n"
        if dados_op['ganho_setup'] > 0:
            section += f"Ganho de Setup: {dados_op['ganho_setup']} min (VÁLIDO - há produção)\n"
        elif dados_op['ganho_setup'] < 0:
            section += f"Atraso de Setup: {abs(dados_op['ganho_setup'])} min\n"
        # Caso especial: OP só de acerto
        if dados_op['acerto_sem_producao']:
            if dados_op['ganho_setup'] < 0:
                section += f"Atraso de Setup: {abs(dados_op['ganho_setup'])} min (NÃO VÁLIDO - sem produção, conta como 100% até o programado)\n"
            else:
                section += f"Setup aparentemente ganho: 0 min (NÃO VÁLIDO - sem produção, conta como 100%)\n"
        section += f"Qtd Produzida: {dados_op['qtd_produzida']:,}\n"
        # Velocidade real
        if dados_op['velocidade_real'] > 0:
            section += f"Velocidade Real: {dados_op['velocidade_real']:.0f} p/h\n"
        if dados_op['velocidade_nominal'] > 0:
            section += f"Velocidade Programada: {dados_op['velocidade_nominal']:.0f} p/h\n"
        # Ganho/perda de produção
        if dados_op['ganho_producao'] > 0:
            section += f"Ganho de Produção: {dados_op['ganho_producao']:.0f} min\n"
        elif dados_op['ganho_producao'] < 0:
            section += f"Atraso de Produção: {abs(dados_op['ganho_producao']):.0f} min\n"
        # Eficiência de produção
        eficiencia = None
        if dados_op['tempo_programado_producao'] > 0 and dados_op['tempo_total_producao'] > 0 and dados_op['qtd_produzida'] > 0:
            eficiencia = (dados_op['tempo_programado_producao'] / dados_op['tempo_total_producao']) * 100
            section += f"Eficiência de Produção: {eficiencia:.2f}%\n"
            # Bloco MÉDIA DE PRODUÇÃO DA OP
            section += f"\n📊 MÉDIA DE PRODUÇÃO DA OP:\n  • {eficiencia:.2f}%\n  • Minutos ganhos: {dados_op['ganho_producao']:.0f} min\n"
        # Média de acerto da OP
        eficiencia_acerto = None
        if dados_op['tempo_setup'] > 0:
            tempo_setup_programado = dados_op['tempo_setup_programado']
            if dados_op['acerto_sem_producao']:
                eficiencia_acerto = 100.0
                section += f"⚙️ MÉDIA DE ACERTO DA OP:\n  • {eficiencia_acerto:.1f}% (considerado como exato - sem produção)\n  • Observação: Ganho não contabilizado pois não há produção\n"
            else:
                eficiencia_acerto = (tempo_setup_programado / dados_op['tempo_setup']) * 100 if dados_op['tempo_setup'] else 0
                section += f"⚙️ MÉDIA DE ACERTO DA OP:\n  • {eficiencia_acerto:.1f}%\n  • Minutos ganhos: {dados_op['ganho_setup']} min {'(VÁLIDO)' if dados_op['tempo_total_producao'] > 0 else ''}\n"
        # Média final da OP
        if eficiencia is not None or eficiencia_acerto is not None:
            if eficiencia is not None and eficiencia_acerto is not None:
                media_final = (eficiencia + eficiencia_acerto) / 2
                section += f"\n🎯 MÉDIA FINAL DA OP:\n  • Média: {media_final:.1f}% {'🟢 EXCELENTE' if media_final >= 100 else '⚠️ REGULAR' if media_final >= 70 else '❌ INSATISFATÓRIO'}\n  • Fórmula: {eficiencia:.1f}% + {eficiencia_acerto:.1f}% / 2 = {media_final:.1f}%\n    - Produção: {dados_op['ganho_producao']:.0f} min\n    - Acerto: {dados_op['ganho_setup']} min\n"
            elif eficiencia is not None:
                section += f"\n🎯 MÉDIA FINAL DA OP:\n  • Média: {eficiencia:.1f}%\n  • Apenas produção nesta OP\n    - Produção: {dados_op['ganho_producao']:.0f} min\n"
            elif eficiencia_acerto is not None:
                section += f"\n🎯 MÉDIA FINAL DA OP:\n  • Média: {eficiencia_acerto:.1f}%\n  • Apenas acerto nesta OP\n    - Acerto: {dados_op['ganho_setup']} min\n"
        # Grupos desta OP
        section += "\n📁 Grupos desta OP:\n"
        for nome_grupo, dados in grupos_op:
            if dados['tem_acerto']:
                section += f"  • Acerto: linha(s) {', '.join(str(i+1) for i in dados['linhas'])}\n"
            if dados['tem_producao']:
                section += f"  • Produção: linha(s) {', '.join(str(i+1) for i in dados['linhas'])}\n"
        section += "\n" + "="*60 + "\n\n"
    return section

def extract_op_number_original(grupos_op):
    """Extract original OP number keeping format"""
    for nome_grupo, dados in grupos_op:
        os_original = dados.get('os_original', '') or dados.get('os', '')
        if os_original:
            return os_original
    return "N/A"

def generate_op_info(dados_op):
    """Generate basic OP information"""
    info = f"Cliente: {dados_op['cliente']}\n"
    info += f"Processo: {dados_op['processo']}\n"
    if dados_op['velocidade_nominal'] > 0:
        info += f"Velocidade Nominal: {dados_op['velocidade_nominal']:.0f} un/h\n"
    return info

def generate_setup_analysis(dados_op, tempo_setup_programado):
    """Generate setup analysis information"""
    analysis = ""
    
    if dados_op['tem_acerto']:
        analysis += "\n⚙️ ANÁLISE DE SETUP\n"
        analysis += f"Tempo Setup Programado: {tempo_setup_programado} min\n"
        analysis += f"Tempo Setup Real: {dados_op['tempo_setup']:.0f} min\n"
        
        # Calculate setup efficiency
        if tempo_setup_programado > 0:
            eficiencia_setup = (tempo_setup_programado / dados_op['tempo_setup']) * 100
            classification = get_efficiency_classification(eficiencia_setup)
            analysis += f"Eficiência Setup: {eficiencia_setup:.1f}% {classification}\n"
        
        if dados_op['tempo_setup'] > tempo_setup_programado:
            atraso = dados_op['tempo_setup'] - tempo_setup_programado
            analysis += f"⚠️ Atraso Setup: {atraso:.0f} min\n"
        else:
            ganho = tempo_setup_programado - dados_op['tempo_setup']
            analysis += f"✨ Ganho Setup: {ganho:.0f} min\n"
    
    return analysis

def generate_production_info(dados_op):
    """Generate production information"""
    info = "\n🏭 ANÁLISE DE PRODUÇÃO\n"
    info += f"Quantidade Produzida: {dados_op['qtd_produzida']:,.0f} un\n"
    info += f"Tempo Total de Produção: {dados_op['tempo_total_producao']:.0f} min\n"
    
    if dados_op['velocidade_nominal'] > 0 and dados_op['qtd_produzida'] > 0:
        tempo_programado = (dados_op['qtd_produzida'] / dados_op['velocidade_nominal']) * 60
        atraso = dados_op['tempo_total_producao'] - tempo_programado
        
        info += f"Tempo Programado: {tempo_programado:.0f} min\n"
        
        if atraso > 0:
            info += f"⚠️ Atraso Produção: {atraso:.0f} min\n"
        else:
            info += f"✨ Ganho Produção: {abs(atraso):.0f} min\n"
            
        # Calculate and show production efficiency
        if tempo_programado > 0:
            eficiencia = (tempo_programado / dados_op['tempo_total_producao']) * 100
            classification = get_efficiency_classification(eficiencia)
            info += f"\nEficiência de Produção: {eficiencia:.1f}% {classification}\n"
    
    return info

def generate_groups_summary(grupos_op):
    """Generate summary of all groups in the OP"""
    summary = "\n📊 GRUPOS DE EVENTOS\n"
    
    for nome_grupo, dados in grupos_op:
        summary += f"\n▫️ {nome_grupo}\n"
        if dados['tem_producao']:
            summary += f"  Produção: {dados['qtd_produzida']:,.0f} un em {dados['tempo_total_producao']:.0f} min\n"
        if dados['tem_acerto']:
            summary += f"  Setup: {dados['tempo_setup']:.0f} min\n"
    
    return summary
