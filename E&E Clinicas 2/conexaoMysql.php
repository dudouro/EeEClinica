<?php

function mysqlConnect()
{
  $db_host = "sql305.infinityfree.com";
  $db_username = "if0_37401687";
  $db_password = "eeeclinicas";
  $db_name = "if0_37401687_clinica";

  $options = [
    PDO::ATTR_EMULATE_PREPARES => false, // desativa a execução emulada de prepared statements
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION // ativa o lançamento de exceções em casos de erros
  ];

  try {
    $pdo = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8mb4", $db_username, $db_password, $options);
    return $pdo;
  } 
  catch (Exception $e) {
    exit('Ocorreu uma falha na conexão com o MySQL: ' . $e->getMessage());
  }
}

?>