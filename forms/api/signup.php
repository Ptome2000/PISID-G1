<?php
$db = "marsami_game";
$dbhost = "localhost";
// $return["message"] = "";
// $return["success"] = false;
$admin_user = "root";
$admin_pass = "";

// Criação da ligação
$conn = new mysqli($dbhost, $admin_user, $admin_pass);
if ($conn->connect_error) {
    die("Erro na ligação: " . $conn->connect_error);
}

// Dados do novo utilizador
$username = $_POST['username'];
$password = $_POST['password'];
$name = $_POST['name'];
$email = $_POST['email'];
$phone = $_POST['phone'];

// inserir user na bd
try {
    $sql = "CALL criar_utilizador($name, $username, $email, $password, $phone)"
    if ($conn->query($sql) === TRUE) {
        echo "Utilizador criado com sucesso.<br>";
        header("Location: ../login.php");
    } else {
        echo "Erro ao criar utilizador: " . $conn->error . "<br>";
    }
} catch (Exception $e) {
    $return["message"] = "The login failed. Check if the user exists in the database.";
    echo $e;
    // header('Content-Type: application/json');	
//     header("Location: ../login.php?msg=Username or Password not valid");
}

$conn->close();
