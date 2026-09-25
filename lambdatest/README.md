# TestMu AI (Formerly LambdaTest) integration

## Overview

TestMu AI (formerly LambdaTest) is a full-stack agentic AI quality engineering platform for web, mobile, and enterprise applications. Its AI agents help plan, author, execute, and analyze tests throughout the software development lifecycle.

Use the TestMu AI integration to log bugs in Datadog while testing websites and web applications across browsers. TestMu AI includes testing environment details, such as browser version, operating system, and resolution, along with comments and screenshots.

The platform supports manual testing and automated testing with Selenium, Playwright, Cypress, Puppeteer, Appium, Espresso, and XCUITest. Testing is available across more than 3,000 browser and operating system combinations and more than 10,000 real devices.

### Supported TestMu AI products

The integration covers the TestMu AI products that send session data to Datadog:

- [Real-Time Testing](https://www.testmuai.com/live-testing/): Live, interactive manual testing across browsers and virtual devices. Use the Mark as Bug action during a session to capture an annotated screenshot and open a Datadog ticket without leaving the test.
- [Test Automation Platform](https://www.testmuai.com/automation-testing-platform/): Run Selenium, Playwright, Cypress, and Puppeteer suites on a cloud grid. Web automation runs stream test status, duration, browser, and operating system to Datadog.
- [Native App Automation Cloud](https://www.testmuai.com/mobile-app-testing/): Run Appium, Espresso, and XCUITest suites against mobile apps. App automation runs stream the same execution data to Datadog.
- [Real Devices Cloud](https://www.testmuai.com/real-device-cloud/): Run manual or automated tests on real iOS and Android hardware. Real device sessions are tagged so you can break usage down by device in the Datadog dashboard.

## Setup

Configure the integration in the TestMu AI dashboard. For instructions, see the [TestMu AI-Datadog integration setup guide][1].

### Configuration

To track incidents in Datadog with TestMu AI:

1. Click **Connect Accounts** to begin authorization of the TestMu AI integration from the Login page in TestMu AI.
2. Log in to your TestMu AI account on the TestMu AI website to be redirected to the Datadog authorization page.
3. Click **Authorize** to complete the integration process.
4. A confirmation email is sent once the integration configuration is complete.
5. Once Datadog is integrated with your TestMu AI account, start logging bugs and performing cross-browser testing.

## Uninstallation

Once you uninstall this integration, any previous authorizations are revoked. 

Additionally, ensure that all API keys associated with this integration have been disabled by searching for the integration name on the [API Keys management page](/organization-settings/api-keys?filter=LambdaTest).

## Support

For support or feature requests, contact TestMu AI on the following channels:

Email: support@testmuai.com
Phone: +1-(866)-430-7087
Website: https://www.testmuai.com/

[1]: https://www.testmuai.com/support/docs/datadog-integration/