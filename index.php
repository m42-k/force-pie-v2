<html>
<head>
<meta charset="UTF-8">
<meta name="description" content="Golfstarz Toy Box">
<meta name="keywords" content="Golfstarz, Toy, Box">
<meta name="author" content="Michael King (n669841) & Pawan Deo (n9739033)">
<title>Toy Box Counter</title>
 
<style>
html {
	background-color: #eec6d9; 
	-webkit-background-size: cover;
	-moz-background-size: cover;
	-o-background-size: cover;
	background-size: cover;
}
* {
	margin: 0;
	padding: 0;
}
#container {
	margin-top: 10px;
	margin-left: auto;
	margin-right: auto;
	width: 100%;
}
a {
	color: #99ff99;
	font-size: 20px;
	padding-left: 20px;
}
h1 {
	font-size: 90px;
	padding: 50px auto;
	margin-top: 10px;
	text-align: center;
	text-shadow: -1px -1px 0px rgba(255,255,255,0.3), 1px 1px 0px rgba(0,0,0,0.8);
	color: #444444;
	font-family: "Impact", "Lucida Sans Unicode", "Lucida Grande", sans-serif;
	text-transform: uppercase;
}
#boximagecontainer {
	margin-top: 30px;
	margin-left: auto;
	margin-right: auto;
	width: auto;
	height: auto;
}
#boximagecontainer img {
  display: block;
  max-width: 400px;
  max-height: 400px;
  width: auto;
  height: auto;
	margin-left: auto;
	margin-right: auto;
}
#counterscontainer {
	margin-top: 20px;
	margin-left: auto;
	margin-right: auto;
	width: auto;
	height: auto;
  padding-top: 5px;
	padding-bottom: 5px;
}
p {
	font-family: "Impact", "Lucida Sans Unicode", "Lucida Grande", sans-serif;
	padding-top: 10px;
	padding-bottom: 10px;
	font-size: 70px;
	width: 100%;
	color: #000000;
	background-color: #ECECEC;
	text-align: center;
	margin-top: 20px;
	margin-left: auto;
	margin-right: auto;
}
p.green_counter {
	color: #00ca41;
}
p.red_counter {
	color: #ff0000;
}
p.yellow_counter {
	color: #ffde40;
}
</style>
</head>

<body>
<div id="container">
<h1>Toy Box</h1>
<div id="boximagecontainer">
<img src="box-image.png" alt="Toy Box"/>
</div> <!--- End of boximagecontainer -->
<div id="counterscontainer">
<p class="green_counter">
	<?php
# Debug
ini_set('display_errors', 'On');
error_reporting(E_ALL|E_STRICT);

$db = new SQLite3('/home/pi/kids-toy/toy_box.db');
$result = ($db->query('SELECT block_count FROM blocks WHERE block_colour = "Green";'));
while ($res = $result->fetchArray(SQLITE3_ASSOC)){
        #var_dump($res);
        print ("" . $res["block_count"] ."");
}
$db->close();
?>
</p>
<p class="red_counter">
	<?php
$db = new SQLite3('/home/pi/kids-toy/toy_box.db');
$result = ($db->query('SELECT block_count FROM blocks WHERE block_colour = "Red";'));
while ($res = $result->fetchArray(SQLITE3_ASSOC)){
        #var_dump($res);
        print ("" . $res["block_count"] ."");
}
$db->close();
?>
</p>
<p class="yellow_counter">
	<?php
$db = new SQLite3('/home/pi/kids-toy/toy_box.db');
$result = ($db->query('SELECT block_count FROM blocks WHERE block_colour = "Yellow";'));
while ($res = $result->fetchArray(SQLITE3_ASSOC)){
        #var_dump($res);
        print ("" . $res["block_count"] ."");
}
$db->close();
?>
</p>
</div> <!--- End of counterscontainer -->
</div> <!--- End of container -->
</body>

</html>
