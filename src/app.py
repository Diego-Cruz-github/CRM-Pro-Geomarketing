from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
from utils.data_processor import DataProcessor
from utils.geocoding import GeocodingService
from utils.email_sender import SparkPostEmailSender
from utils.sms_sender import TwilioSMSSender

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max

# Criar pasta de uploads se não existir
os.makedirs('uploads', exist_ok=True)

# Inicializar serviços
data_processor = DataProcessor()
geocoding_service = GeocodingService()
email_sender = SparkPostEmailSender()
sms_sender = TwilioSMSSender()

# In-memory data storage (production would use PostgreSQL/Redis)
uploaded_data = []

def reset_all_data():
    """Reset all application data completely"
    global uploaded_data, undo_stack
    uploaded_data = []
    undo_stack = []

# Sample data for demonstration
sample_data = [
    {
        'cnpj': '12.345.678/0001-90',
        'razao_social': 'Empresa Demo SP',
        'nome_fantasia': 'Demo SP',
        'situacao': 'ATIVA',
        'cep': '01310-100',
        'endereco_completo': 'Av. Paulista, 1000, São Paulo, SP',
        'latitude': -23.5505,
        'longitude': -46.6333,
        'uf': 'SP',
        'municipio': 'São Paulo',
        'bairro': 'Bela Vista',
        'telefone1': '(11) 99999-1001',
        'telefone2': '(11) 3333-1001',
        'email': 'contato@demosp.com.br',
        'porte': 'MEDIO',
        'cnae': '6201-5',
        'ramo_atividade': 'Desenvolvimento de software',
        'capital_social': 500000.00,
        'mei': False,
        'pipeline_status': 'nao_contactado',
        'data_upload': '2025-01-01T10:00:00',
        'data_ultima_interacao': None,
        'observacoes': '',
        'geo_source': 'ViaCEP'
    },
    {
        'cnpj': '98.765.432/0001-10',
        'razao_social': 'Tech Solutions RJ',
        'nome_fantasia': 'TechRJ',
        'situacao': 'ATIVA',
        'cep': '20040-020',
        'endereco_completo': 'Av. Rio Branco, 500, Rio de Janeiro, RJ',
        'latitude': -22.9068,
        'longitude': -43.1729,
        'uf': 'RJ',
        'municipio': 'Rio de Janeiro',
        'bairro': 'Centro',
        'telefone1': '(21) 98888-2002',
        'telefone2': '(21) 2222-2002',
        'email': 'vendas@techrj.com.br',
        'porte': 'GRANDE',
        'cnae': '6201-5',
        'ramo_atividade': 'Consultoria em TI',
        'capital_social': 1000000.00,
        'mei': False,
        'pipeline_status': 'nao_contactado',
        'data_upload': '2025-01-01T10:00:00',
        'data_ultima_interacao': '2025-01-15T14:30:00',
        'observacoes': 'Cliente interessado em consultoria',
        'geo_source': 'ViaCEP'
    },
    {
        'cnpj': '11.222.333/0001-44',
        'razao_social': 'Inovação MG LTDA',
        'nome_fantasia': 'InovaMG',
        'situacao': 'ATIVA',
        'cep': '30112-000',
        'endereco_completo': 'Rua da Bahia, 1200, Belo Horizonte, MG',
        'latitude': -19.9167,
        'longitude': -43.9345,
        'uf': 'MG',
        'municipio': 'Belo Horizonte',
        'bairro': 'Centro',
        'telefone1': '(31) 97777-3003',
        'telefone2': '',
        'email': 'contato@inovamg.com.br',
        'porte': 'PEQUENO',
        'cnae': '7020-4',
        'ramo_atividade': 'Consultoria empresarial',
        'capital_social': 100000.00,
        'mei': False,
        'pipeline_status': 'nao_contactado',
        'data_upload': '2025-01-01T10:00:00',
        'data_ultima_interacao': '2025-01-20T09:15:00',
        'observacoes': 'Proposta em análise',
        'geo_source': 'Nominatim'
    },
    {
        'cnpj': '55.666.777/0001-88',
        'razao_social': 'Digital RS Serviços',
        'nome_fantasia': 'DigitalRS',
        'situacao': 'ATIVA',
        'cep': '90010-150',
        'endereco_completo': 'Rua dos Andradas, 800, Porto Alegre, RS',
        'latitude': -30.0346,
        'longitude': -51.2177,
        'uf': 'RS',
        'municipio': 'Porto Alegre',
        'bairro': 'Centro Histórico',
        'telefone1': '(51) 96666-4004',
        'telefone2': '(51) 4444-4004',
        'email': 'info@digitalrs.com.br',
        'porte': 'MEDIO',
        'cnae': '6311-9',
        'ramo_atividade': 'Processamento de dados',
        'capital_social': 300000.00,
        'mei': False,
        'pipeline_status': 'negociacao',
        'data_upload': '2025-01-01T10:00:00',
        'data_ultima_interacao': '2025-01-22T16:45:00',
        'observacoes': 'Aguardando aprovação da diretoria',
        'geo_source': 'ViaCEP'
    },
    {
        'cnpj': '44.555.666/0001-22',
        'razao_social': 'StartUp BA Tech',
        'nome_fantasia': 'StartupBA',
        'situacao': 'ATIVA',
        'cep': '40070-110',
        'endereco_completo': 'Av. Sete de Setembro, 300, Salvador, BA',
        'latitude': -12.9714,
        'longitude': -38.5014,
        'uf': 'BA',
        'municipio': 'Salvador',
        'bairro': 'Centro',
        'telefone1': '(71) 95555-5005',
        'telefone2': '',
        'email': 'hello@startupba.com.br',
        'porte': 'PEQUENO',
        'cnae': '6201-5',
        'ramo_atividade': 'Desenvolvimento de aplicativos',
        'capital_social': 50000.00,
        'mei': False,
        'pipeline_status': 'fechado',
        'data_upload': '2025-01-01T10:00:00',
        'data_ultima_interacao': '2025-01-25T11:20:00',
        'observacoes': 'Contrato assinado - cliente satisfeito',
        'geo_source': 'ViaCEP'
    }
]

def ensure_sample_data():
    """Garante que sempre temos dados de exemplo disponíveis - REMOVIDO"""
    # Não carregar mais dados automáticos
    pass

@app.route('/')
def index():
    """Página principal - Geomarketing"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Página de dashboard com estatísticas"""
    return render_template('dashboard.html')

