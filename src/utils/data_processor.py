import pandas as pd
import os
from werkzeug.utils import secure_filename

class DataProcessor:
    """Processador de arquivos de dados empresariais"""
    
    # Mapeamento de colunas para diferentes formatos
    COLUMN_MAPPING = {
        'cnpj': ['CNPJ', 'cnpj', 'Cnpj'],
        'matriz_filial': ['Matriz ou Filial'],
        'razao_social': ['Razao Social', 'Razão Social', 'Nome', 'Empresa'],
        'nome_fantasia': ['Nome Fantasia', 'Fantasia', 'nome_fantasia'],
        'situacao': ['Situacao', 'Situação'],
        'data_situacao': ['Data Situacao', 'Data Situação'],
        'natureza_juridica': ['Natureza Juridica', 'Natureza Jurídica'],
        'abertura': ['Abertura'],
        'cnae': ['CNAE'],
        'ramo_atividade': ['Ramo de Atividade', 'Atividade'],
        'cnae_secundario': ['CNAE secundario', 'CNAE Secundário'],
        'tipo_logradouro': ['Tipo Logradouro'],
        'logradouro': ['Logradouro', 'Endereço', 'Endereco'],
        'numero': ['Numero', 'Número'],
        'complemento': ['Complemento'],
        'bairro': ['Bairro'],
        'cep': ['CEP', 'cep', 'Cep'],
        'uf': ['UF', 'uf', 'Estado'],
        'municipio': ['Municipio', 'Município', 'Cidade'],
        'telefone1': ['Telefone1 Completo', 'Telefone', 'Phone', 'Telefone1'],
        'telefone2': ['Telefone2 Completo', 'Telefone2'],
        'email': ['E-mail', 'Email', 'email', 'E-Mail'],
        'capital_social': ['Capital Social'],
        'porte': ['Porte'],
        'simples_nacional': ['Simples Nacional'],
        'mei': ['MEI'],
        'socios': ['Socio(s)', 'Sócios'],
        'tributacao': ['Tributacao', 'Tributação'],
        'dividas_fgts': ['Dívidas FGTS'],
        'dividas_nao_previdenciarias': ['Dívidas Não Previdenciárias'],
        'dividas_previdenciarias': ['Dívidas Previdenciárias']
    }
    
    def __init__(self, upload_folder='uploads'):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)
    
    def allowed_file(self, filename):
        """Verifica se o arquivo é permitido"""
        ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    def save_file(self, file):
        """Salva o arquivo de upload"""
        if not file or not self.allowed_file(file.filename):
            return None, "Tipo de arquivo não permitido"
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(self.upload_folder, filename)
        file.save(filepath)
        return filepath, None
    
    def read_file(self, filepath):
        """Lê arquivo Excel ou CSV"""
        try:
            if filepath.endswith('.xlsx') or filepath.endswith('.xls'):
                df = pd.read_excel(filepath)
            else:
                # Tentar diferentes separadores para CSV
                for sep in [',', ';', '\t']:
                    try:
                        df = pd.read_csv(filepath, sep=sep)
                        if len(df.columns) > 1:  # Se encontrou colunas
                            break
                    except:
                        continue
                else:
                    df = pd.read_csv(filepath)  # Fallback padrão
            
            return df, None
        except Exception as e:
            return None, f"Erro ao ler arquivo: {str(e)}"
    
    def map_columns(self, df):
        """Mapeia colunas do arquivo para padrão interno"""
        mapped_columns = {}
        
        for standard_col, possible_names in self.COLUMN_MAPPING.items():
            for col_name in possible_names:
                if col_name in df.columns:
                    mapped_columns[standard_col] = col_name
                    break
        
        return mapped_columns
    
    def validate_data(self, df, column_mapping):
        """Valida se os dados essenciais estão presentes"""
        required_fields = ['cep', 'razao_social']
        missing_fields = []
        
        for field in required_fields:
            if field not in column_mapping:
                missing_fields.append(field)
        
        if missing_fields:
            return False, f"Campos obrigatórios não encontrados: {', '.join(missing_fields)}"
        
        return True, None
    
    def clean_data(self, df, column_mapping):
        """Limpa e padroniza os dados"""
        import pandas as pd
        
        cleaned_data = []
        
        for index, row in df.iterrows():
            cleaned_row = {}
            
            # Mapear dados usando o mapeamento de colunas
            for standard_col, original_col in column_mapping.items():
                value = row.get(original_col, '')
                
                # Converter NaN para string vazia
                if pd.isna(value):
                    value = ''
                
                # Limpeza específica por tipo de campo
                if standard_col == 'cep':
                    value = str(value).replace('-', '').replace('.', '').replace('nan', '').zfill(8) if value else ''
                elif standard_col in ['telefone1', 'telefone2']:
                    value = str(value).replace('(', '').replace(')', '').replace('-', '').replace(' ', '').replace('nan', '') if value else ''
                elif standard_col == 'email':
                    value = str(value).lower().strip().replace('nan', '') if value else ''
                elif standard_col == 'cnpj':
                    value = str(value).replace('.', '').replace('/', '').replace('-', '').replace('nan', '') if value else ''
                elif standard_col in ['capital_social']:
                    try:
                        value = float(value) if value and str(value) != 'nan' else 0.0
                    except:
                        value = 0.0
                elif standard_col in ['mei']:
                    value = bool(value) if value and str(value).lower() not in ['nan', 'false', '0', ''] else False
                else:
                    value = str(value).replace('nan', '') if value else ''
                
                cleaned_row[standard_col] = value
            
            cleaned_data.append(cleaned_row)
        
        return cleaned_data
    
    def process_file(self, file):
        """Processa um arquivo completo"""
        # 1. Salvar arquivo
        filepath, error = self.save_file(file)
        if error:
            return None, error
        
        try:
            # 2. Ler arquivo
            df, error = self.read_file(filepath)
            if error:
                return None, error
            
            # 3. Mapear colunas
            column_mapping = self.map_columns(df)
            
            # 4. Validar dados
            is_valid, error = self.validate_data(df, column_mapping)
            if not is_valid:
                return None, error
            
            # 5. Limpar dados
            cleaned_data = self.clean_data(df, column_mapping)
            
            # 6. Remover arquivo temporário
            os.remove(filepath)
            
            return {
                'data': cleaned_data,
                'total_records': len(cleaned_data),
                'columns_found': list(column_mapping.keys()),
                'original_columns': list(df.columns)
            }, None
            
        except Exception as e:
            # Limpar arquivo em caso de erro
            if os.path.exists(filepath):
                os.remove(filepath)
            return None, f"Erro no processamento: {str(e)}"