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
            <h1 class="h2 mb-4">
                Dashboard - <?php 
                    session_start();

                    $user = $_SESSION['username'] ?? ''; 
                    if (!$user) {
                        header('Location: ./login.php');
                    }
                    echo $user;
                ?>
                 - <a href="api/logout.php">Logout</a>
            </h1>
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
                            <th scope="col">Score</th>
                            <th scope="col">Status</th>
                            <th scope="col">Edit</th>

                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>Name1</td>
                            <td>placeholder</td>
                            <td>date</td>
                            <td>20</td>
                            <td>Running</td>
                            <td><button class="btn btn-primary">Edit Game</button></td>
                        </tr>
                        <tr>
                            <td>2</td>
                            <td>Name2</td>
                            <td>placeholder</td>
                            <td>date</td>
                            <td>5</td>
                            <td>Ended</td>
                            <td><button class="btn btn-primary">Edit Game</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </main>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>