param(
    [Parameter(Position=0, Mandatory=$true)]
    [string]$Url,

    [Parameter(Position=1, Mandatory=$false)]
    [string]$Skill = "all"
)

if ($Skill -eq "all") {
    python run.py $Url
} else {
    python run.py $Url --skill $Skill
}
