"""
Core module for report generation.
This module coordinates the generation of different report sections.
"""

from datetime import datetime
from .sections import (
    period,
    summary,
    efficiency,
    ops
)

class ReportGenerator:
    def __init__(self):
        self.sections = []
        
    def generate_report(self, data, report_config):
        """
        Generate a complete production analysis report.
        
        Args:
            data (dict): Data containing groups and OPs analysis
            report_config (dict): Configuration for report generation
            
        Returns:
            str: Complete formatted report
        """
        grupos_para_analise = data.get('grupos', {})
        ops_analise = data.get('ops', {})
        hora_inicio = report_config.get('hora_inicio')
        hora_fim = report_config.get('hora_fim')
        intervalo = report_config.get('intervalo', 60)
        
        # Calculate available time
        tempo_disponivel = period.calculate_available_time(hora_inicio, hora_fim, intervalo)
        
        # Header section
        report = self._generate_header()
        
        # Period section
        report += period.generate_period_section(hora_inicio, hora_fim, intervalo, tempo_disponivel)
        
        # Calculate general metrics
        metrics = efficiency.calculate_general_metrics(grupos_para_analise, ops_analise, tempo_disponivel)
        
        # Summary section
        report += summary.generate_general_summary(metrics, tempo_disponivel)
        
        # General averages section
        if ops_analise:
            report += efficiency.generate_simplified_general_averages(ops_analise)
        
        # OPs analysis section
        if ops_analise:
            report += ops.generate_ops_section(ops_analise, grupos_para_analise)
        
        return report
    
    def _generate_header(self):
        """Generate report header with current date"""
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        header = f"📊 RELATÓRIO DE DESEMPENHO - {data_atual}\n"
        header += "=" * 80 + "\n\n"
        return header
