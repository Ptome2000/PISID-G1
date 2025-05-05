<?php

session_start(); // Inicia a sessão

// Limpa todas as variáveis de sessão
$_SESSION = array();

session_destroy();
header('Location: ../index.php');

?>