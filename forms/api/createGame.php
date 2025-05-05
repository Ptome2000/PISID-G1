<?php
session_start();
$db = "marsami_game";
$dbhost = "localhost";
// $return["message"] = "";
// $return["success"] = false;
$db_user = $_SESSION["username"];
$db_password = $_SESSION["user_pwd"];

$game_name = $_POST["name"];
$game_description = $_POST["description"];

echo $game_name;

$output = shell_exec('where python'); // Windows
echo "<pre>$output</pre>";


// $comando = 'start cmd /k "cd ../../ && python ./src/start_game.py"';
// shell_exec($comando);

$comando = 'start cmd /k "cd ../../ && pip install -r requirements.txt && python ./src/start_game.py && pause"';
shell_exec($comando);





?>