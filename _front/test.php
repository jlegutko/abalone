<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">

    <title>Hello, world!</title>
    <style>
      html {
        display: flex;
        justify-content: center;
        align-items: center;
        align-content: center;
        height: 100%;
      }
      body { 
        width: 50rem;
        text-align: center;
      }
      .box {
        position: relative;
        display: inline-block;
        width: 11%;
        height: 8%; 
        border-radius: 50%;
        margin-right: -4px;
        background: #aaa;
        border: 0.5rem solid white;
        cursor: pointer;
      }

      .box:focus {
        background: #000;
        outline: none;
      }
    </style>
  </head>
  <body>
    
    <?php

    $x = 5;

    for ($i = 0; $i < 5; $i++) {
      for ($y = 0; $y < $x; $y++) {
        print('<button class="box box-' . $i . ',' . $y . '"></button>' . "\n");
      }
      print('<br>' . "\n");
      $x++;
    }

    $x = 0;

    for ($i = 4; $i > 0; $i--) {
      for ($y = 8; $y > $x; $y--) {
        print('<button class="box box-' . $i . ',' . $y . '"></button>' . "\n");
      }
      print('<br>' . "\n");
      $x++;
    }

    ?>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/js/bootstrap.min.js" integrity="sha384-a5N7Y/aK3qNeh15eJKGWxsqtnX/wWdSZSKp+81YjTmS15nvnvxKHuzaWwXHDli+4" crossorigin="anonymous"></script>
  </body>
</html>