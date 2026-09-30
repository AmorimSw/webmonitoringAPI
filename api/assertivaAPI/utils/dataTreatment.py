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
    finalData['emails'] = respData.get('emails', {})

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

def emailDataTreatment(rawData:dict) -> dict:
    '''Retorna um dicionário estruturado para o uso, a partir dos dados obtidos\n
    em consulta via API do Assertiva por e-mail.'''

    respData:dict = rawData.get('resposta', '')
    if not respData:
        return
    finalData = dict()

    # Pessoas físicas relacionadas ao e-mail
    finalData['pessoaFisica'] = respData.get('pessoaFisica', [])
    
    # Pessoas jurídicas relacionadas ao e-mail
    finalData['pessoaJuridica'] = respData.get('pessoaJuridica', [])

    return finalData

def phoneDataTreatment(rawData:dict) -> dict:
    '''Retorna um dicionário estruturado para o uso, a partir dos dados obtidos\n
    em consulta via API do Assertiva por telefone.'''

    respData:dict = rawData.get('resposta', '')
    if not respData:
        return
    finalData = dict()

    # Pessoas físicas relacionadas ao telefone
    finalData['pessoaFisica'] = respData.get('pessoaFisica', [])
    
    # Pessoas jurídicas relacionadas ao telefone
    finalData['pessoaJuridica'] = respData.get('pessoaJuridica', [])

    return finalData

def nameAddressDataTreatment(rawData:dict) -> dict:
    '''Retorna um dicionário estruturado para o uso, a partir dos dados obtidos\n
    em consulta via API do Assertiva por nome ou endereço.'''

    respData:dict = rawData.get('resposta', '')
    if not respData:
        return
    finalData = dict()

    # Pessoas físicas relacionadas ao nome ou endereço
    finalData['pessoaFisica'] = respData.get('pessoaFisica', [])
    
    # Pessoas jurídicas relacionadas ao nome ou endereço
    finalData['pessoaJuridica'] = respData.get('pessoaJuridica', [])

    return finalData

def vehicleHistoryDataTreatment(rawData:dict) -> dict:
    '''Retorna um dicionário estruturado para o uso, a partir dos dados obtidos\n
    em consulta via API do Assertiva por histórico de veículos.'''

    respData:dict = rawData.get('resposta', '')
    if not respData:
        return {}
    finalData = dict()

    # Histórico de veículos
    finalData['historicoVeiculos'] = respData.get('historicoVeiculos', [])

    return finalData
