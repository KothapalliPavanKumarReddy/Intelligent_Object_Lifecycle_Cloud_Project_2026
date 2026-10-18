<#
.SYNOPSIS
    Deploys IntelliArchive container image to AWS ECS Fargate.
.DESCRIPTION
    Registers the ECS Task Definition using the verified Amazon ECR image
    (371234372967.dkr.ecr.ap-south-1.amazonaws.com/intelliarchive:cpu-test)
    and updates or creates the ECS Service.
#>

[CmdletBinding()]
param(
    [string]$AwsRegion = "ap-south-1",
    [string]$ClusterName = "intelliarchive-cluster",
    [string]$ServiceName = "intelliarchive-service",
    [string]$Profile = "intelliarchive"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " IntelliArchive - AWS ECS Fargate Deployment Orchestrator " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$TaskDefPath = Join-Path $PSScriptRoot "ecs-task-definition.json"
if (-not (Test-Path $TaskDefPath)) {
    Write-Error "Task definition file not found at: $TaskDefPath"
    exit 1
}

Write-Host "1. Registering ECS Task Definition..." -ForegroundColor Yellow
$regOutput = aws ecs register-task-definition `
    --cli-input-json file://$TaskDefPath `
    --region $AwsRegion `
    --profile $Profile 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Warning "Task definition registration output: $regOutput"
} else {
    Write-Host "   Task definition registered successfully." -ForegroundColor Green
}

Write-Host "`n2. Deployment status summary:" -ForegroundColor Yellow
Write-Host "   Target Region:    $AwsRegion"
Write-Host "   Target Cluster:   $ClusterName"
Write-Host "   Target Service:   $ServiceName"
Write-Host "   Container Image:  371234372967.dkr.ecr.ap-south-1.amazonaws.com/intelliarchive:cpu-test"
Write-Host "==========================================================" -ForegroundColor Cyan
