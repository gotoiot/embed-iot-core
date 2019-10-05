<!DOCTYPE html>
  <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    </head>
    <body>
        <h1>Bienvenido a la aplicacion de CMS</h1>
        <h2>Implementada mediante imagen de docker abassi/php-server:latest</h2>
        <br>
        <h4>Esta aplicacion interpreta los beacons recibidos como argumentos</h4>
        <h4>En funcion del beacon recibido devuelve diferente contenido HTMLs</h4>
        <?php
            $major = $_GET["major"];
            $minor = $_GET["minor"];

            if ($major == "111" && $minor == "111"){
                print_r('<body style="background-color:#663366;"></body>');
                print_r("<h1>Se esta mostrando el contenido del beacon major/minor: 111/111</h1>");
            } elseif ($major == "111" && $minor == "222"){
                print_r('<body style="background-color:#006633;"></body>');
                print_r("<h1>Se esta mostrando el contenido del beacon major/minor: 111/222</h1>");
            } elseif ($major == "222" && $minor == "111"){
              print_r('<body style="background-color:#886633;"></body>');
              print_r("<h1>Se esta mostrando el contenido del beacon major/minor: 222/111</h1>");
            } elseif ($major == "222" && $minor == "222"){
              print_r('<body style="background-color:#5566AA;"></body>');
              print_r("<h1>Se esta mostrando el contenido del beacon major/minor: 222/222</h1>");
            } else {
                print_r('<body style="background-color:#990000;"></body>');
                print_r("<h1>Se recibio un beacon desconocido!</h1>");
            }
        ?>
    </body>
    <footer>
            Copyright Agustin Bassi - 2019
    </footer>
  </html>