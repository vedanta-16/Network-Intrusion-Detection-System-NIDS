# NIDS Incident Report

## Incident ID
NIDS-1024

## Detection
Port Scan

## Severity
HIGH

## Source
192.168.1.25

## Target
192.168.1.50

## Evidence
- High SYN activity
- Multiple connection attempts
- Abnormal flow behavior
- ML prediction classified the flow as malicious

## ML Confidence
96%

## Recommended Action
Investigate the source host and review associated network traffic and authentication logs.
