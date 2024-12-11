<?php
$csv_url = 'http://localhost:80/ListAll/csv'

$cb = curl_init($csv_url)
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$data = curl_exec($ch);

if ($data === false) {
    die('Error fetching CSV: ' . curl_error($ch));
}

curl_close($ch);

header('Content-Type: text/csv');
header('Content-Disposition: attachment; filename="brevets.csv"');
echo $data;
?>