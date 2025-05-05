<?php
session_start();
$db = "marsami_game";
$dbhost = "localhost";
$db_user = $_SESSION["username"];

$game_name = $_POST["name"];
$game_description = $_POST["description"];

$comando = sprintf(
    'start cmd /k "cd ../../ && pip install -r requirements.txt && python ./src/start_game.py %s %s %s && pause"',
    escapeshellarg($db_user),
    escapeshellarg($game_name),
    escapeshellarg($game_description)
);

// echo $comando;
shell_exec($comando);

header("Location: ../index.php");


?>