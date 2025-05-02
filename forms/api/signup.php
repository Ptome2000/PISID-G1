<?php
$db = "ratosco";
$dbhost = "localhost";
// $return["message"] = "";
// $return["success"] = false;
$admin_user = "root";
$admin_pass = "";

// Dados do novo utilizador (normalmente definidos pelo admin ou gerados)
$username = $_POST['username'];
$password = $_POST['password'];

// Criação da ligação
$conn = new mysqli($dbhost, $admin_user, $admin_pass);

if ($conn->connect_error) {
    die("Erro na ligação: " . $conn->connect_error);
}

// 1. Criar o utilizador
$sql1 = "CREATE USER IF NOT EXISTS '$username'@'$dbhost' IDENTIFIED BY '$password'";

// 2. Atribuir permissões de leitura (SELECT)
$sql2 = "GRANT SELECT ON `$db`.* TO '$username'@'$dbhost'";

// 3. Aplicar alterações
$sql3 = "FLUSH PRIVILEGES";

if ($conn->query($sql1) === TRUE) {
    echo "Utilizador criado com sucesso.<br>";
} else {
    echo "Erro ao criar utilizador: " . $conn->error . "<br>";
}

if ($conn->query($sql2) === TRUE) {
    echo "Permissões atribuídas com sucesso.<br>";
} else {
    echo "Erro ao atribuir permissões: " . $conn->error . "<br>";
}

$conn->query($sql3);

$name = $_POST['name'];
$email = $_POST['email'];
$phone = $_POST['phone'];


// inserir user na bd
try {
    echo $name . " ";
    echo $phone . " ";
    echo $email . " ";
    $type = "USR";
    $group = 1;

    $stmt = $conn->prepare("INSERT INTO `$db`.user (Nome, Telemovel, Tipo, Email, Grupo) VALUES (?, ?, ?, ?, ?)");
    $stmt->bind_param("ssssi", $name, $phone, $type, $email, $group);
   
    if ($stmt->execute()) {
        echo "Utilizador criado com sucesso!";
    } else {
        echo "Erro ao criar utilizador: " . $stmt->error;
    }
    header("Location: ../login.php");
} catch (Exception $e) {
    $return["message"] = "The login failed. Check if the user exists in the database.";
    echo $e;
    // header('Content-Type: application/json');	
    header("Location: ../login.php?msg=Username or Password not valid");		
}

$conn->close();
