$regions = @(
  "johor","kedah","kelantan","melaka","negeri-sembilan",
  "pahang","perak","perlis","penang","sabah","sarawak",
  "selangor","terengganu","kuala-lumpur","putrajaya","labuan"
)

$types = @(
  "property","condo","apartment","house",
  "townhouse","villa","penthouse"
)

foreach ($region in $regions) {
  foreach ($type in $types) {
    Write-Host "Scraping region=$region type=$type"
    poetry run scrapy crawl fazwazrent `
      -a region=$region `
      -a property_type=$type
  }
}
