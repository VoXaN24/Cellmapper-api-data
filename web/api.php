<?php

// Connect to the SQLite database
$db = new SQLite3('db.db');

// Get the value of the "country" parameter from the request
$countryParam = $_GET['country'];

// Get the value of the "cellmapper" parameter from the request
$cellmapperParam = $_GET['cellmapper'];

// Check if the "country" parameter is set to "all"
if ($countryParam === 'all') {
    // Query the database to get all countries and their abbreviations
    $query = "SELECT name, abv FROM country";
    $result = $db->query($query);

    // Fetch the results and store them in an array
    $countries = [];
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $countries[] = $row;
    }

    // Return the countries as JSON
    echo json_encode($countries);
} else {
    // Query the database to get the abbreviation of the specified country
    $query = "SELECT abv FROM country WHERE name = :country";
    $stmt = $db->prepare($query);
    $stmt->bindValue(':country', $countryParam, SQLITE3_TEXT);
    $result = $stmt->execute();

    // Fetch the result
    $row = $result->fetchArray(SQLITE3_ASSOC);

    // Check if a result was found
    if ($row) {
        // Return the abbreviation as JSON
        echo json_encode($row['abv']);
    } else {
        // Return an error message if the country was not found
        if ($countryParam) {
        echo json_encode(['error' => 'Country not found']);
        }
    }
}

// Check if the "cellmapper" parameter is set
if ($cellmapperParam) {
    // Query the database to get the networks with the specified abbreviation
    $query = "SELECT network_name, mmc, mnc FROM mmcmnc_cellmapper WHERE country_code = :abv";
    $stmt = $db->prepare($query);
    $stmt->bindValue(':abv', $cellmapperParam, SQLITE3_TEXT);
    $result = $stmt->execute();

    // Fetch the results and store them in an array
    $networks = [];
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $networks[] = $row;
    }

    // Return the networks as JSON
    echo json_encode($networks);
}

// Close the database connection
$db->close();

?>
