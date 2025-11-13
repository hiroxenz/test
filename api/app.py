from flask import Flask, request, jsonify
import requests


app = Flask(__name__)
@app.route('/api/search-tkk', methods=['GET'])
def search_tkk():
    name = request.args.get('name', 'siti')
    types = request.args.get('types', 'NAMA')  # bisa NAMA atau NIK
    
    base_url = "https://lpjk.pu.go.id"
    check_url = base_url + '/cek-tkk-di-bujk'
    
    headers_get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'id,en-US;q=0.7,en;q=0.3',
        'Connection': 'keep-alive',
    }
    
    r = requests.get(check_url, headers=headers_get)
    print (r.cookies.get_dict())
    csrf = r.cookies['csrf_cookie_name']
    print (csrf)
    cookies = dict(r.cookies)  # Corrected to proper dict format for requests
    
    search_url = base_url + '/search-tkk-di-bujk'
    
    headers_post = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'id,en-US;q=0.7,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': base_url,
        'Referer': check_url,
        'Connection': 'keep-alive',
    }
    
    files = {
        'csrf_token_name': (None, csrf),
        'parameter': (None, name),
        'nama_or_nik': (None, types),  # bisa NAMA atau NIK
        'g-recaptcha-response': (None, ''),
    }
    
    response = requests.post(search_url, headers=headers_post, files=files, cookies=cookies)
    print (response.text)
    
    # Assuming the response is JSON; adjust if needed (e.g., return response.text for raw)
    try:
        return jsonify(response.json())
    except ValueError:
        return jsonify({'error': 'Invalid JSON response', 'raw': response.text})
if __name__ == '__main__':
    app.run(debug=True)
