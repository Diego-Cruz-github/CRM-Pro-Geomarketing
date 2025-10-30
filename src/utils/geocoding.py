import requests
import time

class GeocodingService:
    """Serviço de geocodificação usando APIs gratuitas"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Sistema-Prospeccao-B2B/1.0'
        })
        
        # Cache simples para evitar requests desnecessários
        self.cache = {}
    
    def get_coords_from_cep(self, cep, delay=0.5):
        """
        Busca coordenadas usando CEP
        Usa ViaCEP + Nominatim (OpenStreetMap)
        """
        if not cep or len(cep) != 8:
            return None
        
        # Verificar cache
        if cep in self.cache:
            return self.cache[cep]
        
        try:
            # 1. Buscar endereço no ViaCEP
            viacep_url = f'https://viacep.com.br/ws/{cep}/json/'
            response = self.session.get(viacep_url, timeout=5)
            
            if response.status_code != 200:
                return self._get_fallback_coords(cep)
            
            cep_data = response.json()
            
            # Verificar se CEP é válido
            if 'erro' in cep_data:
                return self._get_fallback_coords(cep)
            
            # 2. Montar endereço para geocodificação
            endereco_parts = []
            if cep_data.get('logradouro'):
                endereco_parts.append(cep_data['logradouro'])
            if cep_data.get('bairro'):
                endereco_parts.append(cep_data['bairro'])
            if cep_data.get('localidade'):
                endereco_parts.append(cep_data['localidade'])
            if cep_data.get('uf'):
                endereco_parts.append(cep_data['uf'])
            
            endereco_parts.append('Brasil')
            endereco_completo = ', '.join(endereco_parts)
            
            # 3. Buscar coordenadas no Nominatim
            nominatim_url = 'https://nominatim.openstreetmap.org/search'
            params = {
                'q': endereco_completo,
                'format': 'json',
                'limit': 1,
                'addressdetails': 1
            }
            
            # Delay para respeitar rate limit
            time.sleep(delay)
            
            geo_response = self.session.get(nominatim_url, params=params, timeout=10)
            
            if geo_response.status_code == 200:
                geo_data = geo_response.json()
                if geo_data:
                    coords = {
                        'lat': float(geo_data[0]['lat']),
                        'lng': float(geo_data[0]['lon']),
                        'source': 'nominatim'
                    }
                    
                    # Adicionar ao cache
                    self.cache[cep] = coords
                    return coords
            
            # Se falhou, tentar coordenadas aproximadas
            return self._get_fallback_coords(cep)
            
        except Exception as e:
            print(f"Erro na geocodificação do CEP {cep}: {e}")
            return self._get_fallback_coords(cep)
    
    def _get_fallback_coords(self, cep):
        """Coordenadas aproximadas por região do CEP"""
        if not cep or len(cep) < 2:
            return None
        
        # Coordenadas aproximadas por prefixo de CEP
        fallback_coords = {
            '01': {'lat': -23.5505, 'lng': -46.6333, 'city': 'São Paulo'},     # SP Capital
            '02': {'lat': -23.5505, 'lng': -46.6333, 'city': 'São Paulo'},     # SP Capital
            '03': {'lat': -23.5505, 'lng': -46.6333, 'city': 'São Paulo'},     # SP Capital
            '04': {'lat': -23.5505, 'lng': -46.6333, 'city': 'São Paulo'},     # SP Capital
            '05': {'lat': -23.5505, 'lng': -46.6333, 'city': 'São Paulo'},     # SP Capital
            '08': {'lat': -23.5505, 'lng': -46.6333, 'city': 'São Paulo'},     # SP Capital
            
            '20': {'lat': -22.9068, 'lng': -43.1729, 'city': 'Rio de Janeiro'}, # RJ Capital
            '21': {'lat': -22.9068, 'lng': -43.1729, 'city': 'Rio de Janeiro'}, # RJ Capital
            '22': {'lat': -22.9068, 'lng': -43.1729, 'city': 'Rio de Janeiro'}, # RJ
            '23': {'lat': -22.9068, 'lng': -43.1729, 'city': 'Rio de Janeiro'}, # RJ
            '24': {'lat': -22.9068, 'lng': -43.1729, 'city': 'Rio de Janeiro'}, # RJ
            '25': {'lat': -22.9068, 'lng': -43.1729, 'city': 'Rio de Janeiro'}, # RJ
            '26': {'lat': -22.9068, 'lng': -43.1729, 'city': 'Rio de Janeiro'}, # RJ
            '27': {'lat': -22.9068, 'lng': -43.1729, 'city': 'Rio de Janeiro'}, # RJ
            '28': {'lat': -22.9068, 'lng': -43.1729, 'city': 'Rio de Janeiro'}, # RJ
            
            '30': {'lat': -19.9167, 'lng': -43.9345, 'city': 'Belo Horizonte'}, # MG
            '31': {'lat': -19.9167, 'lng': -43.9345, 'city': 'Belo Horizonte'}, # MG
            '32': {'lat': -19.9167, 'lng': -43.9345, 'city': 'Belo Horizonte'}, # MG
            '33': {'lat': -19.9167, 'lng': -43.9345, 'city': 'Belo Horizonte'}, # MG
            '34': {'lat': -19.9167, 'lng': -43.9345, 'city': 'Belo Horizonte'}, # MG
            '35': {'lat': -19.9167, 'lng': -43.9345, 'city': 'Belo Horizonte'}, # MG
            '36': {'lat': -19.9167, 'lng': -43.9345, 'city': 'Belo Horizonte'}, # MG
            '37': {'lat': -19.9167, 'lng': -43.9345, 'city': 'Belo Horizonte'}, # MG
            '38': {'lat': -19.9167, 'lng': -43.9345, 'city': 'Belo Horizonte'}, # MG
            '39': {'lat': -19.9167, 'lng': -43.9345, 'city': 'Belo Horizonte'}, # MG
            
            '40': {'lat': -12.9714, 'lng': -38.5014, 'city': 'Salvador'},       # BA
            '41': {'lat': -12.9714, 'lng': -38.5014, 'city': 'Salvador'},       # BA
            '42': {'lat': -12.9714, 'lng': -38.5014, 'city': 'Salvador'},       # BA
            '43': {'lat': -12.9714, 'lng': -38.5014, 'city': 'Salvador'},       # BA
            '44': {'lat': -12.9714, 'lng': -38.5014, 'city': 'Salvador'},       # BA
            '45': {'lat': -12.9714, 'lng': -38.5014, 'city': 'Salvador'},       # BA
            '46': {'lat': -12.9714, 'lng': -38.5014, 'city': 'Salvador'},       # BA
            '47': {'lat': -12.9714, 'lng': -38.5014, 'city': 'Salvador'},       # BA
            '48': {'lat': -12.9714, 'lng': -38.5014, 'city': 'Salvador'},       # BA
            
            '50': {'lat': -30.0346, 'lng': -51.2177, 'city': 'Porto Alegre'},   # RS
            '51': {'lat': -30.0346, 'lng': -51.2177, 'city': 'Porto Alegre'},   # RS
            '52': {'lat': -30.0346, 'lng': -51.2177, 'city': 'Porto Alegre'},   # RS
            '53': {'lat': -30.0346, 'lng': -51.2177, 'city': 'Porto Alegre'},   # RS
            '54': {'lat': -30.0346, 'lng': -51.2177, 'city': 'Porto Alegre'},   # RS
            '55': {'lat': -30.0346, 'lng': -51.2177, 'city': 'Porto Alegre'},   # RS
            '56': {'lat': -30.0346, 'lng': -51.2177, 'city': 'Porto Alegre'},   # RS
            '57': {'lat': -30.0346, 'lng': -51.2177, 'city': 'Porto Alegre'},   # RS
            '58': {'lat': -30.0346, 'lng': -51.2177, 'city': 'Porto Alegre'},   # RS
            '59': {'lat': -30.0346, 'lng': -51.2177, 'city': 'Porto Alegre'},   # RS
            
            '60': {'lat': -3.7172, 'lng': -38.5433, 'city': 'Fortaleza'},       # CE
            '61': {'lat': -3.7172, 'lng': -38.5433, 'city': 'Fortaleza'},       # CE
            '62': {'lat': -3.7172, 'lng': -38.5433, 'city': 'Fortaleza'},       # CE
            '63': {'lat': -3.7172, 'lng': -38.5433, 'city': 'Fortaleza'},       # CE
            
            '70': {'lat': -15.7801, 'lng': -47.9292, 'city': 'Brasília'},       # DF
            '71': {'lat': -15.7801, 'lng': -47.9292, 'city': 'Brasília'},       # DF
            '72': {'lat': -15.7801, 'lng': -47.9292, 'city': 'Brasília'},       # DF
            '73': {'lat': -15.7801, 'lng': -47.9292, 'city': 'Brasília'},       # DF
            
            '80': {'lat': -25.4284, 'lng': -49.2733, 'city': 'Curitiba'},       # PR
            '81': {'lat': -25.4284, 'lng': -49.2733, 'city': 'Curitiba'},       # PR
            '82': {'lat': -25.4284, 'lng': -49.2733, 'city': 'Curitiba'},       # PR
            '83': {'lat': -25.4284, 'lng': -49.2733, 'city': 'Curitiba'},       # PR
            '84': {'lat': -25.4284, 'lng': -49.2733, 'city': 'Curitiba'},       # PR
            '85': {'lat': -25.4284, 'lng': -49.2733, 'city': 'Curitiba'},       # PR
            '86': {'lat': -25.4284, 'lng': -49.2733, 'city': 'Curitiba'},       # PR
            '87': {'lat': -25.4284, 'lng': -49.2733, 'city': 'Curitiba'},       # PR
            
            '88': {'lat': -27.5954, 'lng': -48.5480, 'city': 'Florianópolis'},  # SC
            '89': {'lat': -27.5954, 'lng': -48.5480, 'city': 'Florianópolis'},  # SC
        }
        
        prefix = cep[:2]
        coords = fallback_coords.get(prefix)
        
        if coords:
            result = coords.copy()
            result['source'] = 'fallback'
            return result
        
        # Fallback nacional (centro do Brasil)
        return {
            'lat': -15.7801,
            'lng': -47.9292,
            'source': 'fallback_nacional'
        }
    
    def geocode_batch(self, data_list, batch_size=50, delay=0.5):
        """
        Geocodifica uma lista de dados em lote
        """
        results = []
        total = len(data_list)
        
        for i, item in enumerate(data_list):
            cep = item.get('cep')
            coords = self.get_coords_from_cep(cep, delay)
            
            # Adicionar coordenadas ao item
            enhanced_item = item.copy()
            if coords:
                enhanced_item['latitude'] = coords['lat']
                enhanced_item['longitude'] = coords['lng']
                enhanced_item['geo_source'] = coords['source']
            else:
                enhanced_item['latitude'] = None
                enhanced_item['longitude'] = None
                enhanced_item['geo_source'] = 'failed'
            
            results.append(enhanced_item)
            
            # Progress feedback
            if (i + 1) % 10 == 0:
                print(f"Geocodificação: {i + 1}/{total} ({((i + 1)/total)*100:.1f}%)")
        
        return results