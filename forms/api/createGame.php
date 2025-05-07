<?php
set_time_limit(300); // tempo em segundos (ex: 300 = 5 minutos)
session_start();
$db = "marsami_game";
$dbhost = "localhost";
$db_user = $_SESSION["username"];

$game_name = $_POST["name"];
$game_description = $_POST["description"];

$cmd = sprintf(
    'start c:/xampp/htdocs/mazerun/scripts/start_pc2.bat %s %s %s && pause',
    escapeshellarg($db_user),
    escapeshellarg($game_name),
    escapeshellarg($game_description)

);

// echo $comando;
shell_exec($cmd);

header("Location: ../index.php");

?>