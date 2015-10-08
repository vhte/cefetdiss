/* Total de consumidores MT por segmento */
select ConsumidorMT.* from ConsumidorMT, TransformadorMT,EquipamentoMT
WHERE ConsumidorMT.TRANSFORMADOR_ID = TransformadorMT.ID
AND TransformadorMT.ID=EquipamentoMT.ID
AND EquipamentoMT.SEGMENTO_ID = 410

/* Total de consumidores BT por segmento */
SELECT EquipamentoMT.SEGMENTO_ID, count(ConsumidorBT.ID) AS 'consumidores'
FROM ConsumidorBT, PontoServicoBT, TrechoBT, TransformadorMT, EquipamentoMT, Segmento
WHERE ConsumidorBT.PONTO_SERVICO_ID=PontoServicoBT.ID
AND PontoServicoBT.BARRABT_ID=TrechoBT.BARRABT_FIM_ID
AND TrechoBT.TRANSFORMADOR_ID=TransformadorMT.ID
AND TransformadorMT.ID=EquipamentoMT.ID
AND EquipamentoMT.SEGMENTO_ID = Segmento.ID
/*AND EquipamentoMT.SEGMENTO_ID BETWEEN 139 and 152*/
AND Segmento.ID = 410
GROUP BY EquipamentoMT.SEGMENTO_ID;

/* Total de equipamentos  por alimentador */
select Alimentador.ID, Alimentador.CEMIG_ID, COUNT(EquipamentoMT.ID) as 'totalequip' 
FROM EquipamentoMT, Segmento,Alimentador
where EquipamentoMT.SEGMENTO_ID = Segmento.ID
and Segmento.ALIMENTADOR_ID = Alimentador.ID
/*and Alimentador.ID = 11*/
group by Alimentador.CEMIG_ID
order by totalequip desc;

/* Quantidade de equipamentos por segmento */
select COUNT(EquipamentoMT.ID) as 'totalequip'/*, EquipamentoMT.IC*/, EquipamentoMT.SEGMENTO_ID
FROM EquipamentoMT, Segmento,Alimentador
where EquipamentoMT.SEGMENTO_ID = Segmento.ID
and Segmento.ALIMENTADOR_ID = Alimentador.ID
/*and Alimentador.ID = 11*/
group by SEGMENTO_ID
order by totalequip desc

/* Todos os equipamentos de um determinado segmento */
select EquipamentoMT.*, EquipamentoMT.IC, EquipamentoMT.SEGMENTO_ID
FROM EquipamentoMT, Segmento,Alimentador
where EquipamentoMT.SEGMENTO_ID = Segmento.ID
and Segmento.ALIMENTADOR_ID = Alimentador.ID
AND EquipamentoMT.SEGMENTO_ID = 410 /*622 e 557*/

/* Calcula preço de equipamento por TipoEquipamento*/
SELECT DISTINCT EquipamentoNovo.* FROM EquipamentoNovo, TipoEquipamento, EquipamentoMT
WHERE EquipamentoMT.TIPO_EQUIPAMENTO_ID = TipoEquipamento.ID
AND TipoEquipamento.ID = EquipamentoNovo.TIPO_EQUIPAMENTO_ID
AND EquipamentoMT.TIPO_EQUIPAMENTO_ID=55

/* Total de equipamentos por alimentador*/
select Alimentador.CEMIG_ID,count(EquipamentoMT.ID) as 'totalequip' FROM EquipamentoMT, Segmento, Alimentador
WHERE Alimentador.ID = Segmento.ALIMENTADOR_ID
AND Segmento.ID = EquipamentoMT.SEGMENTO_ID
group by Alimentador.CEMIG_ID
order by totalequip ASC

/* Equips com preços por segmento */
select distinct EquipamentoMT.ID, EquipamentoMT.IC,

IF(EquipamentoMT.TIPO_EQUIPAMENTO_ID != 1, EquipamentoNovo.CUSTO, (EquipamentoNovo.CUSTO/1000*CaboMT.COMPRIMENTO)) AS 'CUSTO',
EquipamentoNovo.CUSTO,

EquipamentoMT.TIPO_EQUIPAMENTO_ID
from EquipamentoMT
join Segmento ON EquipamentoMT.SEGMENTO_ID = Segmento.ID
join EquipamentoNovo ON EquipamentoNovo.TIPO_EQUIPAMENTO_ID = EquipamentoMT.TIPO_EQUIPAMENTO_ID
left join CaboMT ON EquipamentoMT.ID = CaboMT.ID
where Segmento.ID = 410

