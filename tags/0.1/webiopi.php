<?php
/*
   Copyright 2012 Eric Ptak - trouch.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

include("gpio.php");

function sendError($code, $message) {
	header($_SERVER['SERVER_PROTOCOL'] . " " . $code . " " . $message);
	exit($message);
}

function doGET($gpio, $vars) {
	if ($vars[1] == "*") {
		writeJSON($gpio);
	}
	else {
		sendError(404, "Not Found");
	}
}

function writeJSON($gpio) {
	$pins = $gpio->GPIO_AVAILABLE;
	$alt = $gpio->getALTPins();

	header("Content-Type: application/json");
	echo '{"UART": 1, "I2C": 0, "SPI": 0, "GPIO":{'. "\n";

	$first = true;
	foreach($pins as $pin) {
		if (!$first)
			print ", \n";

		$mode = "GPIO";
		$direction = "out";
		$value = 0;
		if (in_array($pin, $alt)) {
			$mode = "ALT";
		} 
		else {
			$direction = $gpio->getDirection($pin);
			$value = $gpio->getValue($pin);
		}
		
		printf ('"%d": {"mode": "%s", "direction": "%s", "value": %d}', $pin, $mode, $direction, $value);
		$first = false;
	}

	echo "\n}}";
}

function doPOST($gpio, $vars) {
	if ($vars[1] == "GPIO") {
		if (count($vars) != 5) {
			sendError(400, "Bad Request");
		}
		$pin = $vars[2];
		$cmd = $vars[3];
		$val = $vars[4];
		$ret = "";

		if ($cmd == "direction") {
			$ret = $gpio->setDirection($pin, $val);
		}
		else if ($cmd == "value") {
			$ret = $gpio->setValue($pin, $val);
		}
		else {
			sendError(400, "Bad Request");
		}

		header("Content-Type: text/plain");
		print $ret;
	}
	else {
		sendError(404, "Not Found");
	}
}

function routeRequest($gpio) {
	$method = $_SERVER['REQUEST_METHOD'];
	$request_uri = $_SERVER['REQUEST_URI'];
	$root = $_SERVER['DOCUMENT_ROOT'];
	$script = $_SERVER['SCRIPT_FILENAME'];

	$path = pathinfo($script);
	$context = substr($path['dirname'], strlen($root));
	$uri = substr($request_uri, strlen($context));

	$vars = explode('/', $uri);
	if ($method == "GET") {
		doGET($gpio, $vars);
	}
	else if ($method == "POST") {
		doPOST($gpio, $vars);
	}
	else {
		sendError(405, "Not Allowed");
	}
}


$gpio = new GPIO();
$gpio->init();

routeRequest($gpio);


?>
