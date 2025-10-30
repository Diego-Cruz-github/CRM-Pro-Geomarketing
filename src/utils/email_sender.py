import requests
import os
from typing import List, Dict, Optional
import logging

class SparkPostEmailSender:
    """
    Serviço para envio de emails via SparkPost API
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('SPARKPOST_API_KEY')
        self.base_url = 'https://api.sparkpost.com/api/v1'
        self.headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }
        
    def send_single_email(self, to_email: str, subject: str, content: str, 
                         from_email: str = None, from_name: str = None) -> Dict:
        """
        Envia um email individual
        """
        try:
            from_email = from_email or os.getenv('DEFAULT_FROM_EMAIL', 'noreply@seudominio.com')
            from_name = from_name or os.getenv('DEFAULT_FROM_NAME', 'Sistema de Prospecção')
            
            payload = {
                "recipients": [{"address": to_email}],
                "content": {
                    "from": {
                        "email": from_email,
                        "name": from_name
                    },
                    "subject": subject,
                    "html": content,
                    "text": self._html_to_text(content)
                }
            }
            
            response = requests.post(
                f"{self.base_url}/transmissions",
                json=payload,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'message': 'Email enviado com sucesso',
                    'transmission_id': result.get('results', {}).get('id'),
                    'accepted': result.get('results', {}).get('total_accepted_recipients', 0),
                    'rejected': result.get('results', {}).get('total_rejected_recipients', 0)
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro da API: {response.status_code}',
                    'details': response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Erro de conexão: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro interno: {str(e)}'
            }
    
    def send_bulk_email(self, recipients: List[Dict], subject: str, content: str,
                       from_email: str = None, from_name: str = None) -> Dict:
        """
        Envia emails em massa
        recipients: [{'email': 'teste@teste.com', 'name': 'Nome Empresa', 'substitutions': {...}}]
        """
        try:
            from_email = from_email or os.getenv('DEFAULT_FROM_EMAIL', 'noreply@seudominio.com')
            from_name = from_name or os.getenv('DEFAULT_FROM_NAME', 'Sistema de Prospecção')
            
            # Preparar destinatários
            spark_recipients = []
            for recipient in recipients:
                spark_recipient = {
                    "address": recipient['email']
                }
                
                # Adicionar dados de substituição se existirem
                if 'substitutions' in recipient:
                    spark_recipient['substitution_data'] = recipient['substitutions']
                
                spark_recipients.append(spark_recipient)
            
            payload = {
                "recipients": spark_recipients,
                "content": {
                    "from": {
                        "email": from_email,
                        "name": from_name
                    },
                    "subject": subject,
                    "html": content,
                    "text": self._html_to_text(content)
                }
            }
            
            response = requests.post(
                f"{self.base_url}/transmissions",
                json=payload,
                headers=self.headers,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'message': 'Emails enviados com sucesso',
                    'transmission_id': result.get('results', {}).get('id'),
                    'accepted': result.get('results', {}).get('total_accepted_recipients', 0),
                    'rejected': result.get('results', {}).get('total_rejected_recipients', 0),
                    'total_sent': len(recipients)
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro da API: {response.status_code}',
                    'details': response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Erro de conexão: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro interno: {str(e)}'
            }
    
    def get_email_templates(self) -> Dict:
        """
        Retorna templates pré-definidos de email
        """
        return {
            'prospeccao_inicial': {
                'subject': 'Oportunidade de Negócio - {{empresa_nome}}',
                'html': '''
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <h2>Olá, {{empresa_nome}}!</h2>
                    
                    <p>Espero que esta mensagem encontre vocês bem.</p>
                    
                    <p>Meu nome é <strong>{{nome_vendedor}}</strong> e represento a <strong>{{empresa_vendedor}}</strong>. 
                    Entramos em contato porque identificamos uma oportunidade interessante para sua empresa em {{cidade}} - {{uf}}.</p>
                    
                    <p>Nossa solução pode ajudar empresas como a sua a:</p>
                    <ul>
                        <li>Aumentar a eficiência operacional</li>
                        <li>Reduzir custos</li>
                        <li>Melhorar a experiência do cliente</li>
                    </ul>
                    
                    <p>Gostaria de agendar uma breve conversa de 15 minutos para apresentar nossa proposta?</p>
                    
                    <p>Aguardo seu retorno.</p>
                    
                    <p>Atenciosamente,<br>
                    <strong>{{nome_vendedor}}</strong><br>
                    {{empresa_vendedor}}<br>
                    {{telefone_vendedor}}<br>
                    {{email_vendedor}}</p>
                </body>
                </html>
                '''
            },
            'follow_up': {
                'subject': 'Acompanhamento - {{empresa_nome}}',
                'html': '''
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <h2>Olá novamente, {{empresa_nome}}!</h2>
                    
                    <p>Espero que estejam bem por aí em {{cidade}}.</p>
                    
                    <p>Enviei uma mensagem há alguns dias sobre uma oportunidade para sua empresa, 
                    mas imagino que devem estar ocupados com a rotina.</p>
                    
                    <p>Nossa proposta pode realmente fazer a diferença para empresas do seu porte ({{porte}}) 
                    no setor de {{ramo_atividade}}.</p>
                    
                    <p>Que tal conversarmos rapidamente? Posso ligar no {{telefone}} em um horário conveniente.</p>
                    
                    <p>Atenciosamente,<br>
                    <strong>{{nome_vendedor}}</strong></p>
                </body>
                </html>
                '''
            },
            'proposta_comercial': {
                'subject': 'Proposta Comercial - {{empresa_nome}}',
                'html': '''
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <h2>Proposta Comercial para {{empresa_nome}}</h2>
                    
                    <p>Conforme nossa conversa, segue nossa proposta personalizada:</p>
                    
                    <div style="background: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h3>Resumo da Proposta:</h3>
                        <p><strong>Empresa:</strong> {{empresa_nome}}<br>
                        <strong>Localização:</strong> {{cidade}} - {{uf}}<br>
                        <strong>Porte:</strong> {{porte}}<br>
                        <strong>Investimento:</strong> {{valor_proposta}}</p>
                    </div>
                    
                    <p>Esta proposta é válida por 30 dias e inclui:</p>
                    <ul>
                        <li>Implementação completa</li>
                        <li>Treinamento da equipe</li>
                        <li>Suporte por 12 meses</li>
                    </ul>
                    
                    <p>Estou à disposição para esclarecer qualquer dúvida.</p>
                    
                    <p>Atenciosamente,<br>
                    <strong>{{nome_vendedor}}</strong></p>
                </body>
                </html>
                '''
            }
        }
    
    def _html_to_text(self, html_content: str) -> str:
        """
        Converte HTML básico para texto simples
        """
        import re
        
        # Remove tags HTML
        text = re.sub('<[^<]+?>', '', html_content)
        
        # Limpa espaços extras
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        return text.strip()
    
    def validate_api_key(self) -> Dict:
        """
        Valida se a API key está funcionando
        """
        try:
            response = requests.get(
                f"{self.base_url}/account",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'API key válida',
                    'account_info': response.json()
                }
            else:
                return {
                    'success': False,
                    'error': f'API key inválida: {response.status_code}',
                    'details': response.text
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro ao validar API: {str(e)}'
            }