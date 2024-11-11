<?php

require "../conexaoMysql.php";
$pdo = mysqlConnect();

$codigo = $pdo->lastInsertId();
$nome = $_POST["nome"] ?? "";
$email = $_POST["email"] ?? "";
$telefone = $_POST["telefone"] ?? "";
$mensagem = $_POST["mensagem"] ?? "";
$datahora = $_POST["datahora"] ?? "";


try {

  $sql = <<<SQL
  -- Repare que a coluna Id foi omitida por ser auto_increment
  INSERT INTO Contato (codigo, nome, email, telefone, mensagem, datahora)
  VALUES (?, ?, ?, ?, ?, ?)
  SQL;

  // Neste caso utilize prepared statements para prevenir
  // ataques do tipo SQL Injection, pois precisamos
  // cadastrar dados fornecidos pelo usuário 
  $stmt = $pdo->prepare($sql);
  $stmt->execute([
    $codigo, $nome, $email, $telefone, $mensagem, $datahora
  ]);

  header("location: mostra-contato.php");
  exit();
} 
catch (Exception $e) {  
  exit('Falha ao cadastrar cliente: ' . $e->getMessage());
}
