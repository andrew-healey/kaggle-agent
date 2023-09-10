import { Browser, Page, launch } from "puppeteer";

import { config } from "dotenv";
import { BrowserDriver } from "./browser.js";
config();

const {HEADLESS} = process.env;
const headless = HEADLESS === "false" ? false : "new";
const executablePath = process.env.EXECUTABLE_PATH;

export const getBrowser = () => launch({
  headless,
  defaultViewport: null,
  args: [
    "--window-size=1920,1080",
    "--window-position=0,0",
    "--disable-blink-features=AutomationControlled"
  ],
  ignoreDefaultArgs: ["--enable-automation"],
  // executablePath,
  channel: "chrome"
});