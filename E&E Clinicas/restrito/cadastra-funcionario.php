<?php

require "../conexaoMysql.php";
$pdo = mysqlConnect();

$codigo = $pdo->lastInsertId();
$nome = $_POST["nome"] ?? "";
$email = $_POST["email"] ?? "";
$senha = $_POST["senha"] ?? "";
$dataNascimento = $_POST["dataNascimento"] ?? "";
$estadoCivil = $_POST["estadoCivil"] ?? "";
$funcao = $_POST["funcao"] ?? "";

// calcula um hash de senha seguro para armazenar no BD
$senhaHash = password_hash($senha, PASSWORD_DEFAULT);

try {

  $sql = <<<SQL
  -- Repare que a coluna Id foi omitida por ser auto_increment
  INSERT INTO Funcionario (codigo, nome, email, senhaHash, 
                       dataNascimento, estadoCivil, funcao)
  VALUES (?, ?, ?, ?, ?, ?, ?)
  SQL;

  // Neste caso utilize prepared statements para prevenir
  // ataques do tipo SQL Injection, pois precisamos
  // cadastrar dados fornecidos pelo usuário 
  $stmt = $pdo->prepare($sql);
  $stmt->execute([
    $codigo, $nome, $email, $senhaHash,
    $dataNascimento, $estadoCivil, $funcao
  ]);

  header("location: mostra-funcionario.php");
  exit();
} 
catch (Exception $e) {  
  exit('Falha ao cadastrar cliente: ' . $e->getMessage());
}