/* Equips com preço por equips */
SELECT DISTINCT EquipamentoMT.ID AS ID, EquipamentoMT.IC AS IC, 
IF(EquipamentoMT.TIPO_EQUIPAMENTO_ID != 1, EquipamentoNovo.CUSTO, (EquipamentoNovo.CUSTO/1000*CaboMT.COMPRIMENTO)) AS CUSTO
/*EquipamentoNovo.CUSTO,*/ 
/*EquipamentoMT.TIPO_EQUIPAMENTO_ID */
FROM EquipamentoMT 
JOIN Segmento ON EquipamentoMT.SEGMENTO_ID = Segmento.ID 
JOIN Alimentador ON Segmento.ALIMENTADOR_ID = Alimentador.ID 
JOIN EquipamentoNovo ON EquipamentoNovo.TIPO_EQUIPAMENTO_ID = EquipamentoMT.TIPO_EQUIPAMENTO_ID 
LEFT JOIN CaboMT ON EquipamentoMT.ID = CaboMT.ID
WHERE Alimentador.ID = 3;

/* Numero de eventos de interrupcao, unidades afetados e tempo das interrupcoes por ANO e por ALIMENTADOR */
SELECT COUNT(ID) AS 'EVENTOS', SUM(CONS_DIST) as 'AFETADOS', SUM(DURACAO)/60 AS 'DURACAO'
FROM Interrupcao
WHERE YEAR(DATA_INICIO) = 2011; /*2012*/;

SELECT Alimentador.CEMIG_ID,COUNT(Interrupcao.ID) AS 'EVENTOS', SUM(Interrupcao.CONS_DIST) as 'AFETADOS', SUM(Interrupcao.DURACAO)/60 AS 'DURACAO'
FROM Interrupcao, Alimentador
WHERE Interrupcao.ALIMENTADOR_ID = Alimentador.ID
GROUP BY Alimentador.CEMIG_ID ASC;


/* Numero interrupcoes por mês dos alimentadores */
SELECT
	Alimentador.CEMIG_ID,
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=1,1,0)) AS 'JAN',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=2,1,0)) AS 'FEV',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=3,1,0)) AS 'MAR',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=4,1,0)) AS 'APR',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=5,1,0)) AS 'MAY',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=6,1,0)) AS 'JUN',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=7,1,0)) AS 'JUL',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=8,1,0)) AS 'AUG',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=9,1,0)) AS 'SEP',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=10,1,0)) AS 'OCT',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=11,1,0)) AS 'NOV',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=12,1,0)) AS 'DEZ'
FROM
	Interrupcao, Alimentador
WHERE
	Interrupcao.ALIMENTADOR_ID = Alimentador.ID AND
	Alimentador.CEMIG_ID LIKE 'BHSE%' AND
	YEAR(Interrupcao.DATA_INICIO) = 2013
GROUP BY
	Alimentador.CEMIG_ID;

/* Soma de unidades afetadas por todas as interrupcoes no ano */
SELECT
	Alimentador.CEMIG_ID,
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=1,Interrupcao.CONS_DIST,0)) AS 'JAN',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=2,Interrupcao.CONS_DIST,0)) AS 'FEV',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=3,Interrupcao.CONS_DIST,0)) AS 'MAR',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=4,Interrupcao.CONS_DIST,0)) AS 'APR',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=5,Interrupcao.CONS_DIST,0)) AS 'MAY',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=6,Interrupcao.CONS_DIST,0)) AS 'JUN',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=7,Interrupcao.CONS_DIST,0)) AS 'JUL',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=8,Interrupcao.CONS_DIST,0)) AS 'AUG',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=9,Interrupcao.CONS_DIST,0)) AS 'SEP',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=10,Interrupcao.CONS_DIST,0)) AS 'OCT',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=11,Interrupcao.CONS_DIST,0)) AS 'NOV',
	SUM(IF(MONTH(Interrupcao.DATA_INICIO)=12,Interrupcao.CONS_DIST,0)) AS 'DEC'
FROM
	Interrupcao, Alimentador
WHERE
	Interrupcao.ALIMENTADOR_ID = Alimentador.ID AND
	Alimentador.CEMIG_ID LIKE 'BHSE%' AND
	YEAR(Interrupcao.DATA_INICIO) = 2013
GROUP BY
	Alimentador.CEMIG_ID;
