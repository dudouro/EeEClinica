<?php

require "../conexaoMysql.php";
$pdo = mysqlConnect();

$nome = $_POST["nome"] ?? "";
$email = $_POST["email"] ?? "";
$tel = $_POST["tel"] ?? "";
$dataAgendamento = $_POST["dataAgendamento"] ?? "";
$sexo = $_POST["sexo"] ?? "";
$codMedico = $_POST["codMedico"] ?? "";

try {
  // Inicia a transação
  $pdo->beginTransaction();

  // CRIAR PACIENTE
  $sql1 = <<<SQL
  INSERT INTO Paciente (Nome, Email, Telefone, Sexo)
  VALUES (:nome, :email, :tel, :sexo)
  SQL;

  $stmt1 = $pdo->prepare($sql1);
  $stmt1->bindParam(':nome', $nome);
  $stmt1->bindParam(':email', $email);
  $stmt1->bindParam(':tel', $tel);
  $stmt1->bindParam(':sexo', $sexo);
  $stmt1->execute();

  $codPaciente = $pdo->lastInsertId();

  // CRIAR AGENDAMENTO
  $sql2 = <<<SQL
  INSERT INTO Agendamento (Datahora, CodigoMedico, CodigoPaciente)
  VALUES (:dataAgendamento, :codMedico, :codPaciente)
  SQL;

  $stmt2 = $pdo->prepare($sql2);
  $stmt2->bindParam(':dataAgendamento', $dataAgendamento);
  $stmt2->bindParam(':codMedico', $codMedico);
  $stmt2->bindParam(':codPaciente', $codPaciente);
  $stmt2->execute();

  // Confirma as operações (commit)
  $pdo->commit();

  header("location: mostra-agendamento.php");
  exit();
} 
catch (Exception $e) {  
  // Desfaz as operações em caso de erro
  $pdo->rollBack();
  exit('Falha ao cadastrar agendamento: ' . $e->getMessage());
}
