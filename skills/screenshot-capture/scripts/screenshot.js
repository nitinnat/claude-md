#!/usr/bin/env node

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function captureScreenshot(url, options = {}) {
  const {
    output,
    selector,
    fullPage = false,
    outputDir = 'public/assets/screenshots'
  } = options;

  const browser = await chromium.launch({
    headless: true
  });

  try {
    const context = await browser.newContext({
      viewport: { width: 1200, height: 800 },
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    });

    const page = await context.newPage();

    console.log(`Navigating to ${url}...`);
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });

    // Wait a bit for dynamic content
    await page.waitForTimeout(2000);

    // Ensure output directory exists
    const projectRoot = process.cwd();
    const screenshotDir = path.join(projectRoot, outputDir);
    if (!fs.existsSync(screenshotDir)) {
      fs.mkdirSync(screenshotDir, { recursive: true });
    }

    // Generate filename
    const timestamp = Date.now();
    const filename = output ? `${output}.png` : `screenshot_${timestamp}.png`;
    const filepath = path.join(screenshotDir, filename);

    // Take screenshot
    if (selector) {
      console.log(`Capturing element: ${selector}`);
      const element = await page.locator(selector).first();
      await element.screenshot({ path: filepath });
    } else {
      console.log(`Capturing ${fullPage ? 'full page' : 'viewport'}...`);
      await page.screenshot({
        path: filepath,
        fullPage
      });
    }

    console.log(`Screenshot saved to: ${filepath}`);
    return filepath;

  } catch (error) {
    console.error(`Error capturing screenshot: ${error.message}`);
    throw error;
  } finally {
    await browser.close();
  }
}

// Parse command line arguments
function parseArgs() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args[0].startsWith('--')) {
    console.error('Usage: node screenshot.js <URL> [--output filename] [--selector CSS_SELECTOR] [--full-page]');
    process.exit(1);
  }

  const options = {
    url: args[0]
  };

  for (let i = 1; i < args.length; i++) {
    switch (args[i]) {
      case '--output':
        options.output = args[++i];
        break;
      case '--selector':
        options.selector = args[++i];
        break;
      case '--full-page':
        options.fullPage = true;
        break;
      case '--output-dir':
        options.outputDir = args[++i];
        break;
    }
  }

  return options;
}

// Main execution
if (require.main === module) {
  const { url, ...options } = parseArgs();
  captureScreenshot(url, options)
    .then(() => process.exit(0))
    .catch((error) => {
      console.error('Failed to capture screenshot:', error);
      process.exit(1);
    });
}

module.exports = { captureScreenshot };
