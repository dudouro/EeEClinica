Para o site da clínica utilizando um banco de dados NoSQL, a interação seria baseada em um formato de documentos estruturados de maneira a otimizar as operações de leitura e escrita de agendamentos. Um banco de dados NoSQL como MongoDB, que utiliza documentos JSON, seria um exemplo adequado para esse tipo de implementação.

Cada documento representaria um paciente ou um agendamento, contendo todos os detalhes necessários. A estrutura seria pensada para evitar relacionamentos complexos (como em SQL) e focar em manter as informações agregadas dentro de um único documento.
Casos de Uso para o Site da Clínica

Agendar Horário na Clínica

Objetivo: Permitir que os pacientes agendem horários de consulta.
Ator Principal: Paciente
Fluxo:
Paciente acessa a página de agendamento.
Seleciona o médico/especialidade.
Escolhe data e horário disponível.
Insere informações pessoais.
Confirma o agendamento.
O sistema registra no banco de dados NoSQL.
Paciente recebe confirmação por e-mail ou SMS.

Checar Agendamentos do Dia

Objetivo: Verificar agendamentos do dia.
Ator Principal: Médico/Administrador
Fluxo:
Médico ou administrador acessa página de agendamentos.
Seleciona data atual.
Sistema exibe lista de agendamentos do dia (nome, horário, especialidade).

Remarcar Agendamento

Objetivo: Alterar data ou horário de um agendamento.
Ator Principal: Paciente
Fluxo:
Paciente acessa seus agendamentos.
Escolhe qual agendamento deseja remarcar.
Seleciona nova data e horário.
Sistema verifica disponibilidade e atualiza no banco NoSQL.
Paciente recebe confirmação.

Cancelar Agendamento

Objetivo: Cancelar um agendamento existente.
Ator Principal: Paciente
Fluxo:
Paciente acessa seus agendamentos.
Seleciona o agendamento para cancelar.
Confirma cancelamento.
Sistema remove o agendamento do banco de dados.
Paciente recebe notificação de cancelamento.
