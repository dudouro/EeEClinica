<?php

require "../conexaoMysql.php";
$pdo = mysqlConnect();

try {
  $sql = <<<SQL
  SELECT codigo, nome, email, telefone, 
         mensagem, datahora
  FROM Contato
  SQL;

  // Neste exemplo não é necessário utilizar prepared statements
  // porque não há a possibilidade de injeção de SQL, 
  // pois nenhum parâmetro do usuário é utilizado na query SQL. 
  // Além disso, como há resultados a serem processados, 
  // utilizamos o método query (e não o exec).
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
  <!-- 1: Tag de responsividade -->
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Clientes cadastrados</title>

  <!-- 2: Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
  <style>
    body {
      padding-top: 2rem;
    }
    img {
      width: 20px;
    }
  </style>  
</head>

<body>

  <div class="container">
    <h3>Mensagens Cadastradas</h3>
    <table class="table table-striped table-hover">
      <tr>
        <th></th>
        <th>Codigo</th>
        <th>Nome</th>
        <th>Email</th>
        <th>Telefone</th>
        <th>Mensagem</th>
        <th>DataHora</th>
      </tr>

      <?php
      while ($row = $stmt->fetch()) {

        // Limpa os dados produzidos pelo usuário
        // com possibilidade de ataque XSS
        // antes de inserí-los na página HTML
        $nome = htmlspecialchars($row['nome']);
        $telefone = htmlspecialchars($row['telefone']);
        $email = htmlspecialchars($row['email']);
        $mensagem = htmlspecialchars($row['mensagem']);

        $data = new DateTime($row['datahora']);

        echo <<<HTML
          <tr>
            <td>
            </td> 
            <td>{$row['codigo']}</td> 
            <td>$nome</td>
            <td>$email</td>
            <td>$telefone</td>
            <td>$mensagem</td>
            <td>$data</td>
          </tr>      
        HTML;
      }
      ?>

    </table>
    <a href="index.html">Menu de opções</a>
  </div>

</body>

</html>