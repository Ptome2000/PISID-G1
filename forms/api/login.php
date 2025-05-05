<?php 

	$db = "marsami_game";
	$dbhost = "localhost";
	$return["message"] = "";
	$return["success"] = false;
	$username = $_POST["username"];
	$password = $_POST["password"];
	try {
		$conn = mysqli_connect($dbhost, $username, $password, $db);	
		mysqli_close($conn);		
		header('Content-Type: application/json');
		$return["success"] = true;
		// echo json_encode($return);

        session_start();
        // setcookie("username", $username, time() + 3600, "/");
        
        $_SESSION["username"] = $username;
        $_SESSION["user_pwd"] = $password;
        header("Location: ../index.php");
	} catch (Exception $e) {
		$return["message"] = "The login failed. Check if the user exists in the database.";
		header('Content-Type: application/json');	

        echo $username . " ";
        echo $password;
        header("Location: ../login.php?msg=Username or Password not valid");		
	}
?>