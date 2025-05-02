<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
    <style>
        body {
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f8f9fa; /* Cor de fundo clara */
        }
        .form-container {
            width: 100%;
            max-width: 360px; /* Tamanho da box */
            padding: 2rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>

    <div class="form-container">
      <form action="./api/login.php" method="post">
        <h1 class="h3 mb-3 fw-normal text-center">Login</h1>
    
        <div class="form-floating">
          <input type="text" class="form-control" name="username" id="floatingInput" placeholder="Username" required>
          <label for="floatingInput">Username</label>
        </div>
        <div class="form-floating mt-2">
          <input type="password" class="form-control" name="password" id="floatingPassword" placeholder="Password">
          <label for="floatingPassword">Password</label>
        </div>
        <hr>
        <button class="btn btn-dark w-100 py-2" type="submit">
            <a href="#" class="text-white text-decoration-none">Login</a>
          </button>        
        <p class="mt-3 text-center">
            Don't have an account? <a href="signIn.html">Sign up</a>
        </p>
        
        <p class="mt-3 mb-0 text-body-secondary text-center">2025</p>
      </form>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-3xPpM17w5D8lgrdksmsu+vBgFekUMw+i9Zs2Xsna3AymsGpQmSRvtxNncYccBteB" crossorigin="anonymous"></script>
    <script>
      const params = new URLSearchParams(window.location.search);
      const msg = params.get('msg');
      if (msg) {
        alert(msg)
      }
    </script>

    <?php
      $user = $_COOKIE['username'] ?? '';
      if ($user) header('Location: ./dashboard.php')
    ?>
</body>
</html>