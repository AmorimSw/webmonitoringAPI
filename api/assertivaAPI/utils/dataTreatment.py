def personDataTreatment(rawData:dict) -> dict:
    '''Retorna um dicionário estruturado para o uso, a partir dos dados obtidos\n
    em consulta via API do Assertiva.'''

    respData:dict = rawData.get('resposta', '')
    if not respData:
        return
    finalData = dict()

    # Dados cadastrais de uma pessoa
    finalData['dadosCadastrais'] = respData.get('dadosCadastrais', {})
    
    # Telefones relacionados a ela
    phoneNumbers = []
    for key in respData.get('telefones', {}).keys():
        for item in respData['telefones'][key]:
            phoneNumbers.append(item)
    finalData['telefones'] = phoneNumbers
    
    # Endereços relacionados a ela
    finalData['enderecos'] = respData['enderecos']
    
    # Emails relacionados a ela
    finalData['emails'] = respData.get('dadosCadastrais', {})

    # Histórico profissional
    finalData['possivelHistoricoProfissional'] = respData.get('possivelHistoricoProfissional', {})

    # Participações societárias
    finalData['participacoesEmpresas'] = respData.get('participacoesEmpresas', {})

    return finalData

def companyDataTreatment(rawData:dict) -> dict:
    '''Retorna um dicionário estruturado para o uso, a partir dos dados obtidos\n
    em consulta via API do Assertiva.'''

    respData:dict = rawData.get('resposta', '')
    if not respData:
        return
    finalData = dict()

    # Dados cadastrais de uma pessoa
    finalData['dadosCadastrais'] = respData.get('dadosCadastrais', {})
    
    # Telefones relacionados a ela
    phoneNumbers = []
    for key in respData.get('telefones', {}).keys():
        for item in respData['telefones'][key]:
            phoneNumbers.append(item)
    finalData['telefones'] = phoneNumbers
    
    # Endereços relacionados a ela
    finalData['enderecos'] = respData['enderecos']
    
    # Emails relacionados a ela
    finalData['emails'] = respData.get('emails', {})

    # Histórico profissional
    finalData['socios'] = respData.get('socios', {})

    # Participações societárias
    finalData['participacoesEmpresas'] = respData.get('participacoesEmpresas', {})

    return finalData
