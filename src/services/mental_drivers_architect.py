import json
import logging
from typing import Dict, List, Any, Optional
from .ai_manager import AIManager

logger = logging.getLogger(__name__)

class MentalDriversArchitect:
    """Arquiteto de Drivers Mentais - Sistema de Ancoragem Psicológica"""

    def __init__(self, ai_manager: AIManager):
        self.ai_manager = ai_manager
        self.universal_drivers = self._load_universal_drivers()
        logger.info("Mental Drivers Architect inicializado com 19 drivers universais")

    def _load_universal_drivers(self) -> List[Dict[str, Any]]:
        """Carrega os 19 drivers mentais universais"""
        return [
            {
                "nome": "FERIDA EXPOSTA",
                "gatilho": "Dor não resolvida",
                "mecanica": "Trazer à consciência o que foi reprimido",
                "ativacao": "Você ainda [comportamento doloroso] mesmo sabendo que [consequência]?",
                "categoria": "emocional_primario"
            },
            {
                "nome": "TROFÉU SECRETO", 
                "gatilho": "Desejo inconfessável",
                "mecanica": "Validar ambições proibidas",
                "ativacao": "Não é sobre dinheiro, é sobre [desejo real oculto]",
                "categoria": "emocional_primario"
            },
            {
                "nome": "INVEJA PRODUTIVA",
                "gatilho": "Comparação com pares",
                "mecanica": "Transformar inveja em combustível", 
                "ativacao": "Enquanto você [situação atual], outros como você [resultado desejado]",
                "categoria": "emocional_primario"
            },
            {
                "nome": "RELÓGIO PSICOLÓGICO",
                "gatilho": "Urgência existencial",
                "mecanica": "Tempo como recurso finito",
                "ativacao": "Quantos [período] você ainda vai [desperdício]?",
                "categoria": "emocional_primario"
            },
            {
                "nome": "IDENTIDADE APRISIONADA",
                "gatilho": "Conflito entre quem é e quem poderia ser",
                "mecanica": "Expor a máscara social",
                "ativacao": "Você não é [rótulo limitante], você é [potencial real]",
                "categoria": "emocional_primario"
            },
            {
                "nome": "CUSTO INVISÍVEL",
                "gatilho": "Perda não percebida",
                "mecanica": "Quantificar o preço da inação",
                "ativacao": "Cada dia sem [solução] custa [perda específica]",
                "categoria": "emocional_primario"
            },
            {
                "nome": "AMBIÇÃO EXPANDIDA",
                "gatilho": "Sonhos pequenos demais",
                "mecanica": "Elevar o teto mental de possibilidades",
                "ativacao": "Se o esforço é o mesmo, por que você está pedindo tão pouco?",
                "categoria": "emocional_primario"
            },
            {
                "nome": "DIAGNÓSTICO BRUTAL",
                "gatilho": "Confronto com a realidade atual",
                "mecanica": "Criar indignação produtiva com status quo",
                "ativacao": "Olhe seus números/situação. Até quando você vai aceitar isso?",
                "categoria": "emocional_primario"
            },
            {
                "nome": "AMBIENTE VAMPIRO",
                "gatilho": "Consciência do entorno tóxico",
                "mecanica": "Revelar como ambiente atual suga energia/potencial",
                "ativacao": "Seu ambiente te impulsiona ou te mantém pequeno?",
                "categoria": "emocional_primario"
            },
            {
                "nome": "MENTOR SALVADOR",
                "gatilho": "Necessidade de orientação externa",
                "mecanica": "Ativar desejo por figura de autoridade que acredita neles",
                "ativacao": "Você precisa de alguém que veja seu potencial quando você não consegue",
                "categoria": "emocional_primario"
            },
            {
                "nome": "CORAGEM NECESSÁRIA",
                "gatilho": "Medo paralisante disfarçado",
                "mecanica": "Transformar desculpas em decisões corajosas",
                "ativacao": "Não é sobre condições perfeitas, é sobre decidir apesar do medo",
                "categoria": "emocional_primario"
            },
            {
                "nome": "MECANISMO REVELADO",
                "gatilho": "Compreensão do como",
                "mecanica": "Desmistificar o complexo",
                "ativacao": "É simplesmente [analogia simples], não [complicação percebida]",
                "categoria": "racional_complementar"
            },
            {
                "nome": "PROVA MATEMÁTICA",
                "gatilho": "Certeza numérica",
                "mecanica": "Equação irrefutável",
                "ativacao": "Se você fizer X por Y dias = Resultado Z garantido",
                "categoria": "racional_complementar"
            },
            {
                "nome": "PADRÃO OCULTO",
                "gatilho": "Insight revelador",
                "mecanica": "Mostrar o que sempre esteve lá",
                "ativacao": "Todos que conseguiram [resultado] fizeram [padrão específico]",
                "categoria": "racional_complementar"
            },
            {
                "nome": "EXCEÇÃO POSSÍVEL",
                "gatilho": "Quebra de limitação",
                "mecanica": "Provar que regras podem ser quebradas",
                "ativacao": "Diziam que [limitação], mas [prova contrária]",
                "categoria": "racional_complementar"
            },
            {
                "nome": "ATALHO ÉTICO",
                "gatilho": "Eficiência sem culpa",
                "mecanica": "Validar o caminho mais rápido",
                "ativacao": "Por que sofrer [tempo longo] se existe [atalho comprovado]?",
                "categoria": "racional_complementar"
            },
            {
                "nome": "DECISÃO BINÁRIA",
                "gatilho": "Simplificação radical",
                "mecanica": "Eliminar zona cinzenta",
                "ativacao": "Ou você [ação desejada] ou aceita [consequência dolorosa]",
                "categoria": "racional_complementar"
            },
            {
                "nome": "OPORTUNIDADE OCULTA",
                "gatilho": "Vantagem não percebida",
                "mecanica": "Revelar demanda/chance óbvia mas ignorada",
                "ativacao": "O mercado está gritando por [solução] e ninguém está ouvindo",
                "categoria": "racional_complementar"
            },
            {
                "nome": "MÉTODO VS SORTE",
                "gatilho": "Caos vs sistema",
                "mecanica": "Contrastar tentativa aleatória com caminho estruturado",
                "ativacao": "Sem método você está cortando mata com foice. Com método, está na autoestrada",
                "categoria": "racional_complementar"
            }
        ]

    def create_custom_drivers(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Cria drivers mentais customizados baseado no contexto"""

        logger.info(f"🧠 Criando drivers mentais customizados para {context.get('segmento', 'contexto')}")

        prompt = f"""
# ARQUITETO DE DRIVERS MENTAIS - SISTEMA DE ANCORAGEM PSICOLÓGICA

Baseado no contexto fornecido, crie 7-10 DRIVERS MENTAIS CUSTOMIZADOS seguindo a estrutura completa.

## CONTEXTO:
{json.dumps(context, ensure_ascii=False, indent=2)[:4000]}

CRIE drivers seguindo esta estrutura JSON:

```json
{{
  "drivers_customizados": [
    {{
      "nome": "NOME IMPACTANTE (máx 3 palavras)",
      "gatilho_central": "A emoção ou lógica core",
      "definicao_visceral": "1-2 frases que capturam a essência",
      "mecanica_psicologica": "Como funciona no cérebro",
      "momento_instalacao": "Quando plantar durante a jornada",
      "roteiro_ativacao": {{
        "pergunta_abertura": "Pergunta que expõe a ferida",
        "historia_analogia": "História/analogia de 3-5 frases que ilustra o conceito",
        "metafora_visual": "Metáfora visual que ancora na memória",
        "comando_acao": "Comando que direciona o comportamento"
      }},
      "frases_ancoragem": [
        "Frase 1 pronta para usar",
        "Frase 2 que reativa o driver",
        "Frase 3 que intensifica a tensão"
      ],
      "prova_logica": {{
        "estatistica": "Dado relevante",
        "caso_exemplo": "História real",
        "demonstracao": "Como provar na prática"
      }},
      "loop_reforco": "Como reativar em momentos posteriores",
      "categoria": "emocional_primario ou racional_complementar",
      "prioridade": "critica, alta ou media"
    }}
  ],
  "sequencia_estrategica": {{
    "fase_1_despertar": ["Driver para consciência"],
    "fase_2_desejo": ["Driver para amplificação"],
    "fase_3_decisao": ["Driver para pressão"],
    "fase_4_direcao": ["Driver para caminho"]
  }},
  "momentos_criticos": {{
    "abertura": "Driver para quebra de padrão",
    "desenvolvimento": "Driver para construção de crença", 
    "climax": "Driver para pré-pitch",
    "fechamento": "Driver para urgência final"
  }}
}}
```

Retorne APENAS o JSON estruturado, SEM explicações adicionais.
"""
        try:
            response = self.ai_manager.generate_text(prompt)
            response_json = json.loads(response)

            logger.info(f"✅ Drivers mentais customizados criados com sucesso.")
            return response_json

        except Exception as e:
            logger.error(f"❌ Erro ao gerar drivers mentais: {str(e)}", exc_info=True)

            # Retorna drivers básicos em caso de erro
            return {
                "drivers_customizados": [
                    {
                        "nome": "DIAGNÓSTICO BRUTAL",
                        "gatilho_central": "Confronto com realidade atual",
                        "definicao_visceral": f"Expor a verdade dolorosa sobre a situação atual em {context.get('segmento', 'negócios')}",
                        "mecanica_psicologica": "Criar indignação produtiva que gera movimento",
                        "momento_instalacao": "Abertura - primeira quebra de padrão",
                        "roteiro_ativacao": {
                            "pergunta_abertura": f"Seus resultados em {context.get('segmento', 'negócios')} condizem com seu potencial real?",
                            "historia_analogia": "É como olhar no espelho e ver que a pessoa refletida não é quem você planejou se tornar",
                            "metafora_visual": "Imagine um termômetro que finalmente mostra a temperatura real, não a que você gostaria que fosse",
                            "comando_acao": "Pare de aceitar mediocre como normal"
                        },
                        "frases_ancoragem": [
                            "Até quando você vai aceitar resultados que não condizem com seu potencial?",
                            "A realidade não negocia com suas desculpas",
                            "Diagnóstico honesto é o primeiro passo para cura real"
                        ],
                        "categoria": "emocional_primario",
                        "prioridade": "critica"
                    }
                ],
                "sequencia_estrategica": {
                    "fase_1_despertar": ["DIAGNÓSTICO BRUTAL"],
                    "fase_2_desejo": ["AMBIÇÃO EXPANDIDA"],
                    "fase_3_decisao": ["RELÓGIO PSICOLÓGICO"],
                    "fase_4_direcao": ["MÉTODO REVELADO"]
                }
            }

# Instância global para importação
from services.ai_manager import ai_manager
mental_drivers_architect = MentalDriversArchitect(ai_manager)