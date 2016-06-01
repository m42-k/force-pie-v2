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

# Open DB
$db = new SQLite3('../toy_box.db');

# you do a query statment that return a strange
# SQLite3Result object that you have to use
# in the fetch statement below
$result = ($db->query('SELECT * FROM blocks;'));
#print_r($result); # I wanted to see what it actually was

# The fetch call will return a boolean False if it hits
# the end, so why not use it in a while loop?
#
# The fetchArray() call can return an 'associated' array
# that actually means give you back an array of ordered
# pairs with name, value.  This is cool because it means
# I can access the various values by name. Each call to
# fetchArray return one row from the thermostats table
while ($res = $result->fetchArray(SQLITE3_ASSOC)){
        #var_dump($res);
        print ("<strong>" . $res["block_num"] ." thermostat,</strong><br />");
        print ("Currently: " . $res["block_colour"] . " <br \>");
        print ("Temperature: " . $res["block_count"] . " <br \>");
        print ("<br>");
}
$db->close(); # I opened it, I should close it
?>
	<?php
	phpinfo();
	?>
<?php
$db = new SQLite('../toy_box.db');

var_dump($db->querySingle('SELECT block_count FROM blocks WHERE block_colour = "Red"'));
print_r($db->querySingle('SELECT block_count FROM blocks WHERE block_colour = "Green"'));

$db->close();
?>
</p>
<p class="red_counter">
2
</p>
<p class="yellow_counter">
3
</p>
</div> <!--- End of counterscontainer -->
</div> <!--- End of container -->
</body>

</html>
