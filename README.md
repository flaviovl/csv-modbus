## Objetivo

Este projeto é base de um sistema de monitoramento e coleta de dados de multimedidores usando a biblioteca pymodbus.

## Funcionalidades

* Conectar, desconectar e ler registradores usando pymodbus;
* Ler arquivos .csv de mapas de memoria e gerar de forma automatica mapa de registradores para coleta de dados;
* Filtrar mapas de registradores por grupos (tipos de coleção);
* Gerar blocos de registradores contíguos para reduzir número de requisições ao dispositivo;
* Gerar função de decodificação de responsta; 


## Os seguintes multimedidores são suportados:
* Multimedidor de Grandezas Elétricas MD30 - Embrasul
* Multimedidor de Grandezas Elétricas TR4020 - EMBRASUL

obs: para adicionar um novo multimedidor é necessário gerar um arquivo csv com seu respectivo mapa de memória
