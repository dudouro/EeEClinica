<?php

require "../conexaoMysql.php";
$pdo = mysqlConnect();

try {
  // Consulta SQL para buscar os dados do agendamento, médico e paciente
  $sql = <<<SQL
  SELECT A.Datahora, 
         M.Nome as nomeMedico, 
         P.Nome as nomePaciente, 
         P.Sexo, 
         P.Email, 
         P.Telefone
  FROM Agendamento A
  INNER JOIN Medico M ON A.CodigoMedico = M.Codigo
  INNER JOIN Paciente P ON A.CodigoPaciente = P.Codigo
  SQL;

  // Executa a consulta
  $stmt = $pdo->query($sql);
} 
catch (Exception $e) {
  exit('Ocorreu uma falha: ' . $e->getMessage());
}
?>
<!doctype html>
<html lang="pt-BR">

<head>
  <meta charset="utf-8">
  <!-- Tag de responsividade -->
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Agendamentos Cadastrados</title>

  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
  <style>
    body {
      padding-top: 2rem;
    }
  </style>  
</head>

<body>

  <div class="container">
    <h3>Agendamentos Cadastrados</h3>
    <table class="table table-striped table-hover">
      <tr>
        <th>Data e Hora</th>
        <th>Nome do Médico</th>
        <th>Nome do Paciente</th>
        <th>Sexo do Paciente</th>
        <th>Email do Paciente</th>
        <th>Telefone do Paciente</th>
      </tr>

      <?php
      while ($row = $stmt->fetch()) {

        // Limpa os dados produzidos pelo usuário
        $dataAgendamento = htmlspecialchars($row['Datahora']);
        $nomeMedico = htmlspecialchars($row['nomeMedico']);
        $nomePaciente = htmlspecialchars($row['nomePaciente']);
        $sexoPaciente = htmlspecialchars($row['Sexo']);
        $emailPaciente = htmlspecialchars($row['Email']);
        $telefonePaciente = htmlspecialchars($row['Telefone']);

        // Formata a data de agendamento
        $data = new DateTime($dataAgendamento);
        $dataFormatoDiaMesAno = $data->format('d-m-Y H:i');

        echo <<<HTML
          <tr>
            <td>$dataFormatoDiaMesAno</td> 
            <td>$nomeMedico</td>
            <td>$nomePaciente</td>
            <td>$sexoPaciente</td>
            <td>$emailPaciente</td>
            <td>$telefonePaciente</td>
          </tr>      
        HTML;
      }
      ?>

    </table>
    <a href="../index.html">Menu de opções</a>
  </div>

</body>

</html>
