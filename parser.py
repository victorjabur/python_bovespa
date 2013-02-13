import os
import bovespaparser.bovespaparser as bp
import MySQLdb
from bovespaparser import CODNEG, NOMRES, ESPECI, DATA, PREABE, PREMIN, PREMAX, PREMED, PREULT, PREOFC, PREOFV, TOTNEG, QUATOT, VOLTOT

def parseFile(filename, opts):
    with open(filename, 'rU') as f:
        return bp.parsedata(f, opts)

def importData():
    diretorio = 'D:/bovespa/cotahist/'
    opts=[CODNEG, NOMRES, ESPECI, DATA, PREABE, PREULT, PREMIN, PREMAX, PREMED, PREOFC, PREOFV, TOTNEG, QUATOT, VOLTOT]
    for arquivo in os.listdir(diretorio):
        print 'Processando o arquivo ' + arquivo
        if arquivo.startswith('COTAHIST'):
            cotas = parseFile(diretorio + arquivo, opts)
            importToMysql(cotas)
        print 'OK'

def insertToTableMySql(nome_tabela, dictCampos):
    sql_cabecalho = 'insert into ' + nome_tabela + '('
    sql_nome_campo = ''
    sql_valor_campo = ''
    for nome_campo, valor_campo in dictCampos.items():
        sql_nome_campo = sql_nome_campo + nome_campo + ','
        sql_valor_campo = sql_valor_campo + "'" + str(valor_campo) + "',"
    sql = sql_cabecalho + sql_nome_campo[:-1] + ') values(' + sql_valor_campo[:-1] + ')'
    return sql

def importToMysql(cotas):
    db = MySQLdb.connect(host='localhost', user='bovespa', passwd='bovespa', db='bovespa')
    cursor = db.cursor()
    for f_codneg, f_nomres, f_especi, f_data, f_preabe, f_preult, f_premin, f_premax, f_premed, f_preofc, f_preofv, f_totneg, f_quatot, f_voltot in cotas:
        campos = {'codigo_acao' : f_codneg,
                  'nome_empresa' : f_nomres,
                  'tipo_acao' : f_especi,
                  'data' : f_data,
                  'preco_abertura' : f_preabe,
                  'preco_fechamento' : f_preult,
                  'preco_minimo' : f_premin,
                  'preco_maximo' : f_premax,
                  'preco_medio' : f_premed,
                  'preco_melhor_oferta_compra' : f_preofc,
                  'preco_melhor_oferta_venda' : f_preofv,
                  'quantidade_titulos_negociados' : f_totneg,
                  'numero_negocios' : f_quatot,
                  'volume_negociado' : f_voltot}
        sql = insertToTableMySql('cotacao_bovespa', campos)
        try:
            cursor.execute(sql)
        except Exception, err:
            print err
    db.commit()
importData()
