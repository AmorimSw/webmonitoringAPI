import json
from typing import List

def filter_brick_pf_research(brick_pf_research:dict):
    raw_participacoesSocietarias = None
    raw_historicoProfissional = None
    raw_processosJuridicos = None
    raw_contatos = None
    result = dict()

    for i, analysis in enumerate(brick_pf_research.get('data').get('analyses')):
        match analysis['type']:

            case 'PF_COMPANIES':
                raw_participacoesSocietarias = json.loads(brick_pf_research['data']['analyses'][i]['content'])

            case 'PF_EMPLOYMENT_BONDS':
                raw_historicoProfissional = json.loads(brick_pf_research['data']['analyses'][i]['content'])
                
            case 'PF_LAW_SUITS':
                raw_processosJuridicos = json.loads(brick_pf_research['data']['analyses'][i]['content'])
                
            case 'PF_ADDRESSES':
                raw_contatos:List[dict] = json.loads(brick_pf_research['data']['analyses'][i]['content'])

    # Filtro de dados de contato
    enderecos = []
    telefones = []
    emails = []
    for contato in raw_contatos:
        if contato.get('phones'):
            for telefone in contato.get('phones'):
                telefones.append(telefone)

        if contato.get('emails'):
            for email in contato.get('emails'):
                emails.append(email)
        contato.pop('phones')
        contato.pop('emails')

        enderecos.append(contato)

    historicoProfissional = []
    for empresa in raw_historicoProfissional:
        dados_empresa = dict()
        dados_empresa['cnpj'] = empresa['company_cnpj']
        dados_empresa['dataRegistro'] = empresa['entry_date']
        dados_empresa['dataDesligamento'] = empresa['exit_date']
        dados_empresa['razaoSocial'] = empresa['company_name']
        dados_empresa['setor'] = empresa['company_cnae']
        historicoProfissional.append(dados_empresa)

    result['enderecos'] = enderecos
    result['telefones'] = telefones
    result['emails'] = emails
    result['historicoProfissional'] = historicoProfissional
    result['participacoesSocietarias'] = raw_participacoesSocietarias
    result['processosJuridicos'] = raw_processosJuridicos

    return result