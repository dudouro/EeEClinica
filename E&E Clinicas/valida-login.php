<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require "conexaoMysql.php";
$pdo = mysqlConnect();

$email = $_POST["email"] ?? "";
$senha = $_POST["senha"] ?? "";

try {
  $sql = <<<SQL
    SELECT senhahash FROM Funcionario
    WHERE email = ?
  SQL;

  $stmt = $pdo->prepare($sql);
  $stmt->execute([$email]);

  $row = $stmt->fetch();
  if ($row && password_verify($senha, $row['senhahash'])) {
    // Login com sucesso
    header("Location: restrito/index.html");
    exit();
  } else {
    // Login falhou
    echo "Usuário ou senha incorretos.";
  }
} 
catch (Exception $e) {  
  exit('Falha ao verificar login: ' . $e->getMessage());
}
