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

$id = $_POST['id'] ?? null;
$name = $_POST['name'] ?? '';
$description = $_POST['description'] ?? '';
$username = $_SESSION['username'] ?? '';

if (!$id || !$username) {
    die('Dados inválidos.');
}

$stmt = $conn->prepare("UPDATE game SET GameName = ?, Description = ? WHERE IDJogo = ? AND Username = ?");
$stmt->bind_param("ssis", $name, $description, $id, $username);
$stmt->execute();

header("Location: ../index.php");
exit;