Aplicação que extrai o relatório no formato necessário para a Multiplan do banco de dados do Parkinplus.
É necessário antes, que se crie uma VIEW no banco da forma descrita a baixo, e um usuário específico para essa view, de forma a não comprometer a segurança do banco.
O programa deve ser compilado com o IP do banco, usuário e senha, da garagem que irá utilizá-lo.

-- Primeiro se cria a VIEW:

CREATE VIEW abonolojistamultiplan 
AS SELECT ticketonline, tarifa, datahorasaida 
FROM logrotativo  
WHERE nometarifa IN ("NOME DAS TARIFAS REALACIONADAS AO APP LOGISTA"));

-- Segundo se cria a role e a concede acesso unico á VIEW criada.

--DROP ROLE multiplan;
CREATE ROLE multiplan LOGIN
ENCRYPTED PASSWORD 'md5(A SENHA CRIPTOGRAFADA EM MD5)'
NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE;

GRANT SELECT ON public.abonolojistamultiplan TO multiplan;

Após isso, alterar no código o número de IP usuario e senha (porta e banco se necessário) e compilá-lo.
