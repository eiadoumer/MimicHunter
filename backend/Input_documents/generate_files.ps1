$high = 'Plagiarism detection software compares text against a database of sources. It identifies matching phrases and generates a similarity report.'

1..5 | ForEach-Object {
    if ($_ -eq 1) { $high | Out-File -FilePath "high_$_.txt" -Encoding utf8 }
    if ($_ -eq 2) { ($high + ' (with a small addition)') | Out-File -FilePath "high_$_.txt" -Encoding utf8 }
    if ($_ -eq 3) { ($high + ' It highlights overlapping content.') | Out-File -FilePath "high_$_.txt" -Encoding utf8 }
    if ($_ -eq 4) { 'Plagiarism detection software compares text against a database of sources. It identifies matching phrases and generates a similarity report.' | Out-File -FilePath "high_$_.txt" -Encoding utf8 }
    if ($_ -eq 5) { ($high + ' The report shows percentage of similarity.') | Out-File -FilePath "high_$_.txt" -Encoding utf8 }
}

$mid = @(
    'Software for detecting plagiarism checks submitted text against existing works. It finds identical sequences and produces a similarity score.',
    'Plagiarism checkers scan documents and compare with online content. They detect copied phrases and output a matching percentage.',
    'Anti-plagiarism tools compare your text to a reference database. They identify reused sentences and create a similarity index.',
    'Plagiarism detection algorithms analyze text overlaps with source documents. They generate a report of matching content and similarity rate.',
    'A plagiarism detector compares input text against stored sources. It finds duplicate passages and reports the similarity level.'
)

$i = 1
$mid | ForEach-Object { $_ | Out-File -FilePath "mid_$i.txt" -Encoding utf8; $i++ }

$low = @(
    'Many universities require originality checking for student assignments. Teachers use software to verify that work is not copied from websites.',
    'Original writing is important in academic research. Checking for copied material helps maintain honesty in education.',
    'Some online tools can scan documents for unoriginal content. These programs highlight sentences that match other published texts.',
    'Students should learn to cite sources properly to avoid plagiarism. Paraphrasing is better than copying verbatim from references.',
    'Plagiarism checkers are helpful for both teachers and writers. They provide confidence that the work is properly attributed.'
)

$i = 1
$low | ForEach-Object { $_ | Out-File -FilePath "low_$i.txt" -Encoding utf8; $i++ }

Write-Host "Done! 15 UTF-8 files created in: $(Get-Location)"