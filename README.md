# ticketshield-indexnow

Automated IndexNow submission for TicketShield.com - Daily sitemap scraping and search engine indexing

## Overview

This repository automates the process of submitting URLs from the TicketShield website to search engines using the IndexNow protocol. The workflow runs daily at 2 AM UTC and can also be triggered manually.

## How It Works

1. **Fetches Sitemap**: Retrieves all URLs from https://www.ticketshield.com/sitemap.xml
2. **Submits to IndexNow**: Batch submits all URLs to search engines (Bing, Yandex, etc.) using the IndexNow protocol
3. **Generates llms.txt**: Creates an AI-friendly site description file for LLM discoverability

## Setup Instructions

### 1. Add GitHub Secret

The workflow requires an `INDEXNOW_KEY` GitHub secret to be configured:

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `INDEXNOW_KEY`
5. Value: `0d50972d50074294add5020661864326`
6. Click **Add secret**

### 2. Verify API Key File on Website

Ensure the following file exists on your Framer site:
- URL: `https://www.ticketshield.com/.well-known/0d50972d50074294add5020661864326.txt`
- Content: `0d50972d50074294add5020661864326`

This file is required by IndexNow to verify ownership of your domain.

### 3. Manual Trigger (Optional)

To manually run the workflow:
1. Go to the **Actions** tab in your repository
2. Select **IndexNow Daily Submission**
3. Click **Run workflow**
4. Select the branch and click **Run workflow**

## Files

- **`.github/workflows/indexnow.yml`**: GitHub Actions workflow configuration
- **`indexnow_automation.py`**: Python script that handles the submission logic
- **`llms.txt`**: Generated file (not committed) for AI assistant discoverability

## IndexNow Protocol

IndexNow is a protocol that allows webmasters to instantly inform search engines about the latest content changes on their website. Supported by:
- Microsoft Bing
- Yandex
- And others

Learn more: https://www.bing.com/indexnow/getstarted

## Uploading llms.txt to Framer

The workflow generates `llms.txt` locally during execution. To make it available on your website:

1. After the workflow runs, the `llms.txt` file is generated
2. Manually upload this file to your Framer site's `.well-known` directory
3. The file should be accessible at: `https://www.ticketshield.com/.well-known/llms.txt`

**Note**: Automatic upload to Framer would require Framer API credentials, which are not currently configured.

## Schedule

The workflow runs automatically:
- **Schedule**: Daily at 2:00 AM UTC (9:00 PM EST / 6:00 PM PST)
- **Manual**: Can be triggered anytime via GitHub Actions UI

## Troubleshooting

### Workflow Fails
- Verify the `INDEXNOW_KEY` secret is set correctly
- Check that the sitemap URL (https://www.ticketshield.com/sitemap.xml) is accessible
- Ensure the API key file exists at the `.well-known` URL

### No URLs Found
- Verify the sitemap XML is properly formatted
- The script will fall back to a list of known important pages if the sitemap fetch fails

### IndexNow Submission Errors
- HTTP 200: Success
- HTTP 202: Accepted and queued
- HTTP 400: Bad request (check URL format)
- HTTP 403: Forbidden (verify API key file)
- HTTP 422: Unprocessable (check URL format)

## Support

For issues or questions about the IndexNow protocol, visit:
- IndexNow Documentation: https://www.indexnow.org/
- Bing Webmaster Tools: https://www.bing.com/webmasters/
