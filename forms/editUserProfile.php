<?php
session_start();

$user = $_SESSION['username'] ?? '';
if (!$user) {
    header('Location: ./login.php');
    exit();
}

// Ligação à BD
$conn = new mysqli("localhost", "root", "", "marsami_game");
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Buscar os dados do utilizador
$stmt = $conn->prepare("SELECT * FROM user WHERE Username = ?");
$stmt->bind_param("s", $user);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows === 1) {
    $userData = $result->fetch_assoc();
} else {
    echo "Utilizador não encontrado.";
    exit();
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit User Profile</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="text-center text-white bg-dark">

<div class="container mt-4">
    <main class="col-lg-6 col-md-8 mx-auto">
        <h1 class="h2 mb-4">Edit Profile - <?php echo htmlspecialchars($user); ?></h1>
        <hr>

        <form method="post" action="./api/updateProfile.php">
            <input type="hidden" name="id" value="<?= htmlspecialchars($userData['Username']) ?>">

            <div class="mb-3">
                <label for="fullName" class="form-label">Full Name</label>
                <input type="text" name="fullName" class="form-control bg-dark text-white border-light" id="fullName"
                value="<?= htmlspecialchars($userData['Nome']) ?>">
            </div>

            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" name="email" class="form-control bg-dark text-white border-light" id="email"
                value="<?= htmlspecialchars($userData['Email']) ?>">
            </div>

            <div class="mb-3">
                <label for="telephone" class="form-label">Phone Number</label>
                <input type="tel" name="telephone" class="form-control bg-dark text-white border-light" id="telephone"
                value="<?= htmlspecialchars($userData['Telemovel']) ?>">
            </div>

            <button type="submit" class="btn btn-primary w-100 py-2">Save Changes</button>
        </form>

         <a href="index.php" class="btn btn-outline-light w-100 mt-3">Back to Dashboard</a>
    </main>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>