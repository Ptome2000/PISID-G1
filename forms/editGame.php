<?php
session_start();
if (!isset($_SESSION['username'])) {
    header('Location: login.php');
    exit();
}

$host = 'localhost';
$dbname = 'marsami_game';
$user = 'root';
$password = '';

$conn = new mysqli($host, $user, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$gameId = $_GET['id'] ?? null;
if (!$gameId) {
    die("ID do jogo não fornecido.");
}

// Preparar a query com mysqli
$stmt = $conn->prepare("SELECT * FROM game WHERE IDJogo = ? AND Username = ?");
$stmt->bind_param("is", $gameId, $_SESSION['username']);
$stmt->execute();
$result = $stmt->get_result();
$game = $result->fetch_assoc();

if (!$game) {
    die("Jogo não encontrado ou não pertence ao utilizador.");
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit Game</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="text-center text-white bg-dark">

<div class="container mt-4">
    <main class="col-lg-6 col-md-8 mx-auto">
        <h1 class="h2 mb-4">Edit Game</h1>
        <hr>

        <form method="post" action="./api/updateGame.php">
            <input type="hidden" name="id" value="<?= htmlspecialchars($game['IDJogo']) ?>">

            <div class="mb-3">
                <label for="gameName" class="form-label">Game Name</label>
                <input type="text" name="name" class="form-control bg-dark text-white border-light" id="gameName"
                       value="<?= htmlspecialchars($game['GameName']) ?>" required>
            </div>

            <div class="mb-3">
                <label for="gameDescription" class="form-label">Description</label>
                <textarea name="description" class="form-control bg-dark text-white border-light" id="gameDescription"
                          rows="3" required><?= htmlspecialchars($game['Description']) ?></textarea>
            </div>

            <button type="submit" class="btn btn-primary w-100 py-2">Save Changes</button>
        </form>

        <a href="index.php" class="btn btn-outline-light w-100 mt-3">Back to Dashboard</a>
    </main>
</div>

</body>
</html>