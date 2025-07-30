#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARQV30 Enhanced v2.0 - Configuração do Banco de Dados
Integração com Supabase PostgreSQL
"""

import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from supabase.client import create_client, Client
import json

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Gerenciador de conexão e operações com Supabase"""

    def __init__(self):
        """Inicializa conexão com Supabase"""
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_ANON_KEY')
        self.service_role_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

        if not self.supabase_url or not self.supabase_key:
            raise ValueError("Credenciais do Supabase não configuradas")

        # Cliente principal (anon key)
        self.client: Client = create_client(self.supabase_url, self.supabase_key)

        # Cliente admin (service role)
        if self.service_role_key:
            self.admin_client: Client = create_client(self.supabase_url, self.service_role_key)
        else:
            self.admin_client = self.client

    def test_connection(self) -> bool:
        """Testa conexão com o banco"""
        try:
            # Tenta fazer uma query simples
            result = self.client.table('analyses').select('id').limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"Erro ao testar conexão: {str(e)}")
            return False

    def create_analysis(self, analysis_data: dict) -> Optional[str]:
        """Cria nova análise no banco de dados"""
        try:
            supabase = get_db_client()

            # Função para serializar objetos complexos
            def serialize_data(obj):
                if hasattr(obj, '__dict__'):
                    return obj.__dict__
                elif isinstance(obj, (list, tuple)):
                    return [serialize_data(item) for item in obj]
                elif isinstance(obj, dict):
                    return {k: serialize_data(v) for k, v in obj.items()}
                else:
                    return obj

            # Serializar os resultados da análise
            results = analysis_data.get('results', {})
            serialized_results = serialize_data(results)

            response = supabase.table('analyses').insert({
                'segment': str(analysis_data.get('segmento', '')),
                'product': str(analysis_data.get('produto', '')),
                'price': float(analysis_data.get('preco', 0)) if analysis_data.get('preco') else 0,
                'target_audience': str(analysis_data.get('publico', '')),
                'revenue_goal': float(analysis_data.get('objetivo_receita', 0)) if analysis_data.get('objetivo_receita') else 0,
                'marketing_budget': float(analysis_data.get('orcamento_marketing', 0)) if analysis_data.get('orcamento_marketing') else 0,
                'launch_timeline': str(analysis_data.get('prazo_lancamento', '')),
                'competitors': str(analysis_data.get('concorrentes', '')),
                'search_query': str(analysis_data.get('query', '')),
                'additional_data': str(analysis_data.get('dados_adicionais', '')),
                'analysis_results': serialized_results,
                'created_at': datetime.utcnow().isoformat()
            }).execute()

            if response.data:
                logger.info(f"✅ Análise criada com ID: {response.data[0]['id']}")
                return response.data[0]['id']
            else:
                logger.error("❌ Falha ao criar análise - sem dados de resposta")
                return None

        except Exception as e:
            logger.error(f"Erro ao criar análise: {str(e)}")
            return None

    def update_analysis(self, analysis_id: int, update_data: Dict[str, Any]) -> bool:
        """Atualiza análise existente"""
        try:
            # Adiciona timestamp de atualização
            update_data['updated_at'] = datetime.now().isoformat()

            # Converte dados JSON para string se necessário
            for key, value in update_data.items():
                if isinstance(value, (dict, list)):
                    update_data[key] = json.dumps(value, ensure_ascii=False)

            # Atualiza no banco
            result = self.client.table('analyses').update(update_data).eq('id', analysis_id).execute()

            if result.data:
                logger.info(f"Análise {analysis_id} atualizada com sucesso")
                return True
            else:
                logger.error(f"Erro ao atualizar análise {analysis_id}")
                return False

        except Exception as e:
            logger.error(f"Erro ao atualizar análise {analysis_id}: {str(e)}")
            return False

    def get_analysis(self, analysis_id: int) -> Optional[Dict[str, Any]]:
        """Busca análise por ID"""
        try:
            result = self.client.table('analyses').select('*').eq('id', analysis_id).execute()

            if result.data:
                analysis = result.data[0]

                # Converte campos JSON de volta para objetos
                json_fields = [
                    'avatar_data', 'positioning_data', 'competition_data',
                    'marketing_data', 'metrics_data', 'funnel_data',
                    'market_intelligence', 'action_plan', 'comprehensive_analysis'
                ]

                for field in json_fields:
                    if analysis.get(field) and isinstance(analysis[field], str):
                        try:
                            analysis[field] = json.loads(analysis[field])
                        except json.JSONDecodeError:
                            pass

                return analysis
            else:
                return None

        except Exception as e:
            logger.error(f"Erro ao buscar análise {analysis_id}: {str(e)}")
            return None

    def list_analyses(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Lista análises com paginação"""
        try:
            result = self.client.table('analyses')\
                .select('id, nicho, produto, status, created_at, updated_at')\
                .order('created_at', desc=True)\
                .range(offset, offset + limit - 1)\
                .execute()

            return result.data if result.data else []

        except Exception as e:
            logger.error(f"Erro ao listar análises: {str(e)}")
            return []

    def delete_analysis(self, analysis_id: int) -> bool:
        """Remove análise do banco"""
        try:
            result = self.client.table('analyses').delete().eq('id', analysis_id).execute()

            if result.data:
                logger.info(f"Análise {analysis_id} removida com sucesso")
                return True
            else:
                logger.error(f"Erro ao remover análise {analysis_id}")
                return False

        except Exception as e:
            logger.error(f"Erro ao remover análise {analysis_id}: {str(e)}")
            return False

    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do banco"""
        try:
            # Total de análises
            total_result = self.client.table('analyses').select('id', count='exact').execute()
            total_analyses = total_result.count if total_result.count else 0

            # Análises por status
            status_result = self.client.table('analyses')\
                .select('status', count='exact')\
                .execute()

            status_counts = {}
            if status_result.data:
                for item in status_result.data:
                    status = item.get('status', 'unknown')
                    status_counts[status] = status_counts.get(status, 0) + 1

            # Análises recentes (últimos 7 dias)
            from datetime import timedelta
            week_ago = (datetime.now() - timedelta(days=7)).isoformat()

            recent_result = self.client.table('analyses')\
                .select('id', count='exact')\
                .gte('created_at', week_ago)\
                .execute()

            recent_count = recent_result.count if recent_result.count else 0

            return {
                'total_analyses': total_analyses,
                'status_counts': status_counts,
                'recent_analyses': recent_count,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {str(e)}")
            return {
                'total_analyses': 0,
                'status_counts': {},
                'recent_analyses': 0,
                'error': str(e)
            }

# Instância global do gerenciador
db_manager = DatabaseManager()