#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Gerador de PDF
Endpoints para geração de relatórios em PDF
"""

import os
import logging
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
import tempfile

logger = logging.getLogger(__name__)

# Cria blueprint
pdf_bp = Blueprint('pdf', __name__)

class PDFGenerator:
    """Gerador de relatórios PDF profissionais"""

    def __init__(self):
        """Inicializa gerador de PDF"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Configura estilos personalizados"""

        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1a365d')
        ))

        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            textColor=colors.HexColor('#2d3748')
        ))

        # Seção
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=15,
            spaceBefore=20,
            textColor=colors.HexColor('#4a5568'),
            borderWidth=1,
            borderColor=colors.HexColor('#e2e8f0'),
            borderPadding=5
        ))

        # Texto normal
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_JUSTIFY,
            leading=14
        ))

        # Lista
        self.styles.add(ParagraphStyle(
            name='BulletList',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=8,
            leftIndent=20,
            bulletIndent=10
        ))

    def generate_analysis_report(self, analysis_data: dict) -> BytesIO:
        """Gera relatório completo da análise"""

        # Cria buffer em memória
        buffer = BytesIO()

        # Cria documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )

        # Constrói conteúdo
        story = []

        # Capa
        story.extend(self._build_cover_page(analysis_data))
        story.append(PageBreak())

        # Sumário executivo
        story.extend(self._build_executive_summary(analysis_data))
        story.append(PageBreak())

        # Avatar detalhado
        if 'avatar_ultra_detalhado' in analysis_data:
            story.extend(self._build_avatar_section(analysis_data['avatar_ultra_detalhado']))
            story.append(PageBreak())

        # Drivers Mentais Customizados
        if 'drivers_mentais_customizados' in analysis_data:
            story.extend(self._build_drivers_section(analysis_data['drivers_mentais_customizados']))
            story.append(PageBreak())

        # Sistema Anti-Objeção
        if 'sistema_anti_objecao' in analysis_data:
            story.extend(self._build_anti_objection_section(analysis_data['sistema_anti_objecao']))
            story.append(PageBreak())

        # Provas Visuais
        if 'provas_visuais_sugeridas' in analysis_data:
            story.extend(self._build_visual_proofs_section(analysis_data['provas_visuais_sugeridas']))
            story.append(PageBreak())

        # Pré-Pitch Invisível
        if 'pre_pitch_invisivel' in analysis_data:
            story.extend(self._build_pre_pitch_section(analysis_data['pre_pitch_invisivel']))
            story.append(PageBreak())

        # Posicionamento
        if 'escopo' in analysis_data:
            story.extend(self._build_positioning_section(analysis_data['escopo']))
            story.append(PageBreak())

        # Análise de concorrência
        if 'analise_concorrencia_detalhada' in analysis_data:
            story.extend(self._build_competition_section(analysis_data['analise_concorrencia_detalhada']))
            story.append(PageBreak())

        # Estratégia de marketing
        if 'estrategia_palavras_chave' in analysis_data:
            story.extend(self._build_marketing_section(analysis_data['estrategia_palavras_chave']))
            story.append(PageBreak())

        # Métricas e KPIs
        if 'metricas_performance_detalhadas' in analysis_data:
            story.extend(self._build_metrics_section(analysis_data['metricas_performance_detalhadas']))
            story.append(PageBreak())

        # Projeções
        if 'projecoes_cenarios' in analysis_data:
            story.extend(self._build_projections_section(analysis_data['projecoes_cenarios']))
            story.append(PageBreak())

        # Plano de ação
        if 'plano_acao_detalhado' in analysis_data:
            story.extend(self._build_action_plan_section(analysis_data['plano_acao_detalhado']))
            story.append(PageBreak())

        # Insights exclusivos
        if 'insights_exclusivos' in analysis_data:
            story.extend(self._build_insights_section(analysis_data['insights_exclusivos']))
            story.append(PageBreak())

        # Pesquisa Web Massiva
        if 'pesquisa_web_massiva' in analysis_data:
            story.extend(self._build_research_section(analysis_data['pesquisa_web_massiva']))

        # Gera PDF
        doc.build(story)
        buffer.seek(0)

        return buffer

    def _build_cover_page(self, data: dict) -> list:
        """Constrói página de capa"""
        story = []

        # Título principal
        story.append(Paragraph("ANÁLISE ULTRA-DETALHADA DE MERCADO", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5*inch))

        # Subtítulo
        segmento = data.get('segmento', 'Não informado')
        produto = data.get('produto', 'Não informado')

        story.append(Paragraph(f"Segmento: {segmento}", self.styles['CustomSubtitle']))
        if produto != 'Não informado':
            story.append(Paragraph(f"Produto: {produto}", self.styles['CustomSubtitle']))

        story.append(Spacer(1, 1*inch))

        # Informações do relatório
        metadata = data.get('metadata', {})
        generated_at = metadata.get('generated_at', datetime.now().isoformat())

        info_data = [
            ['Data de Geração:', generated_at[:10]],
            ['Versão:', '2.0.0'],
            ['Modelo IA:', metadata.get('model', 'Gemini Pro')],
            ['Tempo de Processamento:', f"{metadata.get('processing_time', 0)} segundos"]
        ]

        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))

        story.append(info_table)
        story.append(Spacer(1, 1*inch))

        # Rodapé da capa
        story.append(Paragraph("ARQV30 Enhanced v2.0", self.styles['CustomNormal']))
        story.append(Paragraph("Powered by Artificial Intelligence", self.styles['CustomNormal']))

        return story

    def _build_executive_summary(self, data: dict) -> list:
        """Constrói sumário executivo"""
        story = []

        story.append(Paragraph("SUMÁRIO EXECUTIVO", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        # Resumo dos principais pontos
        summary_points = [
            f"Segmento analisado: {data.get('segmento', 'N/A')}",
            f"Público-alvo: {data.get('publico', 'N/A')}",
            f"Preço: R$ {data.get('preco', 'N/A')}",
            f"Objetivo de receita: R$ {data.get('objetivo_receita', 'N/A')}"
        ]

        for point in summary_points:
            story.append(Paragraph(f"• {point}", self.styles['BulletList']))

        story.append(Spacer(1, 0.2*inch))

        # Principais insights
        insights = data.get('insights_exclusivos', [])
        if insights:
            story.append(Paragraph("Principais Insights:", self.styles['SectionHeader']))
            for insight in insights[:5]:  # Primeiros 5 insights
                story.append(Paragraph(f"• {insight}", self.styles['BulletList']))

        return story

    def _build_avatar_section(self, avatar_data: dict) -> list:
        """Constrói seção do avatar"""
        story = []

        story.append(Paragraph("AVATAR ULTRA-DETALHADO", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        # Perfil demográfico
        demo = avatar_data.get('perfil_demografico', {})
        if demo:
            story.append(Paragraph("Perfil Demográfico", self.styles['SectionHeader']))

            demo_data = [
                ['Idade:', demo.get('idade', 'N/A')],
                ['Gênero:', demo.get('genero', 'N/A')],
                ['Renda:', demo.get('renda', 'N/A')],
                ['Escolaridade:', demo.get('escolaridade', 'N/A')],
                ['Localização:', demo.get('localizacao', 'N/A')]
            ]

            demo_table = Table(demo_data, colWidths=[1.5*inch, 4*inch])
            demo_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))

            story.append(demo_table)
            story.append(Spacer(1, 0.2*inch))

        # Perfil psicográfico
        psico = avatar_data.get('perfil_psicografico', {})
        if psico:
            story.append(Paragraph("Perfil Psicográfico", self.styles['SectionHeader']))

            for key, value in psico.items():
                if value:
                    story.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", self.styles['CustomNormal']))

        # Dores específicas
        dores = avatar_data.get('dores_especificas', [])
        if dores:
            story.append(Paragraph("Dores Específicas", self.styles['SectionHeader']))
            for dor in dores:
                story.append(Paragraph(f"• {dor}", self.styles['BulletList']))

        # Desejos profundos
        desejos = avatar_data.get('desejos_profundos', [])
        if desejos:
            story.append(Paragraph("Desejos Profundos", self.styles['SectionHeader']))
            for desejo in desejos:
                story.append(Paragraph(f"• {desejo}", self.styles['BulletList']))

        return story

    def _build_drivers_section(self, drivers_data) -> list:
        """Constrói seção de drivers mentais"""
        story = []

        story.append(Paragraph("DRIVERS MENTAIS CUSTOMIZADOS", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        if isinstance(drivers_data, dict) and 'drivers_customizados' in drivers_data:
            drivers = drivers_data['drivers_customizados']
        elif isinstance(drivers_data, list):
            drivers = drivers_data
        else:
            drivers = []

        for i, driver in enumerate(drivers, 1):
            if isinstance(driver, dict):
                story.append(Paragraph(f"Driver {i}: {driver.get('nome', 'Driver Mental')}", self.styles['SectionHeader']))

                story.append(Paragraph(f"<b>Gatilho Central:</b> {driver.get('gatilho_central', 'N/A')}", self.styles['CustomNormal']))
                story.append(Paragraph(f"<b>Definição:</b> {driver.get('definicao_visceral', 'N/A')}", self.styles['CustomNormal']))

                if driver.get('roteiro_ativacao'):
                    roteiro = driver['roteiro_ativacao']
                    story.append(Paragraph("<b>Roteiro de Ativação:</b>", self.styles['CustomNormal']))
                    story.append(Paragraph(f"• Pergunta: {roteiro.get('pergunta_abertura', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"• História: {roteiro.get('historia_analogia', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"• Comando: {roteiro.get('comando_acao', 'N/A')}", self.styles['BulletList']))

                if driver.get('frases_ancoragem'):
                    story.append(Paragraph("<b>Frases de Ancoragem:</b>", self.styles['CustomNormal']))
                    for frase in driver['frases_ancoragem']:
                        story.append(Paragraph(f"• \"{frase}\"", self.styles['BulletList']))

                story.append(Spacer(1, 0.2*inch))

        return story

    def _build_anti_objection_section(self, anti_objection_data) -> list:
        """Constrói seção do sistema anti-objeção"""
        story = []

        story.append(Paragraph("SISTEMA ANTI-OBJEÇÃO", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        # Objeções universais
        if anti_objection_data.get('objecoes_universais'):
            story.append(Paragraph("Objeções Universais", self.styles['SectionHeader']))

            for tipo, objecao in anti_objection_data['objecoes_universais'].items():
                if isinstance(objecao, dict):
                    story.append(Paragraph(f"<b>{tipo.title()}:</b>", self.styles['CustomNormal']))
                    story.append(Paragraph(f"Objeção: {objecao.get('objecao', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"Contra-ataque: {objecao.get('contra_ataque', 'N/A')}", self.styles['BulletList']))
                    story.append(Spacer(1, 0.1*inch))

        # Objeções ocultas
        if anti_objection_data.get('objecoes_ocultas'):
            story.append(Paragraph("Objeções Ocultas", self.styles['SectionHeader']))

            for tipo, objecao in anti_objection_data['objecoes_ocultas'].items():
                if isinstance(objecao, dict):
                    story.append(Paragraph(f"<b>{tipo.replace('_', ' ').title()}:</b>", self.styles['CustomNormal']))
                    story.append(Paragraph(f"Perfil: {objecao.get('perfil_tipico', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"Contra-ataque: {objecao.get('contra_ataque', 'N/A')}", self.styles['BulletList']))
                    story.append(Spacer(1, 0.1*inch))

        return story

    def _build_visual_proofs_section(self, visual_proofs_data) -> list:
        """Constrói seção de provas visuais"""
        story = []

        story.append(Paragraph("PROVAS VISUAIS INSTANTÂNEAS", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        if isinstance(visual_proofs_data, list):
            for i, prova in enumerate(visual_proofs_data, 1):
                if isinstance(prova, dict):
                    story.append(Paragraph(f"PROVI {i}: {prova.get('nome', 'Prova Visual')}", self.styles['SectionHeader']))

                    story.append(Paragraph(f"<b>Conceito Alvo:</b> {prova.get('conceito_alvo', 'N/A')}", self.styles['CustomNormal']))
                    story.append(Paragraph(f"<b>Experimento:</b> {prova.get('experimento', 'N/A')}", self.styles['CustomNormal']))

                    if prova.get('materiais'):
                        story.append(Paragraph("<b>Materiais:</b>", self.styles['CustomNormal']))
                        for material in prova['materiais']:
                            story.append(Paragraph(f"• {material}", self.styles['BulletList']))

                    story.append(Spacer(1, 0.2*inch))

        return story

    def _build_pre_pitch_section(self, pre_pitch_data) -> list:
        """Constrói seção do pré-pitch invisível"""
        story = []

        story.append(Paragraph("PRÉ-PITCH INVISÍVEL", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        # Orquestração emocional
        if pre_pitch_data.get('orquestracao_emocional'):
            story.append(Paragraph("Orquestração Emocional", self.styles['SectionHeader']))

            sequencia = pre_pitch_data['orquestracao_emocional'].get('sequencia_psicologica', [])
            for fase in sequencia:
                if isinstance(fase, dict):
                    story.append(Paragraph(f"<b>{fase.get('fase', 'Fase')}:</b> {fase.get('objetivo', 'N/A')}", self.styles['CustomNormal']))
                    story.append(Paragraph(f"Tempo: {fase.get('tempo', 'N/A')}", self.styles['BulletList']))
                    if fase.get('tecnicas'):
                        story.append(Paragraph(f"Técnicas: {', '.join(fase['tecnicas'])}", self.styles['BulletList']))
                    story.append(Spacer(1, 0.1*inch))

        # Roteiro completo
        if pre_pitch_data.get('roteiro_completo'):
            story.append(Paragraph("Roteiro Completo", self.styles['SectionHeader']))
            roteiro = pre_pitch_data['roteiro_completo']

            if roteiro.get('abertura'):
                abertura = roteiro['abertura']
                story.append(Paragraph(f"<b>Abertura ({abertura.get('tempo', 'N/A')}):</b>", self.styles['CustomNormal']))
                story.append(Paragraph(abertura.get('script', 'N/A'), self.styles['BulletList']))

            if roteiro.get('fechamento'):
                fechamento = roteiro['fechamento']
                story.append(Paragraph(f"<b>Fechamento ({fechamento.get('tempo', 'N/A')}):</b>", self.styles['CustomNormal']))
                story.append(Paragraph(fechamento.get('script', 'N/A'), self.styles['BulletList']))

        return story

    def _build_research_section(self, research_data) -> list:
        """Constrói seção da pesquisa web massiva"""
        story = []

        story.append(Paragraph("PESQUISA WEB MASSIVA", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        # Estatísticas da pesquisa
        story.append(Paragraph("Estatísticas da Pesquisa", self.styles['SectionHeader']))

        stats_data = [
            ['Métrica', 'Valor'],
            ['Total de Queries', str(research_data.get('total_queries', 0))],
            ['Total de Resultados', str(research_data.get('total_resultados', 0))],
            ['Conteúdo Extraído', f"{research_data.get('conteudo_extraido_chars', 0):,} caracteres"],
        ]

        stats_table = Table(stats_data, colWidths=[2*inch, 2*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(stats_table)
        story.append(Spacer(1, 0.2*inch))

        # Queries executadas
        if research_data.get('queries_executadas'):
            story.append(Paragraph("Queries Executadas", self.styles['SectionHeader']))
            for query in research_data['queries_executadas'][:10]:  # Primeiras 10
                story.append(Paragraph(f"• {query}", self.styles['BulletList']))

        return story

    def _build_positioning_section(self, escopo_data: dict) -> list:
        """Constrói seção de posicionamento"""
        story = []

        story.append(Paragraph("ESCOPO E POSICIONAMENTO", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        # Posicionamento no mercado
        posicionamento = escopo_data.get('posicionamento_mercado', '')
        if posicionamento:
            story.append(Paragraph("Posicionamento no Mercado", self.styles['SectionHeader']))
            story.append(Paragraph(posicionamento, self.styles['CustomNormal']))

        # Proposta de valor
        proposta = escopo_data.get('proposta_valor', '')
        if proposta:
            story.append(Paragraph("Proposta de Valor", self.styles['SectionHeader']))
            story.append(Paragraph(proposta, self.styles['CustomNormal']))

        # Diferenciais competitivos
        diferenciais = escopo_data.get('diferenciais_competitivos', [])
        if diferenciais:
            story.append(Paragraph("Diferenciais Competitivos", self.styles['SectionHeader']))
            for diferencial in diferenciais:
                story.append(Paragraph(f"• {diferencial}", self.styles['BulletList']))

        return story

    def _build_competition_section(self, competition_data: dict) -> list:
        """Constrói seção de análise de concorrência"""
        story = []

        story.append(Paragraph("ANÁLISE DE CONCORRÊNCIA", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        # Concorrentes diretos
        diretos = competition_data.get('concorrentes_diretos', [])
        if diretos:
            story.append(Paragraph("Concorrentes Diretos", self.styles['SectionHeader']))

            for i, concorrente in enumerate(diretos, 1):
                if isinstance(concorrente, dict):
                    nome = concorrente.get('nome', f'Concorrente {i}')
                    story.append(Paragraph(f"<b>{nome}</b>", self.styles['CustomNormal']))

                    pontos_fortes = concorrente.get('pontos_fortes', [])
                    if pontos_fortes:
                        story.append(Paragraph("Pontos Fortes:", self.styles['CustomNormal']))
                        for ponto in pontos_fortes:
                            story.append(Paragraph(f"• {ponto}", self.styles['BulletList']))

                    pontos_fracos = concorrente.get('pontos_fracos', [])
                    if pontos_fracos:
                        story.append(Paragraph("Pontos Fracos:", self.styles['CustomNormal']))
                        for ponto in pontos_fracos:
                            story.append(Paragraph(f"• {ponto}", self.styles['BulletList']))

                    story.append(Spacer(1, 0.1*inch))

        # Gaps de oportunidade
        gaps = competition_data.get('gaps_oportunidade', [])
        if gaps:
            story.append(Paragraph("Oportunidades Identificadas", self.styles['SectionHeader']))
            for gap in gaps:
                story.append(Paragraph(f"• {gap}", self.styles['BulletList']))

        return story

    def _build_marketing_section(self, marketing_data: dict) -> list:
        """Constrói seção de estratégia de marketing"""
        story = []

        story.append(Paragraph("ESTRATÉGIA DE MARKETING", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        # Palavras-chave primárias
        primarias = marketing_data.get('palavras_primarias', [])
        if primarias:
            story.append(Paragraph("Palavras-Chave Primárias", self.styles['SectionHeader']))
            story.append(Paragraph(", ".join(primarias), self.styles['CustomNormal']))

        # Palavras-chave secundárias
        secundarias = marketing_data.get('palavras_secundarias', [])
        if secundarias:
            story.append(Paragraph("Palavras-Chave Secundárias", self.styles['SectionHeader']))
            story.append(Paragraph(", ".join(secundarias[:15]), self.styles['CustomNormal']))

        # Long tail
        long_tail = marketing_data.get('long_tail', [])
        if long_tail:
            story.append(Paragraph("Palavras-Chave Long Tail", self.styles['SectionHeader']))
            story.append(Paragraph(", ".join(long_tail[:10]), self.styles['CustomNormal']))

        return story

    def _build_metrics_section(self, metrics_data: dict) -> list:
        """Constrói seção de métricas"""
        story = []

        story.append(Paragraph("MÉTRICAS DE PERFORMANCE", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        # KPIs principais
        kpis = metrics_data.get('kpis_principais', [])
        if kpis:
            story.append(Paragraph("KPIs Principais", self.styles['SectionHeader']))

            for kpi in kpis:
                if isinstance(kpi, dict):
                    metrica = kpi.get('metrica', 'N/A')
                    objetivo = kpi.get('objetivo', 'N/A')
                    story.append(Paragraph(f"<b>{metrica}:</b> {objetivo}", self.styles['CustomNormal']))

        # ROI esperado
        roi = metrics_data.get('roi_esperado', '')
        if roi:
            story.append(Paragraph("ROI Esperado", self.styles['SectionHeader']))
            story.append(Paragraph(roi, self.styles['CustomNormal']))

        return story

    def _build_projections_section(self, projections_data: dict) -> list:
        """Constrói seção de projeções"""
        story = []

        story.append(Paragraph("PROJEÇÕES E CENÁRIOS", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        # Tabela de cenários
        cenarios = ['conservador', 'realista', 'otimista']
        table_data = [['Cenário', 'Receita Mensal', 'Clientes/Mês', 'Ticket Médio']]

        for cenario in cenarios:
            cenario_data = projections_data.get(cenario, {})
            if cenario_data:
                table_data.append([
                    cenario.title(),
                    cenario_data.get('receita_mensal', 'N/A'),
                    cenario_data.get('clientes_mes', 'N/A'),
                    cenario_data.get('ticket_medio', 'N/A')
                ])

        if len(table_data) > 1:
            projections_table = Table(table_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            projections_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))

            story.append(projections_table)

        return story

    def _build_action_plan_section(self, action_data: dict) -> list:
        """Constrói seção do plano de ação"""
        story = []

        story.append(Paragraph("PLANO DE AÇÃO DETALHADO", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        # Fases do plano
        fases = ['fase_1_preparacao', 'fase_2_lancamento', 'fase_3_crescimento']

        for fase in fases:
            fase_data = action_data.get(fase, {})
            if fase_data:
                fase_nome = fase.replace('_', ' ').title()
                story.append(Paragraph(fase_nome, self.styles['SectionHeader']))

                duracao = fase_data.get('duracao', 'N/A')
                story.append(Paragraph(f"<b>Duração:</b> {duracao}", self.styles['CustomNormal']))

                atividades = fase_data.get('atividades', [])
                if atividades:
                    story.append(Paragraph("<b>Atividades:</b>", self.styles['CustomNormal']))
                    for atividade in atividades:
                        story.append(Paragraph(f"• {atividade}", self.styles['BulletList']))

                story.append(Spacer(1, 0.1*inch))

        return story

    def _build_insights_section(self, insights: list) -> list:
        """Constrói seção de insights exclusivos"""
        story = []

        story.append(Paragraph("INSIGHTS EXCLUSIVOS", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        for i, insight in enumerate(insights, 1):
            story.append(Paragraph(f"{i}. {insight}", self.styles['CustomNormal']))
            story.append(Spacer(1, 0.1*inch))

        return story

    def _build_ultra_detailed_avatar_section(self, avatar_data: dict) -> list:
        """Constrói seção ultra-detalhada do avatar com dashboard completo"""
        story = []

        story.append(Paragraph("🎯 AVATAR ARQUEOLÓGICO ULTRA-DETALHADO", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.3*inch))

        # Dashboard completo do avatar
        dashboard = avatar_data.get('dashboard_avatar_completo', {})

        if dashboard:
            # Identidade Demográfica Precisa
            demo = dashboard.get('identidade_demografica_precisa', {})
            if demo:
                story.append(Paragraph("📊 IDENTIDADE DEMOGRÁFICA PRECISA", self.styles['SectionHeader']))

                story.append(Paragraph(f"<b>Idade Específica:</b> {demo.get('idade_especifica', 'N/A')}", self.styles['CustomNormal']))
                story.append(Paragraph(f"<b>Distribuição de Gênero:</b> {demo.get('genero_distribuicao', 'N/A')}", self.styles['CustomNormal']))

                # Localização detalhada
                loc = demo.get('localizacao_detalhada', {})
                if loc:
                    story.append(Paragraph("<b>Localização Detalhada:</b>", self.styles['CustomNormal']))
                    story.append(Paragraph(f"• Regiões: {loc.get('regioes_concentracao', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"• Tipo de cidade: {loc.get('tipo_cidade', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"• Mobilidade: {loc.get('mobilidade_geografica', 'N/A')}", self.styles['BulletList']))

                # Educação
                edu = demo.get('nivel_educacional_completo', {})
                if edu:
                    story.append(Paragraph("<b>Nível Educacional:</b>", self.styles['CustomNormal']))
                    story.append(Paragraph(f"• Formação: {edu.get('formacao_principal', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"• Áreas: {edu.get('areas_conhecimento', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"• Educação continuada: {edu.get('educacao_continuada', 'N/A')}", self.styles['BulletList']))

                # Situação familiar
                fam = demo.get('situacao_familiar_detalhada', {})
                if fam:
                    story.append(Paragraph("<b>Situação Familiar:</b>", self.styles['CustomNormal']))
                    story.append(Paragraph(f"• Estado civil: {fam.get('estado_civil', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"• Filhos: {fam.get('filhos', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"• Responsabilidades: {fam.get('responsabilidades_familiares', 'N/A')}", self.styles['BulletList']))

                # Perfil econômico
                econ = demo.get('perfil_economico_completo', {})
                if econ:
                    story.append(Paragraph("<b>Perfil Econômico:</b>", self.styles['CustomNormal']))
                    story.append(Paragraph(f"• Renda individual: {econ.get('renda_individual', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"• Renda familiar: {econ.get('renda_familiar', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"• Fontes de renda: {econ.get('fontes_renda', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"• Patrimônio: {econ.get('patrimonio_estimado', 'N/A')}", self.styles['BulletList']))

                story.append(Spacer(1, 0.2*inch))

            # Perfil Psicográfico Visceral
            psico = dashboard.get('perfil_psicografico_visceral', {})
            if psico:
                story.append(Paragraph("🧠 PERFIL PSICOGRÁFICO VISCERAL", self.styles['SectionHeader']))

                # Personalidade detalhada
                pers = psico.get('personalidade_detalhada', {})
                if pers:
                    story.append(Paragraph("<b>Personalidade Detalhada:</b>", self.styles['CustomNormal']))

                    big_five = pers.get('big_five', {})
                    if big_five:
                        story.append(Paragraph("Big Five:", self.styles['CustomNormal']))
                        for trait, desc in big_five.items():
                            story.append(Paragraph(f"• {trait.title()}: {desc}", self.styles['BulletList']))

                    story.append(Paragraph(f"• Estilo comunicação: {pers.get('estilo_comunicacao', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"• Tomada de decisão: {pers.get('tomada_decisao', 'N/A')}", self.styles['BulletList']))
                    story.append(Paragraph(f"• Gestão de tempo: {pers.get('gestao_tempo', 'N/A')}", self.styles['BulletList']))

                # Valores e crenças
                val = psico.get('valores_e_crenças', {})
                if val:
                    story.append(Paragraph("<b>Valores e Crenças:</b>", self.styles['CustomNormal']))

                    valores = val.get('valores_fundamentais', [])
                    if valores:
                        story.append(Paragraph("Valores fundamentais:", self.styles['CustomNormal']))
                        for valor in valores[:5]:
                            story.append(Paragraph(f"• {valor}", self.styles['BulletList']))

                    crenças_lim = val.get('crenças_limitantes', [])
                    if crenças_lim:
                        story.append(Paragraph("Crenças limitantes:", self.styles['CustomNormal']))
                        for crenca in crenças_lim[:3]:
                            story.append(Paragraph(f"• {crenca}", self.styles['BulletList']))

                    story.append(Paragraph(f"• Relação com dinheiro: {val.get('relacao_dinheiro', 'N/A')}", self.styles['BulletList']))

                # Medos e ansiedades
                medos = psico.get('medos_e_ansiedades', {})
                if medos:
                    story.append(Paragraph("<b>Medos e Ansiedades:</b>", self.styles['CustomNormal']))
                    story.append(Paragraph(f"• Medo primário: {medos.get('medo_primario', 'N/A')}", self.styles['BulletList']))

                    medos_sec = medos.get('medos_secundarios', [])
                    if medos_sec:
                        story.append(Paragraph("Medos secundários:", self.styles['CustomNormal']))
                        for medo in medos_sec[:3]:
                            story.append(Paragraph(f"• {medo}", self.styles['BulletList']))

                    ansiedades = medos.get('ansiedades_cotidianas', [])
                    if ansiedades:
                        story.append(Paragraph("Ansiedades cotidianas:", self.styles['CustomNormal']))
                        for ansiedade in ansiedades[:3]:
                            story.append(Paragraph(f"• {ansiedade}", self.styles['BulletList']))

                # Desejos e aspirações
                desejos = psico.get('desejos_e_aspirações', {})
                if desejos:
                    story.append(Paragraph("<b>Desejos e Aspirações:</b>", self.styles['CustomNormal']))
                    story.append(Paragraph(f"• Desejo primário: {desejos.get('desejo_primario', 'N/A')}", self.styles['BulletList']))

                    desejos_oc = desejos.get('desejos_ocultos', [])
                    if desejos_oc:
                        story.append(Paragraph("Desejos ocultos:", self.styles['CustomNormal']))
                        for desejo in desejos_oc[:3]:
                            story.append(Paragraph(f"• {desejo}", self.styles['BulletList']))

                    sonhos = desejos.get('sonhos_audaciosos', [])
                    if sonhos:
                        story.append(Paragraph("Sonhos audaciosos:", self.styles['CustomNormal']))
                        for sonho in sonhos[:3]:
                            story.append(Paragraph(f"• {sonho}", self.styles['BulletList']))

                story.append(Spacer(1, 0.2*inch))

            # Dores e Frustrações Viscerais
            dores = dashboard.get('dores_frustrações_viscerais', {})
            if dores:
                story.append(Paragraph("💔 DORES E FRUSTRAÇÕES VISCERAIS", self.styles['SectionHeader']))

                story.append(Paragraph(f"<b>Dor Primária Inconfessável:</b> {dores.get('dor_primaria_inconfessavel', 'N/A')}", self.styles['CustomNormal']))

                frusts = dores.get('frustrações_diarias', [])
                if frusts:
                    story.append(Paragraph("<b>Frustrações Diárias:</b>", self.styles['CustomNormal']))
                    for frust in frusts[:5]:
                        story.append(Paragraph(f"• {frust}", self.styles['BulletList']))

                arrep = dores.get('arrependimentos_passado', [])
                if arrep:
                    story.append(Paragraph("<b>Arrependimentos do Passado:</b>", self.styles['CustomNormal']))
                    for arr in arrep[:3]:
                        story.append(Paragraph(f"• {arr}", self.styles['BulletList']))

                comp = dores.get('comparações_dolorosas', [])
                if comp:
                    story.append(Paragraph("<b>Comparações Dolorosas:</b>", self.styles['CustomNormal']))
                    for c in comp[:3]:
                        story.append(Paragraph(f"• {c}", self.styles['BulletList']))

                story.append(Spacer(1, 0.2*inch))

            # Objeções e Resistências Típicas
            obj = dashboard.get('objeções_resistencias_típicas', {})
            if obj:
                story.append(Paragraph("🛡️ OBJEÇÕES E RESISTÊNCIAS TÍPICAS", self.styles['SectionHeader']))

                # Objeções de tempo
                obj_tempo = obj.get('objecoes_tempo', {})
                if obj_tempo:
                    story.append(Paragraph("<b>Objeções de Tempo:</b>", self.styles['CustomNormal']))
                    frases = obj_tempo.get('frases_exatas', [])
                    if frases:
                        for frase in frases[:3]:
                            story.append(Paragraph(f"• \"{frase}\"", self.styles['BulletList']))
                    story.append(Paragraph(f"• Verdadeira razão: {obj_tempo.get('verdadeira_razao', 'N/A')}", self.styles['BulletList']))

                # Objeções de dinheiro
                obj_din = obj.get('objecoes_dinheiro', {})
                if obj_din:
                    story.append(Paragraph("<b>Objeções de Dinheiro:</b>", self.styles['CustomNormal']))
                    frases = obj_din.get('frases_exatas', [])
                    if frases:
                        for frase in frases[:3]:
                            story.append(Paragraph(f"• \"{frase}\"", self.styles['BulletList']))

                    gastos = obj_din.get('gastos_supérfluos', [])
                    if gastos:
                        story.append(Paragraph("Gastos supérfluos:", self.styles['CustomNormal']))
                        for gasto in gastos[:3]:
                            story.append(Paragraph(f"• {gasto}", self.styles['BulletList']))

                # Objeções de confiança
                obj_conf = obj.get('objecoes_confiança', {})
                if obj_conf:
                    story.append(Paragraph("<b>Objeções de Confiança:</b>", self.styles['CustomNormal']))
                    desconf = obj_conf.get('desconfianças_específicas', [])
                    if desconf:
                        for desc in desconf[:3]:
                            story.append(Paragraph(f"• {desc}", self.styles['BulletList']))

                story.append(Spacer(1, 0.2*inch))

            # Jornada de Transformação Desejada
            jornada = dashboard.get('jornada_transformação_desejada', {})
            if jornada:
                story.append(Paragraph("🚀 JORNADA DE TRANSFORMAÇÃO DESEJADA", self.styles['SectionHeader']))

                story.append(Paragraph(f"<b>Situação Atual (Odiada):</b> {jornada.get('situacao_atual_odiada', 'N/A')}", self.styles['CustomNormal']))
                story.append(Paragraph(f"<b>Estado Futuro (Sonhado):</b> {jornada.get('estado_futuro_sonhado', 'N/A')}", self.styles['CustomNormal']))
                story.append(Paragraph(f"<b>Ponte Necessária:</b> {jornada.get('ponte_necessaria', 'N/A')}", self.styles['CustomNormal']))
                story.append(Paragraph(f"<b>Tempo de Tolerância:</b> {jornada.get('tempo_tolerancia', 'N/A')}", self.styles['CustomNormal']))
                story.append(Paragraph(f"<b>Investimento Máximo:</b> {jornada.get('investimento_máximo', 'N/A')}", self.styles['CustomNormal']))

                marcos = jornada.get('marcos_transformação', [])
                if marcos:
                    story.append(Paragraph("<b>Marcos de Transformação:</b>", self.styles['CustomNormal']))
                    for marco in marcos[:5]:
                        story.append(Paragraph(f"• {marco}", self.styles['BulletList']))

        return story

    def generate_complete_pdf(self, analysis_data: dict) -> BytesIO:
        """Gera relatório completo da análise"""

        # Cria buffer na memória
        buffer = BytesIO()

        # Cria documento PDF
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )

        # Constrói conteúdo
        story = []

        # Capa
        story.extend(self._build_cover_page(analysis_data))
        story.append(PageBreak())

        results = analysis_data.get('results', {})

        # Seções completas do relatório ultra-detalhado
        story.extend(self._build_executive_summary(analysis_data))
        story.extend(self._build_market_research_section(results.get('research_data', {})))
        story.extend(self._build_ultra_detailed_avatar_section(results.get('avatar_data', {})))
        story.extend(self._build_mental_drivers_section(results.get('drivers_data', {})))
        story.extend(self._build_anti_objection_section(results.get('anti_objection_data', {})))
        story.extend(self._build_visual_proofs_section(results.get('visual_proofs_data', {})))
        story.extend(self._build_pre_pitch_section(results.get('pre_pitch_data', {})))
        story.extend(self._build_competition_section(results.get('competition_data', {})))
        story.extend(self._build_positioning_section(results.get('escopo_data', {})))
        story.extend(self._build_marketing_section(results.get('marketing_data', {})))
        story.extend(self._build_metrics_section(results.get('metrics_data', {})))
        story.extend(self._build_projections_section(results.get('projections_data', {})))
        story.extend(self._build_action_plan_section(results.get('action_plan_data', {})))
        story.extend(self._build_insights_section(results.get('insights_exclusivos', [])))
        # I am skipping _build_implementation_roadmap and _build_appendix_section because they are not defined
        # story.extend(self._build_implementation_roadmap(results))
        # story.extend(self._build_appendix_section(results))

        # Gera PDF
        doc.build(story)
        buffer.seek(0)

        return buffer

# Instância global do gerador
pdf_generator = PDFGenerator()

@pdf_bp.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    """Gera PDF da análise"""

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'error': 'Dados não fornecidos',
                'message': 'Envie os dados da análise no corpo da requisição'
            }), 400

        # Gera PDF
        logger.info("Gerando relatório PDF...")
        pdf_buffer = pdf_generator.generate_analysis_report(data)

        # Salva arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf_buffer.getvalue())
            tmp_file_path = tmp_file.name

        # Retorna arquivo
        return send_file(
            tmp_file_path,
            as_attachment=True,
            download_name=f"analise_mercado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        logger.error(f"Erro ao gerar PDF: {str(e)}")
        return jsonify({
            'error': 'Erro ao gerar PDF',
            'message': str(e)
        }), 500

@pdf_bp.route('/pdf_preview', methods=['POST'])
def pdf_preview():
    """Gera preview do PDF (metadados)"""

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'error': 'Dados não fornecidos'
            }), 400

        # Calcula estatísticas do relatório
        sections = []

        if 'avatar_ultra_detalhado' in data:
            sections.append('Avatar Ultra-Detalhado')

        if 'escopo' in data:
            sections.append('Escopo e Posicionamento')

        if 'analise_concorrencia_detalhada' in data:
            sections.append('Análise de Concorrência')

        if 'estrategia_palavras_chave' in data:
            sections.append('Estratégia de Marketing')

        if 'metricas_performance_detalhadas' in data:
            sections.append('Métricas de Performance')

        if 'projecoes_cenarios' in data:
            sections.append('Projeções e Cenários')

        if 'plano_acao_detalhado' in data:
            sections.append('Plano de Ação')

        if 'insights_exclusivos' in data:
            sections.append('Insights Exclusivos')

        # Estima páginas
        estimated_pages = len(sections) + 2  # +2 para capa e sumário

        return jsonify({
            'sections': sections,
            'estimated_pages': estimated_pages,
            'file_size_estimate': f"{estimated_pages * 50}KB",
            'generation_time_estimate': f"{estimated_pages * 2} segundos"
        })

    except Exception as e:
        logger.error(f"Erro no preview: {str(e)}")
        return jsonify({
            'error': 'Erro ao gerar preview',
            'message': str(e)
        }), 500