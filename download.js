import {getBrowser} from "./puppeteer.js"

const browser = await getBrowser();

const searchPage = await browser.newPage();
const projectPage = await browser.newPage();

const getNotebookUrls = async (pageNum)=>{
    await searchPage.goto(`https://www.kaggle.com/code?sortBy=voteCount&page=${pageNum}&language=Python`)
    await 
}

await searchPage.goto("https://www.kaggle.com/code?sortBy=voteCount&page=1&language=Python")