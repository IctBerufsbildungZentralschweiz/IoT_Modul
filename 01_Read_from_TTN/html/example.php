<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <link rel="stylesheet" href="style.css">
    <link rel='icon' href='favicon.ico' type='image/x-icon'/ >
    <link href="https://fonts.googleapis.com/css?family=Lora&display=swap" rel="stylesheet">
    <title>MySQL -- Webpage</title>

</head>
<h1>Auslesen der MySQL Datenbank</h1>

<?php
// IP of SQL server
$servername = "localhost";
// MySQL user
$username = "root";
// MySQL password empty if none
$password = "";
// Name of DB
$dbname = "rak811_db";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}
// SQL-Statement to read Data
$sql = "SELECT * FROM tbl_messages ORDER BY time desc LIMIT 1";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
  // output data of each row
  while($row = $result->fetch_assoc()) {
    // Create flex-container for Data
    echo "<div class=\"container\">";
    // Create div with data Title is H3 Data is H4
      echo "<div class=\"timebox\"><h3>Zeitpunkt: </h3><h4> " . date_format(date_create($row["time"]), "d.m.Y H:i:s") . "</h4></div>";
      echo "<div class=\"box\"><h3>App_id: </h3><h4>     ". $row["app_id"]."</h4></div>";
      echo "<div class=\"box\"><h3>Channel: </h3><h4> ". $row["channel"]."</h4></div>";
      echo "<div class=\"box\"><h3>coding_rate: </h3><h4> ". $row["coding_rate"]."</h4></div>";
      echo "<div class=\"box\"><h3>counter: </h3><h4> ". $row["counter"]."</h4></div>";
	    echo "<div class=\"box\"><h3>dev_id: </h3><h4> ". $row["dev_id"]."</h4></div>";
      echo "<div class=\"box\"><h3>hardware_serial: </h3><h4> ". $row["hardware_serial"]."</h4></div>";
	    echo "<div class=\"box\"><h3>modulation: </h3><h4> ". $row["modulation"]."</h4></div>";
	    echo "<div class=\"box\"><h3>payload_raw: </h3><h4> ". $row["payload_raw"]."</h4></div>";
	    echo "<div class=\"box\"><h3>port: </h3><h4> ". $row["port"]."</h4></div>";
      echo "<div class=\"box\"><h3>rf_chain: </h3><h4> ". $row["rf_chain"]."</h4></div>";
      echo "<div class=\"box\"><h3>rssi: </h3><h4> ". $row["rssi"]."</h4></div>";
	    echo "<div class=\"box\"><h3>snr: </h3><h4> ". $row["snr"]."</h4></div>";
      echo "<div class=\"box\"><h3>tmstmp: </h3><h4> ". $row["tmstmp"]."</h4></div>";
	    echo "<div class=\"box\"><h3>data_rate: </h3><h4> ". $row["data_rate"]."</h4></div>";
	    echo "<div class=\"box\"><h3>topic: </h3><h4> ". $row["topic"]."</h4></div>";



	    echo "<div class=\"box\"><h3>channel: </h3><h4> ". $row["channel"]."</h4></div></div>";


    echo "<div class=\"container\">";
    echo "<div class=\"timebox\"><h3>Zeitpunkt: </h3><h4> " . date_format(date_create($row["time"]), "d.m.Y H:i:s") . "</h4></div>";

    foreach ($row as $title => $item) {
      
      echo "<div class=\"box\"><h3>". $title.": </h3><h4>     ". $item."</h4></div>";
    }

    




    }
} else {
  echo "0 results";
}
$conn->close();
?>