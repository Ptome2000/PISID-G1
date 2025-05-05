<?php
session_start();

$host = 'localhost';
$dbname = 'marsami_game';
$user = 'root';
$password = '';

$conn = new mysqli($host, $user, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Confirmar que o utilizador está autenticado
$username = $_SESSION['username'] ?? '';
if (!$username) {
    header('Location: ../login.php');
    exit();
}

// Dados do formulário
$fullName = $_POST['fullName'] ?? '';
$email = $_POST['email'] ?? '';
$telephone = $_POST['telephone'] ?? '';

// Validação simples
if (!$fullName || !$email || !$telephone) {
    die("Todos os campos são obrigatórios.");
}

// Atualizar os dados do utilizador (mantendo o username intacto)
$stmt = $conn->prepare("UPDATE user SET Nome = ?, Email = ?, Telemovel = ? WHERE Username = ?");
$stmt->bind_param("ssss", $fullName, $email, $telephone, $username);
$stmt->execute();

header("Location: ../index.php");
exit;