<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
</head>
<body class="text-center text-white bg-dark">

    <div class="container mt-4">
        <main class="col-lg-8 col-md-10 mx-auto">
    <?php
        session_start();
        $user = $_SESSION['username'] ?? '';
        if (!$user) {
            header('Location: ./login.php');
            exit();
        }
    ?>

    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="h2 mb-0">
            Dashboard - <?php echo htmlspecialchars($user); ?>
        </h1>
        <div class="d-flex gap-2">
            <a href="editUserProfile.php" class="btn btn-outline-light">Edit Profile</a>
            <a href="api/logout.php" class="btn btn-outline-danger">Logout</a>
        </div>
    </div>

    <hr>
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h2 class="mb-0">Games</h2>
                <a href="createGame.html" class="btn btn-light">Start New Game</a>
            </div>

            <div class="table-responsive small">
                <table class="table table-dark table-striped table-sm">
                    <thead>
                        <tr>
                            <th scope="col">Game Id</th>
                            <th scope="col">Name</th>
                            <th scope="col">Description</th>
                            <th scope="col">Date</th>
                            <th scope="col">Status</th>
                            <th scope="col">Edit</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php
                            $conn = new mysqli("localhost", "root", "", "marsami_game");

                            if ($conn->connect_error) {
                                die("Connection failed: " . $conn->connect_error);
                            }

                            $stmt = $conn->prepare("SELECT IDJogo, GameName, Description, StartDate, GameOver FROM game WHERE Username = ?");
                            $stmt->bind_param("s", $user);
                            $stmt->execute();
                            $result = $stmt->get_result();

                            $hasGames = false;

                            while ($row = $result->fetch_assoc()) {
                                $gameIsOver = $row["GameOver"] == 0 ? "disabled" : "";
                                echo $gameIsOver;
                                $hasGames = true;
                                $status = $row["GameOver"] ? "Ended" : "Running";
                                echo "<tr>";
                                echo "<td>{$row['IDJogo']}</td>";
                                echo "<td>" . htmlspecialchars($row['GameName']) . "</td>";
                                echo "<td>" . htmlspecialchars($row['Description']) . "</td>";
                                echo "<td>{$row['StartDate']}</td>";
                                echo "<td>{$status}</td>";
                                $gameId = $row['IDJogo'];
                                echo "<td><a href=\"editGame.php?id=$gameId\" class=\"$gameIsOver btn btn-outline-primary\">Edit Game</a></td>";
                                echo "</tr>";
                            }

                            if (!$hasGames) {
                                echo "<tr><td colspan='7' class='text-center'>No games found. Start a new game to see it listed here.</td></tr>";
                            }

                            $stmt->close();
                            $conn->close();
                        ?>
                    </tbody>
                </table>
            </div>
        </main>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>