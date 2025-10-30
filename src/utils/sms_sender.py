import requests
import os
from typing import List, Dict, Optional
import base64
import logging

class TwilioSMSSender:
    """
    Serviço para envio de SMS via Twilio API
    """
    
    def __init__(self, account_sid: Optional[str] = None, auth_token: Optional[str] = None, from_number: Optional[str] = None):
        self.account_sid = account_sid or os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = auth_token or os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = from_number or os.getenv('TWILIO_FROM_NUMBER')
        self.base_url = f'https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}'
        
        # Criar headers de autenticação
        if self.account_sid and self.auth_token:
            credentials = f"{self.account_sid}:{self.auth_token}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            self.headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        else:
            self.headers = {}
    
    def send_single_sms(self, to_number: str, message: str) -> Dict:
        """
        Envia um SMS individual
        """
        try:
            if not self.account_sid or not self.auth_token or not self.from_number:
                return {
                    'success': False,
                    'error': 'Configuração Twilio incompleta'
                }
            
            # Limpar e formatar número
            to_number = self._format_phone_number(to_number)
            if not to_number:
                return {
                    'success': False,
                    'error': 'Número de telefone inválido'
                }
            
            # Dados para envio
            data = {
                'From': self.from_number,
                'To': to_number,
                'Body': message
            }
            
            response = requests.post(
                f"{self.base_url}/Messages.json",
                data=data,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 201:
                result = response.json()
                return {
                    'success': True,
                    'message': 'SMS enviado com sucesso',
                    'sid': result.get('sid'),
                    'status': result.get('status'),
                    'to': result.get('to'),
                    'price': result.get('price'),
                    'price_unit': result.get('price_unit')
                }
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                return {
                    'success': False,
                    'error': f'Erro da API: {response.status_code}',
                    'details': error_data.get('message', response.text),
                    'error_code': error_data.get('code')
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
    
    def send_bulk_sms(self, recipients: List[Dict], message_template: str) -> Dict:
        """
        Envia SMS em massa
        recipients: [{'phone': '+5511999999999', 'name': 'Nome Empresa', 'substitutions': {...}}]
        """
        results = {
            'success': True,
            'total_sent': 0,
            'total_failed': 0,
            'sent_messages': [],
            'failed_messages': [],
            'errors': []
        }
        
        for recipient in recipients:
            try:
                phone = recipient.get('phone')
                if not phone:
                    continue
                
                # Aplicar substituições na mensagem
                message = message_template
                if 'substitutions' in recipient:
                    for key, value in recipient['substitutions'].items():
                        message = message.replace(f'{{{{{key}}}}}', str(value))
                
                # Enviar SMS
                result = self.send_single_sms(phone, message)
                
                if result['success']:
                    results['total_sent'] += 1
                    results['sent_messages'].append({
                        'phone': phone,
                        'sid': result.get('sid'),
                        'status': result.get('status')
                    })
                else:
                    results['total_failed'] += 1
                    results['failed_messages'].append({
                        'phone': phone,
                        'error': result.get('error')
                    })
                    results['errors'].append(result.get('error'))
                    
            except Exception as e:
                results['total_failed'] += 1
                results['errors'].append(f'Erro ao processar {recipient.get("phone", "N/A")}: {str(e)}')
        
        if results['total_failed'] > 0 and results['total_sent'] == 0:
            results['success'] = False
        
        return results
    
    def get_sms_templates(self) -> Dict:
        """
        Retorna templates pré-definidos de SMS
        """
        return {
            'prospeccao_inicial': {
                'name': 'Prospecção Inicial',
                'message': '''Olá {{empresa_nome}}! Sou {{nome_vendedor}} da {{empresa_vendedor}}. Identificamos uma oportunidade para sua empresa em {{cidade}}. Podemos conversar? {{telefone_vendedor}}'''
            },
            'follow_up': {
                'name': 'Follow-up',
                'message': '''Oi {{empresa_nome}}! Falei sobre uma oportunidade há alguns dias. Que tal conversarmos rapidamente? {{nome_vendedor}} - {{telefone_vendedor}}'''
            },
            'agendamento': {
                'name': 'Agendamento',
                'message': '''{{empresa_nome}}, podemos agendar uma conversa de 15min sobre nossa proposta? Responda com SIM ou ligue {{telefone_vendedor}}. {{nome_vendedor}}'''
            },
            'proposta_enviada': {
                'name': 'Proposta Enviada',
                'message': '''{{empresa_nome}}, enviamos nossa proposta por email. Dúvidas? Ligue {{telefone_vendedor}}. {{nome_vendedor}} - {{empresa_vendedor}}'''
            }
        }
    
    def _format_phone_number(self, phone: str) -> Optional[str]:
        """
        Formata número de telefone para padrão internacional (+55...)
        """
        if not phone:
            return None
        
        # Remover caracteres não numéricos
        clean_phone = ''.join(filter(str.isdigit, phone))
        
        # Se já tem código do país, manter
        if clean_phone.startswith('55') and len(clean_phone) >= 12:
            return f'+{clean_phone}'
        
        # Adicionar código do Brasil se necessário
        if len(clean_phone) == 11:  # Celular com DDD
            return f'+55{clean_phone}'
        elif len(clean_phone) == 10:  # Fixo com DDD
            return f'+55{clean_phone}'
        elif len(clean_phone) == 9:  # Celular sem DDD (assumir SP)
            return f'+5511{clean_phone}'
        elif len(clean_phone) == 8:  # Fixo sem DDD (assumir SP)
            return f'+5511{clean_phone}'
        
        return None
    
    def validate_credentials(self) -> Dict:
        """
        Valida se as credenciais do Twilio estão funcionando
        """
        try:
            if not self.account_sid or not self.auth_token:
                return {
                    'success': False,
                    'error': 'Credenciais Twilio não configuradas'
                }
            
            response = requests.get(
                f"{self.base_url}.json",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                account_info = response.json()
                return {
                    'success': True,
                    'message': 'Credenciais válidas',
                    'account_info': {
                        'friendly_name': account_info.get('friendly_name'),
                        'status': account_info.get('status'),
                        'type': account_info.get('type')
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f'Credenciais inválidas: {response.status_code}',
                    'details': response.text
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro ao validar credenciais: {str(e)}'
            }
    
    def get_account_balance(self) -> Dict:
        """
        Consulta saldo da conta Twilio
        """
        try:
            response = requests.get(
                f"{self.base_url}/Balance.json",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                balance_info = response.json()
                return {
                    'success': True,
                    'balance': balance_info.get('balance'),
                    'currency': balance_info.get('currency')
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro ao consultar saldo: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Erro ao consultar saldo: {str(e)}'
            }