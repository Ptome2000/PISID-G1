<?php
$db = "marsami_game";
$dbhost = "localhost";
// $return["message"] = "";
// $return["success"] = false;
$admin_user = "root";
$admin_pass = "";

// Criação da ligação
$conn = new mysqli($dbhost, $admin_user, $admin_pass, $db);
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
    $stmt = $conn->prepare("CALL criar_utilizador(?, ?, ?, ?, ?)");
    if ($stmt === false) {
        throw new Exception("Erro na preparação da query: " . $conn->error);
    }

    $stmt->bind_param("sssss", $name, $username, $email, $password, $phone);

    if ($stmt->execute()) {
        echo "Utilizador criado com sucesso.<br>";
        header("Location: ../login.php");
    } else {
        echo "Erro ao criar utilizador: " . $stmt->error . "<br>";
    }

    $stmt->close();
} catch (Exception $e) {
    $return["message"] = "The login failed. Check if the user exists in the database.";
    echo $e;
    // header('Content-Type: application/json');
//     header("Location: ../login.php?msg=Username or Password not valid");
}

$conn->close();
