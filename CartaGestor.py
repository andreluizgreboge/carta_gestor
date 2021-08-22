from collections import Counter
from tika import parser
import pandas as pd

excluir = ['de','o','por','não','um','a','para','isso','é','mais','foram','vem','como',
           'na','que','no','e','os','as','com','do','da','das','dos','uma','em','entanto','aumenta',
           'maior','entre','ainda','já','temos','maio','são','Administração', 'BNY', 'Mellon', 'Serviços', 'Financeiros', 'DTVM', 'S/A',
           'CNPJ:', '02.201.501/0001-61', 'Av.', 'Presidente', 'Wilson,', '231,', '11º', 'andar', 'Rio', 'de', 'Janeiro', '–', 'RJ', 'CEP:',
           '20030-905', 'Telefone', '(21)', '3219-2500', 'Fax', '(21)', '3219-2508', 'www.bnymellon.com.br/sf', 'SAC:', 'Fale', 'conosco', 'no', 'endereço',
           'www.bnymellon.com.br/sf', 'ou', 'no', 'telefone', '0800', '7253219', 'Ouvidoria', 'no', 'endereço',
           'www.bnymellon.com.br/sf', 'ou', 'no', 'telefone:', '0800', '7253219', 'Este', 'material', 'é', 'meramente',
           'informativo', 'e', 'não', 'considera', 'os', 'objetivos', 'de', 'investimento,', 'a', 'situ-', 'ação', 'financeira',
           'ou', 'as', 'necessidades', 'individuais', 'de', 'um', 'ou', 'de', 'determinado', 'grupo', 'de', 'investidores.',
           'Recomendamos', 'a', 'consulta', 'de', 'profissionais', 'espe-', 'cializados', 'para', 'decisão', 'de', 'investimentos.',
           'Fundos', 'de', 'Investimento', 'não', 'contam', 'com', 'a', 'Garantia','/','caps', 'do', 'Administrador,', 'do', 'Gestor,', 'de',
           'qualquer','bahia', 'mecanis-', 'mo', 'de', 'seguro,', 'ou,', 'ainda,', 'do', 'Fundo', 'Garantidor', 'de', 'Crédito', '–', 'FGC.',
           'Rentabilidade', 'obtida','20','am', 'no', 'passado', '2020','não', 'representa', 'garantia', 'de', 'rentabilidade', 'futura.', 'Ao', 'investidor',
           'é', 'recomendada', 'a', 'leitura', 'cuidado-', 'sa', 'do', 'prospecto', 'ou', 'do', 'regulamento', 'do', 'Fundo', 'de', 'Investimento',
           'antes', 'de', 'aplicar','fic','am', 'seus', 'recursos.', 'As', 'rentabilidade', 'divulgadas', 'são', 'líquidas', 'de', 'taxa', 'de', 'administração',
           'e', 'performance', 'e', 'bruta', 'de', 'impos-', 'tos.', 'As', 'informações', 'e', 'conclusões', 'contidas', 'neste', 'material', 'podem',
           'ser', 'alteradas', 'a', 'qualquer', 'tempo,', 'sem', 'que', 'seja', 'necessária', 'prévia', 'comunicação.', 'Este', 'material', 'não', 'pode',
           'ser', 'copiado,', 'reproduzi-', 'do', 'ou', 'distribuído', 'sem', 'a', 'prévia', 'e', 'expressa', 'con-', 'cordância', 'da', 'JGP.', 'Para', 'maiores', 'informações,',
           'consulte', 'nossa', 'área', 'comercial.', 'Gestão', 'e', 'Distribuição', 'JGP', 'Gestão', 'de', 'Recursos', 'Ltda.', 'e', 'JGP', 'Gestão',
           'de', 'Crédito', 'Ltda.', 'Rua', 'Humaitá', '275,', '11º', 'andar', 'Humaitá,', 'Rio', 'de', 'Janeiro', '-', 'RJ', 'CEP:', '22261-005',
           'Brasil', 'www.jgp.com.br', 'https://www.jgp.com.br/?utm_source=report&utm_medium=pdf&utm_campaign=relatorio_gestao&utm_content=abr21', 'Relatório',
           'de', 'Gestão:', 'Carta', 'Macroeconômica', '—', 'Junho', '2021', '1', 'Relatório', 'de', 'Gestão', 'Carta', 'Macroeconômica',
           'Junho', '2021', 'Material', 'de', 'Divulgação', 'https://www.instagram.com/jgp.asset', 'https://www.linkedin.com/company/jgp',
           'http://youtube.co/jgpgestao', 'Relatório', 'de', 'Gestão:', 'Carta', 'Macroeconômica', '—', 'Junho', '2021', '2', 'Process',
           'finished','foi','janeiro', 'br/sf','with','nível','mas','gestão','está','junho','julho', 'exit','março','tudo','essa','tem','bnymellon',
           '|','essa','este','onde', 'code','pois','gestão:', '0','sobre','se','relatório','https://www','muito','ano','carta','fevereiro','www','abril','nos','também','ao','jgp',
           'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'foi', 'ao',
           'ele', 'das', 'tem', 'à', 'seu', 'sua', 'ou', 'ser', 'quando', 'muito', 'há', 'nos', 'já', 'está', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre',
           'era', 'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus', 'quem', 'nas', 'me', 'esse', 'eles', 'estão', 'você', 'tinha', 'foram', 'essa', 'num', 'nem', 'suas', 'meu', 'às',
           'minha', 'têm', 'numa', 'pelos', 'elas', 'havia', 'seja', 'qual', 'será', 'nós', 'tenho', 'lhe', 'deles', 'essas', 'esses', 'pelas', 'este', 'fosse', 'dele', 'tu', 'te',
           'vocês', 'vos', 'lhes', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas', 'nosso', 'nossa', 'nossos', 'nossas', 'dela', 'delas', 'esta', 'estes', 'estas', 'aquele', 'aquela',
           'aqueles', 'aquelas', 'isto', 'aquilo', 'estou', 'está', 'estamos', 'estão', 'estive', 'esteve', 'estivemos', 'estiveram', 'estava', 'estávamos', 'estavam', 'estivera',
           'estivéramos', 'esteja', 'estejamos', 'estejam', 'estivesse', 'estivéssemos', 'estivessem', 'estiver', 'estivermos', 'estiverem', 'hei', 'há', 'havemos', 'hão',
           'houve', 'houvemos', 'houveram', 'houvera', 'houvéramos', 'haja', 'hajamos', 'hajam', 'houvesse', 'houvéssemos', 'houvessem', 'houver', 'houvermos', 'houverem',
           'houverei', 'houverá', 'houveremos', 'houverão', 'houveria', 'houveríamos', 'houveriam', 'sou', 'somos', 'são', 'era', 'éramos', 'eram', 'fui', 'foi', 'fomos',
           'foram', 'fora', 'fôramos', 'seja', 'sejamos', 'sejam', 'fosse', 'fôssemos', 'fossem', 'for', 'formos', 'forem', 'serei', 'será', 'seremos', 'serão', 'seria',
           'seríamos', 'seriam', 'tenho', 'tem', 'temos', 'tém', 'tinha', 'tínhamos', 'tinham', 'tive', 'teve', 'tivemos', 'tiveram', 'tivera', 'tivéramos', 'tenha', 'tenhamos',
           'tenham', 'sendo','novos','fim','novos','meses','fundos','02%','07%','r','início','ab','alguns','21','long','quanto','tivesse','3','data','fundo','25%','9','8','7','6','5','4','2','1', 'tivéssemos','fi', 'tivessem','ativos','novas', 'tiver', 'mês','tivermos', 'pl','tiverem','fia', 'terei', 'terá', 'teremos', 'terão', 'teria', 'teríamos', 'teriam']



jgp = 'C:\\Users\\André Greboge\\PycharmProjects\\SuperRankFIDCS\\carta\\'

gestores = []


for gestor in gestores:
    cols = ['','','','','','','','','','']
    comum = []
    pdfs = ['0121','0221','0321','0421','0521','0621','0721']
    for pdf in pdfs:
        # comum = []
        pdf_ler = parser.from_file(gestor + pdf + '.pdf')
        pdf_lido = pdf_ler['content']
        for char in '-.,\n':
            pdf_lido=pdf_lido.replace(char,' ')
        pdf_lido = pdf_lido.lower()
        lista_palavras_desordenada = [s.lower() for s in pdf_lido.split() if s.lower() not in excluir]
        mais_comum = Counter(lista_palavras_desordenada).most_common(10)
        comum.append(mais_comum)
    tabela = pd.DataFrame(comum, columns=cols)
    print(comum)
    tabela.to_excel('tabela.xlsx')



