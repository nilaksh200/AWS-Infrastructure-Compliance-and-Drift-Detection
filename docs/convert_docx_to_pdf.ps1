param(
    [string]$DocxPath,
    [string]$PdfPath
)

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($DocxPath)
    
    # Update all fields (Table of Contents, Page Numbers, Cross-References)
    try {
        $doc.Fields.Update()
    } catch {
        Write-Output "Field update note: $_"
    }

    # wdFormatPDF = 17
    $doc.SaveAs([ref]$PdfPath, [ref]17)
    $doc.Close([ref]0) # wdDoNotSaveChanges
    Write-Output "Successfully converted $DocxPath to $PdfPath"
} catch {
    Write-Error "Conversion failed: $_"
    exit 1
} finally {
    $word.Quit()
}
