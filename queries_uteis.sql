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
