<?php

require "../conexaoMysql.php";
$pdo = mysqlConnect();

$codigo = $pdo->lastInsertId();
$nome = $_POST["nome"] ?? "";
$especialidade = $_POST["especialidade"] ?? "";
$crm = $_POST["crm"] ?? "";

try {

  $sql = <<<SQL
  -- Repare que a coluna Id foi omitida por ser auto_increment
  INSERT INTO Medico (codigo, nome, especialidade, crm)
  VALUES (?, ?, ?, ?)
  SQL;

  // Neste caso utilize prepared statements para prevenir
  // ataques do tipo SQL Injection, pois precisamos
  // cadastrar dados fornecidos pelo usuário 
  $stmt = $pdo->prepare($sql);
  $stmt->execute([
    $codigo, $nome, $especialidade, $crm
  ]);

  header("location: mostra-medico.php");
  exit();
} 
catch (Exception $e) {  
  exit('Falha ao cadastrar cliente: ' . $e->getMessage());
}