@app.route('/crm')
def crm():
    """Página de CRM/Pipeline"""
    return render_template('crm.html')

@app.route('/api/health')
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'message': 'Hugo Cabeção funcionando'
    })

@app.route('/api/load-sample-data', methods=['POST'])
def load_sample_data():
    """Carrega dados de exemplo para demonstração"""
    global uploaded_data
    uploaded_data = sample_data.copy()
    
    return jsonify({
        'success': True,
        'message': 'Dados de exemplo carregados',
        'total_records': len(uploaded_data),
        'sample_data': uploaded_data[:3]  # Primeiros 3 para demonstração
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Endpoint para upload e processamento de arquivos"""
    try:
        # Verificar se arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
        
        # Processar arquivo
        result, error = data_processor.process_file(file)
        if error:
            return jsonify({'error': error}), 400
        
        # Geocodificar uma amostra para teste (primeiros 10 registros)
        sample_data = result['data'][:10]
        geocoded_sample = geocoding_service.geocode_batch(sample_data, delay=0.2)
        
        # Salvar todos os dados para dashboard/CRM
        global uploaded_data
        all_geocoded = geocoding_service.geocode_batch(result['data'][:100], delay=0.1)  # Processar 100 para demo
        uploaded_data = all_geocoded
        
        return jsonify({
            'success': True,
            'message': 'Arquivo processado com sucesso',
            'total_records': result['total_records'],
            'columns_found': result['columns_found'],
            'original_columns': result['original_columns'],
            'sample_data': geocoded_sample[:3],  # Primeiros 3 registros com coordenadas
            'geocoded_sample_count': len(geocoded_sample)
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/dashboard/stats')
def dashboard_stats():
    """Estatísticas para o dashboard"""
    if not uploaded_data:
        return jsonify({'error': 'Nenhum dado carregado'}), 400
    
    # Calcular estatísticas
    total = len(uploaded_data)
    
    # Por UF
    ufs = {}
    portes = {}
    situacoes = {}
    geocoded = 0
    
    for item in uploaded_data:
        # Contar por UF
        uf = item.get('uf', 'N/A')
        ufs[uf] = ufs.get(uf, 0) + 1
        
        # Contar por porte
        porte = item.get('porte', 'N/A')
        portes[porte] = portes.get(porte, 0) + 1
        
        # Contar por situação
        situacao = item.get('situacao', 'N/A')
        situacoes[situacao] = situacoes.get(situacao, 0) + 1
        
        # Contar geocodificados
        if item.get('latitude') and item.get('longitude'):
            geocoded += 1
    
    # Calcular dados do CRM
    pipeline_stats = {}
    conversion_data = {}
    companies_with_contact = 0
    
    for item in uploaded_data:
        # Status do pipeline
        status = item.get('pipeline_status', 'novo')
        pipeline_stats[status] = pipeline_stats.get(status, 0) + 1
        
        # Empresas com dados de contato
        if item.get('email') or item.get('telefone1'):
            companies_with_contact += 1
    
    # Calcular taxa de conversão
    total_leads = sum(pipeline_stats.values())
    conversion_rate = round((pipeline_stats.get('fechado', 0) / total_leads) * 100, 1) if total_leads > 0 else 0
    
    return jsonify({
        # Dados originais do scan
        'total_records': total,
        'geocoded_records': geocoded,
        'geocoding_rate': round((geocoded / total) * 100, 1) if total > 0 else 0,
        'by_uf': dict(sorted(ufs.items(), key=lambda x: x[1], reverse=True)[:10]),
        'by_porte': portes,
        'by_situacao': situacoes,
        
        # Novos dados do CRM
        'pipeline_stats': pipeline_stats,
        'conversion_rate': conversion_rate,
        'companies_with_contact': companies_with_contact,
        'contact_rate': round((companies_with_contact / total) * 100, 1) if total > 0 else 0,
        'leads_in_progress': pipeline_stats.get('negociacao', 0) + pipeline_stats.get('email_enviado', 0) + pipeline_stats.get('sms_enviado', 0) + pipeline_stats.get('email_sms_enviados', 0)
    })

@app.route('/api/crm/companies')
def get_companies():
    """Lista empresas para CRM"""
    if not uploaded_data:
        return jsonify({'error': 'Nenhum dado carregado'}), 400
    
    # Adicionar status de pipeline se não existir
    for company in uploaded_data:
        if 'pipeline_status' not in company:
            company['pipeline_status'] = 'nao_contactado'
        if 'last_contact' not in company:
            company['last_contact'] = None
        if 'notes' not in company:
            company['notes'] = ''
    
    return jsonify({
        'companies': uploaded_data,
        'total': len(uploaded_data)
    })

@app.route('/api/crm/company/<int:company_id>/status', methods=['PUT'])
def update_company_status(company_id):
    """Atualiza status do pipeline de uma empresa"""
    if not uploaded_data or company_id >= len(uploaded_data):
        return jsonify({'error': 'Empresa não encontrada'}), 404
    
    data = request.get_json()
    new_status = data.get('status')
    notes = data.get('notes', '')
    
    valid_statuses = ['nao_contactado', 'email_enviado', 'sms_enviado', 'email_sms_enviados', 'negociacao', 'fechado', 'perdido']
    if new_status not in valid_statuses:
        return jsonify({'error': 'Status inválido'}), 400
    
    # Atualizar empresa
    uploaded_data[company_id]['pipeline_status'] = new_status
    uploaded_data[company_id]['notes'] = notes
    uploaded_data[company_id]['last_contact'] = datetime.now().isoformat()
    
    return jsonify({
        'success': True,
        'company': uploaded_data[company_id]
    })

@app.route('/api/crm/stats')
def crm_stats():
    """Estatísticas do pipeline CRM"""
    if not uploaded_data:
        return jsonify({'error': 'Nenhum dado carregado'}), 400
    
    # Contar por status
    status_counts = {}
    for company in uploaded_data:
        status = company.get('pipeline_status', 'novo')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    return jsonify({
        'total_companies': len(uploaded_data),
        'pipeline_counts': status_counts
    })

@app.route('/api/email/send', methods=['POST'])
def send_email():
    """Envia email individual"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['to_email', 'subject', 'content']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Enviar email
        result = email_sender.send_single_email(
            to_email=data['to_email'],
            subject=data['subject'],
            content=data['content'],
            from_email=data.get('from_email'),
            from_name=data.get('from_name')
        )
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/email/campaign', methods=['POST'])
def send_email_campaign():
    """Envia campanha de email em massa"""
    try:
        data = request.get_json()
        
        # Validar dados
        if not data.get('template_type'):
            return jsonify({'error': 'Tipo de template obrigatório'}), 400
        
        if not data.get('company_ids') or not isinstance(data['company_ids'], list):
            return jsonify({'error': 'Lista de empresas obrigatória'}), 400
        
        # Obter template
        templates = email_sender.get_email_templates()
        template = templates.get(data['template_type'])
        if not template:
            return jsonify({'error': 'Template não encontrado'}), 400
        
        # Preparar destinatários
        recipients = []
        for company_id in data['company_ids']:
            if company_id < len(uploaded_data):
                company = uploaded_data[company_id]
                if company.get('email'):
                    recipients.append({
                        'email': company['email'],
                        'substitutions': {
                            'empresa_nome': company.get('razao_social', 'Empresa'),
                            'cidade': company.get('municipio', 'Sua cidade'),
                            'uf': company.get('uf', 'UF'),
                            'porte': company.get('porte', 'Médio'),
                            'ramo_atividade': company.get('ramo_atividade', 'Sua área'),
                            'telefone': company.get('telefone1', ''),
                            'nome_vendedor': data.get('sender_name', 'Equipe Comercial'),
                            'empresa_vendedor': data.get('sender_company', 'Nossa Empresa'),
                            'telefone_vendedor': data.get('sender_phone', ''),
                            'email_vendedor': data.get('sender_email', ''),
                            'valor_proposta': data.get('proposal_value', 'A combinar')
                        }
                    })
        
        if not recipients:
            return jsonify({'error': 'Nenhum destinatário válido encontrado'}), 400
        
        # Enviar campanha
        result = email_sender.send_bulk_email(
            recipients=recipients,
            subject=template['subject'],
            content=template['html']
        )
        
        # Atualizar status das empresas após envio bem-sucedido
        if result.get('success') and result.get('total_sent', 0) > 0:
            for company_id in data['company_ids']:
                if company_id < len(uploaded_data):
                    company = uploaded_data[company_id]
                    if company.get('email'):
                        # Determinar novo status baseado no status atual
                        current_status = company.get('pipeline_status', 'nao_contactado')
                        if current_status == 'sms_enviado':
                            new_status = 'email_sms_enviados'
                        else:
                            new_status = 'email_enviado'
                        
                        # Atualizar status e observações
                        company['pipeline_status'] = new_status
                        company['data_ultima_interacao'] = datetime.now().isoformat()
                        
                        # Adicionar observação sobre o envio
                        current_obs = company.get('observacoes', '')
                        template_name = data.get('template_type', 'desconhecido')
                        new_obs = f"📧 Email enviado ({template_name}) - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                        
                        if current_obs:
                            company['observacoes'] = f"{current_obs}\n{new_obs}"
                        else:
                            company['observacoes'] = new_obs
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/email/templates')
def get_email_templates():
    """Lista templates disponíveis"""
    templates = email_sender.get_email_templates()
    return jsonify({
        'templates': list(templates.keys()),
        'details': {
            name: {'subject': template['subject']}
            for name, template in templates.items()
        }
    })

@app.route('/api/email/validate', methods=['POST'])
def validate_email_config():
    """Valida configuração do SparkPost"""
    result = email_sender.validate_api_key()
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

@app.route('/api/sms/send', methods=['POST'])
def send_sms():
    """Envia SMS individual"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['to_number', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Enviar SMS
        result = sms_sender.send_single_sms(
            to_number=data['to_number'],
            message=data['message']
        )
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/sms/campaign', methods=['POST'])
def send_sms_campaign():
    """Envia campanha de SMS em massa"""
    try:
        data = request.get_json()
        
        # Validar dados
        if not data.get('template_type'):
            return jsonify({'error': 'Tipo de template obrigatório'}), 400
        
        if not data.get('company_ids') or not isinstance(data['company_ids'], list):
            return jsonify({'error': 'Lista de empresas obrigatória'}), 400
        
        # Obter template
        templates = sms_sender.get_sms_templates()
        template = templates.get(data['template_type'])
        if not template:
            return jsonify({'error': 'Template não encontrado'}), 400
        
        # Preparar destinatários
        recipients = []
        for company_id in data['company_ids']:
            if company_id < len(uploaded_data):
                company = uploaded_data[company_id]
                phone = company.get('telefone1') or company.get('telefone2')
                if phone:
                    recipients.append({
                        'phone': phone,
                        'substitutions': {
                            'empresa_nome': company.get('razao_social', 'Empresa'),
                            'cidade': company.get('municipio', 'Sua cidade'),
                            'uf': company.get('uf', 'UF'),
                            'nome_vendedor': data.get('sender_name', 'Equipe Comercial'),
                            'empresa_vendedor': data.get('sender_company', 'Nossa Empresa'),
                            'telefone_vendedor': data.get('sender_phone', ''),
                        }
                    })
        
        if not recipients:
            return jsonify({'error': 'Nenhum destinatário com telefone encontrado'}), 400
        
        # Enviar campanha
        result = sms_sender.send_bulk_sms(
            recipients=recipients,
            message_template=template['message']
        )
        
        # Atualizar status das empresas após envio bem-sucedido
        if result.get('success') and result.get('total_sent', 0) > 0:
            for company_id in data['company_ids']:
                if company_id < len(uploaded_data):
                    company = uploaded_data[company_id]
                    phone = company.get('telefone1') or company.get('telefone2')
                    if phone:
                        # Determinar novo status baseado no status atual
                        current_status = company.get('pipeline_status', 'nao_contactado')
                        if current_status == 'email_enviado':
                            new_status = 'email_sms_enviados'
                        else:
                            new_status = 'sms_enviado'
                        
                        # Atualizar status e observações
                        company['pipeline_status'] = new_status
                        company['data_ultima_interacao'] = datetime.now().isoformat()
                        
                        # Adicionar observação sobre o envio
                        current_obs = company.get('observacoes', '')
                        template_name = data.get('template_type', 'desconhecido')
                        new_obs = f"📱 SMS enviado ({template_name}) - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                        
                        if current_obs:
                            company['observacoes'] = f"{current_obs}\n{new_obs}"
                        else:
                            company['observacoes'] = new_obs
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/sms/templates')
def get_sms_templates():
    """Lista templates de SMS disponíveis"""
    templates = sms_sender.get_sms_templates()
    return jsonify({
        'templates': list(templates.keys()),
        'details': templates
    })

@app.route('/api/sms/validate', methods=['POST'])
def validate_sms_config():
    """Valida configuração do Twilio"""
    result = sms_sender.validate_credentials()
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

@app.route('/api/sms/balance')
def get_sms_balance():
    """Consulta saldo da conta Twilio"""
    result = sms_sender.get_account_balance()
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

# Armazenamento para operações de desfazer
undo_stack = []

@app.route('/api/crm/company/add', methods=['POST'])
def add_company():
    """Adiciona uma nova empresa manualmente"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['razao_social']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Criar nova empresa
        new_company = {
            'cnpj': data.get('cnpj', ''),
            'razao_social': data.get('razao_social'),
            'nome_fantasia': data.get('nome_fantasia', ''),
            'situacao': data.get('situacao', 'ATIVA'),
            'cep': data.get('cep', ''),
            'endereco_completo': data.get('endereco_completo', ''),
            'latitude': None,
            'longitude': None,
            'uf': data.get('uf', ''),
            'municipio': data.get('municipio', ''),
            'bairro': data.get('bairro', ''),
            'telefone1': data.get('telefone1', ''),
            'telefone2': data.get('telefone2', ''),
            'email': data.get('email', ''),
            'porte': data.get('porte', ''),
            'cnae': data.get('cnae', ''),
            'ramo_atividade': data.get('ramo_atividade', ''),
            'capital_social': float(data.get('capital_social', 0)) if data.get('capital_social') else 0,
            'mei': bool(data.get('mei', False)),
            'pipeline_status': 'nao_contactado',
            'data_upload': datetime.now().isoformat(),
            'data_ultima_interacao': None,
            'observacoes': data.get('observacoes', ''),
            'geo_source': 'Manual'
        }
        
        # Salvar estado atual para desfazer
        save_undo_state('add_company')
        
        # Adicionar empresa
        global uploaded_data
        uploaded_data.append(new_company)
        
        return jsonify({
            'success': True,
            'message': 'Empresa adicionada com sucesso',
            'company': new_company,
            'total_companies': len(uploaded_data)
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/crm/company/<int:company_id>/update', methods=['PUT'])
def update_company(company_id):
    """Atualiza uma empresa existente"""
    try:
        if not uploaded_data or company_id >= len(uploaded_data):
            return jsonify({'error': 'Empresa não encontrada'}), 404
        
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['razao_social']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo obrigatório: {field}'}), 400
        
        # Salvar estado atual para desfazer
        save_undo_state('update_company')
        
        # Manter dados existentes importantes
        existing_company = uploaded_data[company_id]
        
        # Atualizar empresa
        uploaded_data[company_id].update({
            'cnpj': data.get('cnpj', ''),
            'razao_social': data.get('razao_social'),
            'nome_fantasia': data.get('nome_fantasia', ''),
            'situacao': data.get('situacao', 'ATIVA'),
            'cep': data.get('cep', ''),
            'endereco_completo': data.get('endereco_completo', ''),
            'uf': data.get('uf', ''),
            'municipio': data.get('municipio', ''),
            'bairro': data.get('bairro', ''),
            'telefone1': data.get('telefone1', ''),
            'telefone2': data.get('telefone2', ''),
            'email': data.get('email', ''),
            'porte': data.get('porte', ''),
            'cnae': data.get('cnae', ''),
            'ramo_atividade': data.get('ramo_atividade', ''),
            'capital_social': float(data.get('capital_social', 0)) if data.get('capital_social') else 0,
            'mei': bool(data.get('mei', False)),
            'observacoes': data.get('observacoes', ''),
            'data_ultima_interacao': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'message': 'Empresa atualizada com sucesso',
            'company': uploaded_data[company_id],
            'total_companies': len(uploaded_data)
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/clear-data', methods=['POST'])
def clear_data():
    """Limpa todos os dados carregados"""
    try:
        # Salvar estado atual para desfazer
        save_undo_state('clear_data')
        
        global uploaded_data
        uploaded_data = []
        
        return jsonify({
            'success': True,
            'message': 'Todos os dados foram limpos'
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/reset-all', methods=['POST'])
def reset_all():
    """Reseta completamente todos os dados e histórico"""
    try:
        reset_all_data()
        
        return jsonify({
            'success': True,
            'message': 'Aplicação resetada completamente - todos os dados e histórico removidos'
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/undo', methods=['POST'])
def undo_action():
    """Desfaz a última ação"""
    try:
        global uploaded_data, undo_stack
        
        if not undo_stack:
            return jsonify({'error': 'Nenhuma ação para desfazer'}), 400
        
        # Restaurar estado anterior
        last_state = undo_stack.pop()
        uploaded_data = last_state['data'].copy()
        
        return jsonify({
            'success': True,
            'message': f'Ação "{last_state["action"]}" desfeita com sucesso',
            'total_companies': len(uploaded_data)
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

def save_undo_state(action_name):
    """Salva o estado atual para permitir desfazer"""
    global undo_stack, uploaded_data
    
    # Manter apenas os últimos 10 estados
    if len(undo_stack) >= 10:
        undo_stack.pop(0)
    
    undo_stack.append({
        'action': action_name,
        'data': uploaded_data.copy(),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)